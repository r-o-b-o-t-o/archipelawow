from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .data.items.zones import Zone
    from .world import World

from .conditions import has_all
from .data.items import zones
from .data.items.zones import ZONES_CONTAINER
from .options import Goal


def reachable_zone_names(zone_list: list["Zone"], world: "World") -> list[str]:
    """The zones of `zone_list` this world actually puts an item in the pool for.

    A group like AZEROTH names the zones of both factions, while the pool only carries the ones the
    character's own faction can reach. Requiring the whole group would ask for items that were never
    created, leaving the seed unbeatable however it is filled.
    """
    in_pool = set(ZONES_CONTAINER.build_pool(world))
    return [zone.name for zone in zone_list if zone in in_pool]


def set_completion_conditions(world: "World") -> None:
    match world.options.goal.value:
        case Goal.option_classic_dungeonmaster:
            goal_zones = zones.CLASSIC_DUNGEONS

        case Goal.option_level_60:
            goal_zones = zones.AZEROTH

        case Goal.option_outland_dungeonmaster:
            goal_zones = zones.OUTLAND_DUNGEONS

        case Goal.option_level_70:
            goal_zones = zones.OUTLAND

        case Goal.option_northrend_dungeonmaster:
            goal_zones = zones.NORTHREND_DUNGEONS

        case Goal.option_level_80:
            goal_zones = zones.NORTHREND

    world.multiworld.completion_condition[world.player] = has_all(reachable_zone_names(goal_zones, world), world)
