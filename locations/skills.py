from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from ..world import World

from rule_builder.rules import Has, Or, Rule

from .. import regions
from ..conditions import has_zone, required_level
from ..items.spells import SPELLS_CONTAINER as SPELL_ITEMS_CONTAINER
from ..items.zones import ZONES_CONTAINER, Zone
from ..options import CharacterClass
from ..skill_model import SKILL_MODELS, SkillModel
from ..spell_model import SpellKind
from .location_container import LocationContainer
from .location_registry import Location

# A skill's cap is five times the character's level
SKILL_PER_LEVEL = 5

# SkillLine.dbc
SKILL_BOWS = 45
SKILL_GUNS = 46
SKILL_DEFENSE = 95
SKILL_THROWN = 176
SKILL_CROSSBOWS = 226
SKILL_WANDS = 228
SKILL_POLEARMS = 229

RANGED_SKILLS = {SKILL_BOWS, SKILL_GUNS, SKILL_THROWN, SKILL_CROSSBOWS}

# How many weapon skills a seed picks among those its character can raise, on top of Defense. Each is a grind to its
# cap, and all of them would come to well over a hundred checks for most classes.
PICKED_WEAPON_SKILLS = 3


class Skill(Location):
    """Raising a weapon skill or Defense to its cap at the last level of a bracket."""

    def __init__(self, data: SkillModel, level: int):
        super().__init__(f"Skill: {data.name} {level * SKILL_PER_LEVEL}")
        SKILLS_CONTAINER.add(self)
        self.data = data
        self.level = level
        self.region = regions.get_region_by_level(level)


class SkillsContainer(LocationContainer[Skill]):
    def __init__(self) -> None:
        super().__init__()
        self.all_skills: list[Skill] = []
        # The container is a singleton shared by every player, and the roll must not be re-rolled per caller
        self.__skills_cache: "WeakKeyDictionary[World, dict[int, str | None]]" = WeakKeyDictionary()

    def add(self, location: Skill):
        super().add(location)
        self.all_skills.append(location)

    def skill_items(self, world: "World") -> dict[int, str | None]:
        """The skills that are locations for this world, by id, each with the item teaching it or None for a starting one.

        Rolled once so that every caller sees the same set.
        """
        skills = self.__skills_cache.get(world)
        if skills is None:
            skills = self.pick_skills(world)
            self.__skills_cache[world] = skills

        return skills

    def pick_skills(self, world: "World") -> dict[int, str | None]:
        character_class, race = world.options.character_class.value, world.options.character_race.value
        if character_class in CharacterClass.pure_casters:
            # Every race of these classes is created holding Wands, their one weapon skill raised in normal play
            return {SKILL_WANDS: None}

        items = {item.data.id: item.name for item in SPELL_ITEMS_CONTAINER.build_pool(world) if item.data.kind == SpellKind.WEAPON}
        available: dict[int, str | None] = {}
        zones_in_pool = ZONES_CONTAINER.build_pool(world)
        last_tier_level = world.max_location_level() - world.max_location_level() % 5
        for skill in SKILL_MODELS:
            # Before Outland, only Stormwind and Undercity sell a polearm, from level 20: too rare a weapon to send a seed looking for
            if skill.id == SKILL_POLEARMS:
                continue
            if character_class in CharacterClass.melee_only and skill.id in RANGED_SKILLS:
                continue
            # A pick with no tier left would be a wasted one. A weapon on sale by one tier stays on sale for the later ones.
            if not self.is_raisable(skill, last_tier_level, zones_in_pool, world):
                continue
            if skill.is_starting_skill_of(character_class, race):
                available[skill.id] = None
            elif skill.spell in items:
                available[skill.id] = items[skill.spell]

        # Bear and cat form raise Defense but no weapon skill
        count = 0 if character_class == CharacterClass.option_druid else PICKED_WEAPON_SKILLS
        weapons = [skill_id for skill_id in available if skill_id != SKILL_DEFENSE]
        picked = set(world.random.sample(weapons, min(count, len(weapons))))
        return {skill_id: item for skill_id, item in available.items() if skill_id == SKILL_DEFENSE or skill_id in picked}

    def vendor_zones(self, skill: SkillModel, level: int, zones_in_pool: list[Zone], world: "World") -> list[Zone] | None:
        """The zones of this seed selling a weapon of the skill that the character can buy and equip by `level`.

        None for Defense, which takes no weapon. Raising a weapon skill takes a weapon of its kind, and only the
        zones of the pool count, as for the trainers of locations/spells.py. The starting zones sell every melee
        weapon but fist weapons, while the ranged ones are patchy, and before Outland fist weapons and wands are only
        sold in some capitals.
        """
        if skill.spell == 0:
            return None

        zone_ids = skill.zones_selling(world.options.character_race.value, level)
        return [zone for zone in zones_in_pool if zone.zone_id in zone_ids]

    def is_raisable(self, skill: SkillModel, level: int, zones_in_pool: list[Zone], world: "World") -> bool:
        """Whether a tier of the skill at `level` can be asked for: Defense's always can, a weapon skill's once a zone sells its weapon."""
        return self.vendor_zones(skill, level, zones_in_pool, world) != []

    def build_locations(self, world: "World") -> list[Skill]:
        skills = self.skill_items(world)
        zones_in_pool = ZONES_CONTAINER.build_pool(world)
        # Fist weapons are sold from level 10 and wands from 15, so their first tiers go
        return [
            loc
            for loc in self.all_skills
            if loc.data.id in skills and loc.level <= world.max_location_level() and self.is_raisable(loc.data, loc.level, zones_in_pool, world)
        ]

    def get_slot_data(self, world: "World"):
        return [[loc.data.id, loc.level * SKILL_PER_LEVEL, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        return [(loc.region, loc) for loc in self.build_locations(world)]

    def set_rules(self, world: "World"):
        skills = self.skill_items(world)
        zones_in_pool = ZONES_CONTAINER.build_pool(world)
        starting_zones = ZONES_CONTAINER.get_precollected_items(world)
        for loc in self.build_locations(world):
            rule: Rule = required_level(loc.level)
            item = skills[loc.data.id]
            if item is not None:
                rule &= Has(item)

            zones = self.vendor_zones(loc.data, loc.level, zones_in_pool, world)
            if zones and not any(zone in starting_zones for zone in zones):
                rule &= Or(*[has_zone(zone, world) for zone in zones])
            world.set_rule(world.get_location(loc.name), rule)


SKILLS_CONTAINER = SkillsContainer()

for skill in SKILL_MODELS:
    # The last level of each bracket
    for level in range(5, 81, 5):
        Skill(skill, level)
