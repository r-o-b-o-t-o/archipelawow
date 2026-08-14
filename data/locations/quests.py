import math
from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from ...world import World

from worlds.generic.Rules import set_rule

from ... import regions
from ...conditions import combine_rules, has_all, required_level
from ..items.zones import EXPANSION_ZONE_IDS, ZONES_CONTAINER, Zone
from .location_container import LocationContainer
from .location_registry import Location
from .quest_model import QuestModel, load_quest_models_by_id

STARTING_ZONES_MAX_LEVEL = 10
MIN_QUESTS_PER_REGION = 5


def get_quest_region(level: int, zones: list[Zone]) -> str:
    """The level bracket a quest belongs to, its zones overruling its advertised level in Outland and Northrend.

    Both expansions start handing out quests before their bracket begins -- Hellfire Peninsula offers quests from
    level 58, Borean Tundra from 68 -- which would file them next to the classic content they undercut. The zone a
    quest takes place in is the better answer there, so it raises the quest to its own bracket. Only Outland and
    Northrend zones do this: classic zones sit in a different bracket per faction, and quests are built once at
    import time, before any faction is known.
    """
    region = regions.get_region_by_level(level)
    expansion_regions = [z.region_a for z in zones if z.zone_id in EXPANSION_ZONE_IDS]
    if len(expansion_regions) == 0:
        return region

    # The earliest expansion zone the quest touches, since the zone items themselves gate reaching the rest
    floor = min(expansion_regions, key=lambda r: regions.REGION_LEVELS[r])
    return max(region, floor, key=lambda r: regions.REGION_LEVELS[r])


class Quest(Location):
    def __init__(self, name: str, quest_id: int, level: int, region: str, zones: list[Zone] | None = None, display_zone=True):
        zones = list(zones) if zones else []

        name = f"Quest: {name}"
        if display_zone and len(zones) > 0:
            name += f" ({zones[0].name})"

        super().__init__(name)
        self.quest_id = quest_id
        self.level = level
        self.region = region
        self.zones = zones
        # Filled in by resolve_requirements once the whole prerequisite graph exists
        self.required_zones: list[Zone] = zones
        self.required_level: int = level

        QUESTS_CONTAINER.add(self)


