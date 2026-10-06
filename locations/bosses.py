from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from worlds.generic.Rules import set_rule

from ..boss_model import BOSS_MODELS, BossModel
from ..conditions import combine_rules, has_zone, required_level
from ..items.zones import Zone
from ..options import Dungeonsanity
from . import achievements
from .achievements import Achievement
from .location_container import LocationContainer
from .location_registry import Location


class Boss(Location):
    def __init__(self, data: BossModel, zone: Zone, required_level: int):
        super().__init__(f"Boss: {data.name} ({zone.name})")
        BOSSES_CONTAINER.add(self)
        self.encounter_id = data.id
        self.zone = zone
        self.required_level = required_level


class BossesContainer(LocationContainer[Boss]):
    def build_locations(self, world: "World"):
        locations: list[Boss] = []
        if world.options.classic_dungeonsanity.value == Dungeonsanity.option_all:
            locations += CLASSIC_DUNGEONS
        if world.has_tbc_content() and world.options.outland_dungeonsanity.value == Dungeonsanity.option_all:
            locations += OUTLAND_DUNGEONS
        if world.has_wotlk_content() and world.options.northrend_dungeonsanity.value == Dungeonsanity.option_all:
            locations += NORTHREND_DUNGEONS

        return locations

    def get_slot_data(self, world: "World"):
        return [[loc.encounter_id, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        return [(loc.zone.region(world), loc) for loc in self.build_locations(world)]

    def set_rules(self, world: "World"):
        for boss in self.build_locations(world):
            set_rule(world.get_location(boss.name), combine_rules(has_zone(boss.zone, world), required_level(boss.required_level, world)))


BOSSES_CONTAINER = BossesContainer()


def bosses_of(dungeons: list[Achievement]) -> list[Boss]:
    """The bosses of one bracket's dungeons, which open with the dungeon's achievement: same zone, same level.

    The extract names a boss's dungeon by its map, the one the dungeon's zone teleports into.
    """
    bosses: list[Boss] = []
    for dungeon in dungeons:
        assert dungeon.zone and dungeon.required_level
        bosses += [Boss(data, dungeon.zone, dungeon.required_level) for data in BOSS_MODELS if data.map_id == dungeon.zone.teleport.map]
    return bosses


CLASSIC_DUNGEONS = bosses_of(achievements.CLASSIC_DUNGEONS)
OUTLAND_DUNGEONS = bosses_of(achievements.OUTLAND_DUNGEONS)
NORTHREND_DUNGEONS = bosses_of(achievements.NORTHREND_DUNGEONS)
