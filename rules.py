from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .items.zones import Zone
    from .world import World

from worlds.generic.Rules import add_item_rule

from . import regions
from .conditions import has_all
from .items import zones
from .items.spells import SPELLS_CONTAINER
from .items.zones import ZONES_CONTAINER
from .options import Goal

# The lowest quest density that still leaves the fill room for the spell placement rule.
#
# The rule narrows where a spell may go, and a seed that has cut its quests to the bone has few
# enough locations already: measured over 50 lean seeds it took the fill from 40/50 down to 36/50,
# against 47/50 either way at the default density. Below this the ceiling stands down rather than
# handing the player failed generations, and the region rules -- which cost the same either way --
# carry the pacing on their own.
PLACEMENT_RULE_MIN_QUEST_DENSITY = 25


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


def set_spell_placement_rules(world: "World") -> None:
    """Keep a spell from being placed so far below its own level that it trivialises the game.

    The other half of the pacing the region rules set up: those say a spell has to be in hand before
    the character climbs much further, this says it may not arrive long before the level it was
    written for. Every region is a level bracket, so the bracket a location sits in is the earliest
    the seed expects the player to reach it, and a spell is refused anywhere too far under the level
    its trainer would ask for.

    Only this world's locations carry the rule -- see PLACEMENT_LEVEL_WINDOW -- so it narrows the
    worst cases rather than ruling them out, and a seed too lean to afford it goes without.
    """
    if world.options.quests_density.value < PLACEMENT_RULE_MIN_QUEST_DENSITY:
        return

    for location in world.multiworld.get_locations(world.player):
        region = location.parent_region
        if region is None or region.name not in regions.REGION_LEVELS:
            continue

        region_level = regions.REGION_LEVELS[region.name]
        add_item_rule(
            location, lambda item, level=region_level: (item.player != world.player or SPELLS_CONTAINER.can_place_at_level(item.name, level, world))
        )