class QuestsContainer(LocationContainer):
    def __init__(self) -> None:
        super().__init__()
        self.quests: dict[int, Quest] = {}
        self.quests_json: dict[int, QuestModel] = {}
        # The container is a singleton shared by every player, and the density roll must not be re-rolled per caller
        self.__locations_cache: "WeakKeyDictionary[World, list[Quest]]" = WeakKeyDictionary()

    def add(self, quest: Quest):
        super().add(quest)
        self.quests[quest.quest_id] = quest

    def load_quests_json(self):
        self.quests_json = load_quest_models_by_id(__name__, "quests.json")

        for id, data in self.quests_json.items():
            zone_ids = [z.id for z in [*data.start_zones, *data.objective_zones, *data.end_zones]]
            if data.quest_sort_area:
                zone_ids.insert(0, data.quest_sort_area.id)
            # Dedupe in place so the sort area stays in front and the location is named after it
            quest_zones = list(filter(None, [ZONES_CONTAINER.zones.get(id) for id in dict.fromkeys(zone_ids)]))

            level = data.recommended_level or data.min_level or 1
            region = get_quest_region(level, quest_zones)

            Quest(name=data.display_title, quest_id=id, level=level, region=region, zones=quest_zones)

        self.resolve_requirements()

    def resolve_requirements(self):
        """Roll each quest's prerequisites into the zones and level it takes to finish it.

        Archipelago only knows the rule we give a location, and it has no notion of a quest chain: left
        alone it will happily rule that a Westfall quest is in logic while the quest that unlocks it waits
        in Tanaris. Requirements therefore travel up the chain -- every `requires_all` prerequisite adds
        its own, and a `requires_any` set adds only what all of its alternatives agree on, since the player
        picks one.
        """
        resolved: dict[int, tuple[dict[int, Zone], int]] = {}

        def requirements(quest_id: int, chain: set[int]) -> tuple[dict[int, Zone], int, bool]:
            """The zones and level a quest takes, plus whether a cycle left that answer provisional."""
            cached = resolved.get(quest_id)
            if cached is not None:
                return (*cached, False)

            if quest_id in chain:
                # Back edge: it can only repeat what the chain already carries, but it does mean the
                # answer we are building depends on a quest still being worked out, so nothing on the
                # way back up may be cached
                return {}, 0, True

            quest = self.quests.get(quest_id)
            data = self.quests_json.get(quest_id)
            if quest is None or data is None:
                return {}, 0, False

            chain.add(quest_id)
            zones = {z.zone_id: z for z in quest.zones}
            level = quest.level
            provisional = False

            for id in data.requires_all:
                prerequisite_zones, prerequisite_level, unsettled = requirements(id, chain)
                zones.update(prerequisite_zones)
                level = max(level, prerequisite_level)
                provisional = provisional or unsettled

            if len(data.requires_any) > 0:
                alternatives = [requirements(id, chain) for id in data.requires_any]
                shared = set.intersection(*[set(zone_map) for zone_map, _, _ in alternatives])
                for zone_map, _, unsettled in alternatives:
                    provisional = provisional or unsettled
                    zones.update({id: zone for id, zone in zone_map.items() if id in shared})
                # Whichever alternative the player takes, the cheapest one still has to be cleared
                level = max(level, min(alternative_level for _, alternative_level, _ in alternatives))

            chain.discard(quest_id)
            if not provisional:
                resolved[quest_id] = (zones, level)

            return zones, level, provisional

        for quest_id, quest in self.quests.items():
            zones, level, _ = requirements(quest_id, set())
            quest.required_zones = list(zones.values())
            quest.required_level = level

    def starts_in_other_starting_zone(self, quest_id: int, world: "World") -> bool:
        """Whether the quest itself sits in a level 01-10 zone reserved for other races."""
        quest = self.quests.get(quest_id)
        if quest is None or quest.level > STARTING_ZONES_MAX_LEVEL:
            return False

        race = world.options.character_race.value
        return any(len(zone.starter_for_races) > 0 and race not in zone.starter_for_races for zone in quest.zones)

    def needs_a_group(self, quest_id: int, world: "World") -> bool:
        """Whether the quest asks for a bigger party than the player signed up for."""
        data = self.quests_json.get(quest_id)
        if data is None:
            return False

        # The extractor leaves the field unset on solo quests and never writes a party smaller than two
        return (data.suggested_group_size or 1) > world.options.quests_max_party_size.value

    def runs_in_a_dungeon(self, quest_id: int, world: "World") -> bool:
        """Whether the quest takes place inside a dungeon, when the options ask for those to be left out."""
        if world.options.quests_include_dungeons:
            return False

        data = self.quests_json.get(quest_id)
        return data is not None and data.is_dungeon

    def conflicts_with_character_options(self, quest_id: int, world: "World") -> bool:
        """Whether the quest is offered only to races or classes other than the chosen ones."""
        data = self.quests_json.get(quest_id)
        if data is None:
            return False

        return (data.races is not None and world.options.character_race.value not in data.races) or (
            data.classes is not None and world.options.character_class.value not in data.classes
        )

    def resolve_unreachable_quests(self, world: "World") -> set[int]:
        """Ids of the quests the options put out of reach, prerequisite chains included.

        Prerequisites follow the extractor semantics: a quest needs any one of its `requires_any`
        prerequisites and every one of its `requires_all` ones, so it is only unreachable when all of
        the former or at least one of the latter is unreachable.
        """
        excluded: set[int] = set()
        resolved: set[int] = set()
        skip_other_starting_zones = not world.options.quests_all_starting_zones

        def is_blocked(quest_id: int) -> bool:
            """The reasons a quest is out of reach on its own, before its prerequisites are looked at.

            Has to cover every reason `filter_locations` drops a quest, not just the quest options: a
            quest whose prerequisite is locked to another race or class is as unfinishable as one behind
            a party the player has not got, and the difference is invisible once the prerequisite is gone.
            """
            return (
                self.conflicts_with_character_options(quest_id, world)
                or self.runs_in_a_dungeon(quest_id, world)
                or self.needs_a_group(quest_id, world)
                or (skip_other_starting_zones and self.starts_in_other_starting_zone(quest_id, world))
            )

        def resolve(quest_id: int, chain: set[int]) -> tuple[bool, bool]:
            """Whether the quest is unreachable, and whether a cycle left that answer provisional."""
            if quest_id in resolved:
                return quest_id in excluded, False

            if quest_id in chain:
                # Back edge: it says nothing about reachability, but it does mean everything waiting on
                # it further up the stack is still being worked out and must not be recorded as final
                return False, True

            data = self.quests_json.get(quest_id)
            if data is None:
                # Prerequisite dropped by the extractor, treat it as unobtainable
                return True, False

            if is_blocked(quest_id):
                resolved.add(quest_id)
                excluded.add(quest_id)
                return True, False

            chain.add(quest_id)
            results = [*[resolve(id, chain) for id in data.requires_any], *[resolve(id, chain) for id in data.requires_all]]
            chain.discard(quest_id)

            any_results = results[: len(data.requires_any)]
            unreachable = (len(any_results) > 0 and all(blocked for blocked, _ in any_results)) or any(
                blocked for blocked, _ in results[len(data.requires_any) :]
            )
            provisional = any(unsettled for _, unsettled in results)

            if not provisional:
                resolved.add(quest_id)
                if unreachable:
                    excluded.add(quest_id)

            return unreachable, provisional

        for quest_id in self.quests:
            # Nothing is in progress at the top of the walk, so even a cycle's best answer is final here
            unreachable, _ = resolve(quest_id, set())
            resolved.add(quest_id)
            if unreachable:
                excluded.add(quest_id)

        return excluded

    def build_locations(self, world: "World") -> list[Quest]:
        """The quests that become locations for this world, rolled once so that every caller sees the same set."""
        locations = self.__locations_cache.get(world)
        if locations is None:
            locations = self.pick_locations(world)
            self.__locations_cache[world] = locations

        return locations

    def pick_locations(self, world: "World") -> list[Quest]:
        """Trim the eligible quests down to the requested density, filling each level bracket with its own quota.

        Quotas are computed after filtering so that races, classes and starting zones cutting unevenly into the
        brackets cannot re-introduce the imbalance the quota is there to avoid.
        """
        available = self.filter_locations(world)
        density = world.options.quests_density.value
        if density >= 100:
            return available

        by_region: dict[str, list[Quest]] = {}
        for quest in available:
            by_region.setdefault(quest.region, []).append(quest)

        picked: list[Quest] = []
        for quests in by_region.values():
            quota = min(len(quests), max(MIN_QUESTS_PER_REGION, math.ceil(len(quests) * density / 100)))
            picked += sorted(world.random.sample(quests, quota), key=lambda q: q.id)

        return picked

    def filter_locations(self, world: "World") -> list[Quest]:
        """Every quest this world could hold a location on, before the density roll."""
        result: list[Quest] = []
        unreachable_quests = self.resolve_unreachable_quests(world)

        for quest in self.quests.values():
            if regions.REGION_LEVELS[quest.region] >= world.level_cap():
                continue

            data = self.quests_json[quest.quest_id]
            if data.is_breadcrumb:
                # Breadcrumbs point at a chain the player can also walk up to, and the game takes them
                # away once they do, so they make unreliable locations. They stay in the table because
                # the chains behind them list them as prerequisites -- which is why this is not one of
                # the `is_blocked` reasons: skipping a breadcrumb must not strip out what it leads to
                continue

            if quest.quest_id in unreachable_quests:
                # Locked to another race or class, or wants a zone, a dungeon, a party or a starting
                # zone the options rule out, or follows on from a quest that does
                continue

            result.append(quest)

        return result

    def get_slot_data(self, world: "World"):
        return [[loc.quest_id, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        locations = self.build_locations(world)
        return [(l.region, l) for l in locations]

    def set_rules(self, world: "World"):
        zones_in_pool = set(ZONES_CONTAINER.build_pool(world))
        for q in self.build_locations(world):
            # A quest lists every zone either faction might use for it, so the list is a superset of what
            # this player needs -- "The Islander" names all six capitals -- and zones outside the pool are
            # dropped rather than treated as requirements. The level rule stands alone because a quest
            # whose only zones are cities still has a level, and its region gates just the bracket floor
            required_zones = [z for z in q.required_zones if z in zones_in_pool]
            level_rule = required_level(q.required_level, world)
            zones_rule = has_all([z.name for z in required_zones], world) if len(required_zones) > 0 else None
            set_rule(world.get_location(q.name), combine_rules(zones_rule, level_rule))


QUESTS_CONTAINER = QuestsContainer()
QUESTS_CONTAINER.load_quests_json()
