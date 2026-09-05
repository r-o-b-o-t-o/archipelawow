from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .world import World

from BaseClasses import Region
from worlds.generic.Rules import CollectionRule

from .conditions import combine_rules, has_all, required_level_and_zones

LEVELS_01_05 = "Levels 01-05"
LEVELS_05_10 = "Levels 05-10"
LEVELS_10_15 = "Levels 10-15"
LEVELS_15_20 = "Levels 15-20"
LEVELS_20_25 = "Levels 20-25"
LEVELS_25_30 = "Levels 25-30"
LEVELS_30_35 = "Levels 30-35"
LEVELS_35_40 = "Levels 35-40"
LEVELS_40_45 = "Levels 40-45"
LEVELS_45_50 = "Levels 45-50"
LEVELS_50_55 = "Levels 50-55"
LEVELS_55_60 = "Levels 55-60"
LEVELS_60_65 = "Levels 60-65"
LEVELS_65_70 = "Levels 65-70"
LEVELS_70_75 = "Levels 70-75"
LEVELS_75_80 = "Levels 75-80"

CLASSIC_REGIONS = [
    LEVELS_01_05,
    LEVELS_05_10,
    LEVELS_10_15,
    LEVELS_15_20,
    LEVELS_20_25,
    LEVELS_25_30,
    LEVELS_30_35,
    LEVELS_35_40,
    LEVELS_40_45,
    LEVELS_45_50,
    LEVELS_50_55,
    LEVELS_55_60,
]
OUTLAND_REGIONS = [
    LEVELS_60_65,
    LEVELS_65_70,
]
NORTHREND_REGIONS = [
    LEVELS_70_75,
    LEVELS_75_80,
]
ALL_REGIONS = [*CLASSIC_REGIONS, *OUTLAND_REGIONS, *NORTHREND_REGIONS]

REGION_LEVELS = {
    LEVELS_01_05: 0,
    LEVELS_05_10: 5,
    LEVELS_10_15: 10,
    LEVELS_15_20: 15,
    LEVELS_20_25: 20,
    LEVELS_25_30: 25,
    LEVELS_30_35: 30,
    LEVELS_35_40: 35,
    LEVELS_40_45: 40,
    LEVELS_45_50: 45,
    LEVELS_50_55: 50,
    LEVELS_55_60: 55,
    LEVELS_60_65: 60,
    LEVELS_65_70: 65,
    LEVELS_70_75: 70,
    LEVELS_75_80: 75,
}


def create_and_connect_regions(world: "World") -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: "World") -> None:
    world.multiworld.regions += [Region(r, world.player, world.multiworld) for r in ALL_REGIONS]


def connect(r_from: Region, r_to: Region, rule: Optional[CollectionRule] = None):
    r_from.connect(r_to, f"{r_from.name} -> {r_to.name}", rule)


def connect_regions(world: "World") -> None:
    from .items.progressive import PROGRESSIVE_RIDING
    from .items.spells import SPELLS_CONTAINER
    from .items.zones import ZONES_CONTAINER

    zones_in_pool = ZONES_CONTAINER.build_pool(world)
    for i in range(1, len(ALL_REGIONS)):
        r_from = world.get_region(ALL_REGIONS[i - 1])
        r_to = world.get_region(ALL_REGIONS[i])
        level = REGION_LEVELS[r_to.name]
        rule = required_level_and_zones(
            level,
            list(filter(lambda z: z.region_a == r_to.name, zones_in_pool)),
            list(filter(lambda z: z.region_h == r_to.name, zones_in_pool)),
            world,
        )
        # Moving up a bracket also asks for the abilities of the bracket before last, so a character
        # cannot be expected to keep climbing on a kit the multiworld never handed over. The lag is
        # deliberate: asking for the bracket just below would force every one of its spells into its
        # own handful of locations, which leaves the fill nowhere to put them in a lean seed.
        spells = SPELLS_CONTAINER.names_for_region(ALL_REGIONS[i - 2], world) if i >= 2 else []

        # Riding asks for no such lag: a rank is bought the moment its level is reached, so a bracket
        # can expect the ranks it is old enough for. Nothing is asked for where the ladder has no rung
        # left to give, which is what keeps the rule off the last one.
        riding_count = PROGRESSIVE_RIDING.required_count_for_region(r_to.name, world)
        riding_rule = (lambda state, count=riding_count: state.has(PROGRESSIVE_RIDING.name, world.player, count)) \
            if riding_count else None

        connect(r_from, r_to, combine_rules(rule, has_all(spells, world), riding_rule))


def get_region_by_level(level: int):
    for region in reversed(ALL_REGIONS):
        if level > REGION_LEVELS[region]:
            return region

    return LEVELS_01_05
