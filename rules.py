from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World

from .conditions import has_all
from .data.items import zones
from .options import Goal


def set_completion_conditions(world: "World") -> None:
    match world.options.goal.value:
        case Goal.option_classic_dungeonmaster:
            world.multiworld.completion_condition[world.player] = has_all([i.name for i in zones.CLASSIC_DUNGEONS], world)
        case Goal.option_level_60:
            world.multiworld.completion_condition[world.player] = has_all([z.name for z in zones.AZEROTH], world)
        case Goal.option_outland_dungeonmaster:
            world.multiworld.completion_condition[world.player] = has_all([i.name for i in zones.OUTLAND_DUNGEONS], world)
        case Goal.option_level_70:
            world.multiworld.completion_condition[world.player] = has_all([z.name for z in zones.OUTLAND], world)
        case Goal.option_northrend_dungeonmaster:
            world.multiworld.completion_condition[world.player] = has_all([i.name for i in zones.NORTHREND_DUNGEONS], world)
        case Goal.option_level_80:
            world.multiworld.completion_condition[world.player] = has_all([z.name for z in zones.NORTHREND], world)
