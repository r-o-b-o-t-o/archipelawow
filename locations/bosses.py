from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from ..boss_model import BOSS_MODELS, BossFaction, BossModel
from ..conditions import has_zone, required_level
from ..items.zones import ZONES_CONTAINER, Zone
from ..options import Dungeonsanity
from . import achievements
from .achievements import Achievement
from .location_container import LocationContainer
from .location_registry import Location


class Boss(Location):
    def __init__(self, data: BossModel, zone: Zone):
        super().__init__(f"Boss: {data.name} ({zone.name})")
        BOSSES_CONTAINER.add(self)
        self.encounter_id = data.id
        self.zone = zone
        self.required_level = data.required_level
        self.faction = data.faction

    def is_fightable(self, world: "World"):
        if self.faction == BossFaction.ALLIANCE:
            return world.is_alliance()
        if self.faction == BossFaction.HORDE:
            return world.is_horde()
        return True


class BossesContainer(LocationContainer[Boss]):
    def build_locations(self, world: "World"):
        locations: list[Boss] = []
        if world.options.classic_dungeonsanity.value == Dungeonsanity.option_all:
            locations += CLASSIC_DUNGEONS
        if world.options.outland_dungeonsanity.value == Dungeonsanity.option_all:
            locations += OUTLAND_DUNGEONS
        if world.options.northrend_dungeonsanity.value == Dungeonsanity.option_all:
            locations += NORTHREND_DUNGEONS

        # The pool already leaves out the dungeons past the seed's level cap
        zones_in_pool = set(ZONES_CONTAINER.build_pool(world))
        return [
            loc for loc in locations if loc.zone in zones_in_pool and loc.required_level <= world.max_location_level() and loc.is_fightable(world)
        ]

    def get_slot_data(self, world: "World"):
        return [[loc.encounter_id, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        return [(loc.zone.region(world), loc) for loc in self.build_locations(world)]

    def set_rules(self, world: "World"):
        for boss in self.build_locations(world):
            world.set_rule(world.get_location(boss.name), has_zone(boss.zone, world) & required_level(boss.required_level))


BOSSES_CONTAINER = BossesContainer()


def bosses_of(dungeons: list[Achievement]) -> list[Boss]:
    """The bosses of one bracket's dungeons, which open with the dungeon's zone, each at its own level.

    The extract names a boss's dungeon by its map, the one the dungeon's zone teleports into.
    """
    bosses: list[Boss] = []
    for dungeon in dungeons:
        assert dungeon.zone
        bosses += [Boss(data, dungeon.zone) for data in BOSS_MODELS if data.map_id == dungeon.zone.teleport.map]
    return bosses


CLASSIC_DUNGEONS = bosses_of(achievements.CLASSIC_DUNGEONS)
OUTLAND_DUNGEONS = bosses_of(achievements.OUTLAND_DUNGEONS)
NORTHREND_DUNGEONS = bosses_of(achievements.NORTHREND_DUNGEONS)
