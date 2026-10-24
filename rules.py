from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .items.zones import Zone
    from .locations.achievements import Achievement
    from .world import World

from rule_builder.rules import HasAll, Rule
from worlds.generic.Rules import add_item_rule

from . import regions
from .conditions import required_level
from .items import zones
from .items.spells import SPELLS_CONTAINER
from .items.zones import ZONES_CONTAINER
from .locations import achievements
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
    goal_zones: list[Zone] = []
    goal_dungeons: list[Achievement] = []

    match world.options.goal.value:
        case Goal.option_classic_dungeonmaster:
            goal_zones = zones.CLASSIC_DUNGEONS
            goal_dungeons = achievements.CLASSIC_DUNGEONS

        case Goal.option_level_10 | Goal.option_level_20 | Goal.option_level_30 | Goal.option_level_40 | Goal.option_level_50 | Goal.option_level_60:
            # Only the zones opening below the cap are in the pool
            goal_zones = zones.AZEROTH

        case Goal.option_outland_dungeonmaster:
            goal_zones = zones.OUTLAND_DUNGEONS
            goal_dungeons = achievements.OUTLAND_DUNGEONS

        case Goal.option_level_70:
            goal_zones = zones.OUTLAND

        case Goal.option_northrend_dungeonmaster:
            goal_zones = zones.NORTHREND_DUNGEONS
            goal_dungeons = achievements.NORTHREND_DUNGEONS

        case Goal.option_level_80:
            goal_zones = zones.NORTHREND

    zone_names = reachable_zone_names(goal_zones, world)
    rule: Rule = HasAll(*zone_names)
    # Holding the zones is not the goal itself: the module counts a level goal once the character reaches the cap, and a
    # dungeonmaster goal once every dungeon is cleared, which takes the level the hardest one's achievement asks for
    if world.options.goal.value in Goal.level_goals:
        rule &= required_level(world.level_cap())
    else:
        rule &= required_level(max(d.required_level or 0 for d in goal_dungeons if d.zone and d.zone.name in zone_names))
    world.set_completion_rule(rule)


def set_spell_placement_rules(world: "World") -> None:
    """Keep a spell from being placed so far below its own level that it trivialises the game.

    The other half of the pacing the region rules set up: those say a spell has to be in hand before
    the character climbs much further, this says it may not arrive long before the level it was
    written for. Every region is a level bracket, so the bracket a location sits in is the earliest
    the seed expects the player to reach it, and a spell is refused anywhere too far under the level
    its trainer would ask for.

    Only this world's locations carry the rule -- see PLACEMENT_LEVEL_WINDOW -- so it narrows the
    worst cases rather than ruling them out. It costs the fill nothing measurable, lean seeds included:
    over 2,850 solo seeds of 160 to 930 locations, each filled with and without it, about as many failed
    either way.
    """
    for location in world.multiworld.get_locations(world.player):
        region = location.parent_region
        if region is None or region.name not in regions.REGION_LEVELS:
            continue

        region_level = regions.REGION_LEVELS[region.name]
        add_item_rule(
            location, lambda item, level=region_level: (item.player != world.player or SPELLS_CONTAINER.can_place_at_level(item.name, level, world))
        )
