from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from ... import regions
from .location_container import LocationContainer
from .location_registry import Location


class Level(Location):
    def __init__(self, level: int, region: str):
        super().__init__("Level {:02d}".format(level))
        LEVELS_CONTAINER.add(self)
        self.level = level
        self.region = region


class LevelsContainer(LocationContainer):
    def __init__(self) -> None:
        super().__init__()
        self.all_levels: list[Level] = []

    def add(self, location: Level):
        super().add(location)
        self.all_levels.append(location)

    def build_locations(self, world: "World"):
        return list(filter(lambda loc: loc.level <= world.level_cap(), self.all_levels))

    def get_slot_data(self, world: "World"):
        return [[loc.level, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        locations = self.build_locations(world)
        return [(l.region, l) for l in locations]


LEVELS_CONTAINER = LevelsContainer()

LEVEL_02 = Level(2, regions.LEVELS_01_10)
LEVEL_03 = Level(3, regions.LEVELS_01_10)
LEVEL_04 = Level(4, regions.LEVELS_01_10)
LEVEL_05 = Level(5, regions.LEVELS_01_10)
LEVEL_06 = Level(6, regions.LEVELS_01_10)
LEVEL_07 = Level(7, regions.LEVELS_01_10)
LEVEL_08 = Level(8, regions.LEVELS_01_10)
LEVEL_09 = Level(9, regions.LEVELS_01_10)
LEVEL_10 = Level(10, regions.LEVELS_01_10)
LEVEL_11 = Level(11, regions.LEVELS_10_15)
LEVEL_12 = Level(12, regions.LEVELS_10_15)
LEVEL_13 = Level(13, regions.LEVELS_10_15)
LEVEL_14 = Level(14, regions.LEVELS_10_15)
LEVEL_15 = Level(15, regions.LEVELS_10_15)
LEVEL_16 = Level(16, regions.LEVELS_15_20)
LEVEL_17 = Level(17, regions.LEVELS_15_20)
LEVEL_18 = Level(18, regions.LEVELS_15_20)
LEVEL_19 = Level(19, regions.LEVELS_15_20)
LEVEL_20 = Level(20, regions.LEVELS_15_20)
LEVEL_21 = Level(21, regions.LEVELS_20_25)
LEVEL_22 = Level(22, regions.LEVELS_20_25)
LEVEL_23 = Level(23, regions.LEVELS_20_25)
LEVEL_24 = Level(24, regions.LEVELS_20_25)
LEVEL_25 = Level(25, regions.LEVELS_20_25)
LEVEL_26 = Level(26, regions.LEVELS_25_30)
LEVEL_27 = Level(27, regions.LEVELS_25_30)
LEVEL_28 = Level(28, regions.LEVELS_25_30)
LEVEL_29 = Level(29, regions.LEVELS_25_30)
LEVEL_30 = Level(30, regions.LEVELS_25_30)
LEVEL_31 = Level(31, regions.LEVELS_30_35)
LEVEL_32 = Level(32, regions.LEVELS_30_35)
LEVEL_33 = Level(33, regions.LEVELS_30_35)
LEVEL_34 = Level(34, regions.LEVELS_30_35)
LEVEL_35 = Level(35, regions.LEVELS_30_35)
LEVEL_36 = Level(36, regions.LEVELS_35_40)
LEVEL_37 = Level(37, regions.LEVELS_35_40)
LEVEL_38 = Level(38, regions.LEVELS_35_40)
LEVEL_39 = Level(39, regions.LEVELS_35_40)
LEVEL_40 = Level(40, regions.LEVELS_35_40)
LEVEL_41 = Level(41, regions.LEVELS_40_45)
LEVEL_42 = Level(42, regions.LEVELS_40_45)
LEVEL_43 = Level(43, regions.LEVELS_40_45)
LEVEL_44 = Level(44, regions.LEVELS_40_45)
LEVEL_45 = Level(45, regions.LEVELS_40_45)
LEVEL_46 = Level(46, regions.LEVELS_45_50)
LEVEL_47 = Level(47, regions.LEVELS_45_50)
LEVEL_48 = Level(48, regions.LEVELS_45_50)
LEVEL_49 = Level(49, regions.LEVELS_45_50)
LEVEL_50 = Level(50, regions.LEVELS_45_50)
LEVEL_51 = Level(51, regions.LEVELS_50_55)
LEVEL_52 = Level(52, regions.LEVELS_50_55)
LEVEL_53 = Level(53, regions.LEVELS_50_55)
LEVEL_54 = Level(54, regions.LEVELS_50_55)
LEVEL_55 = Level(55, regions.LEVELS_50_55)
LEVEL_56 = Level(56, regions.LEVELS_55_60)
LEVEL_57 = Level(57, regions.LEVELS_55_60)
LEVEL_58 = Level(58, regions.LEVELS_55_60)
LEVEL_59 = Level(59, regions.LEVELS_55_60)
LEVEL_60 = Level(60, regions.LEVELS_55_60)
LEVEL_61 = Level(61, regions.OUTLAND)
LEVEL_62 = Level(62, regions.OUTLAND)
LEVEL_63 = Level(63, regions.OUTLAND)
LEVEL_64 = Level(64, regions.OUTLAND)
LEVEL_65 = Level(65, regions.OUTLAND)
LEVEL_66 = Level(66, regions.OUTLAND)
LEVEL_67 = Level(67, regions.OUTLAND)
LEVEL_68 = Level(68, regions.OUTLAND)
LEVEL_69 = Level(69, regions.OUTLAND)
LEVEL_70 = Level(70, regions.OUTLAND)
LEVEL_71 = Level(71, regions.NORTHREND)
LEVEL_72 = Level(72, regions.NORTHREND)
LEVEL_73 = Level(73, regions.NORTHREND)
LEVEL_74 = Level(74, regions.NORTHREND)
LEVEL_75 = Level(75, regions.NORTHREND)
LEVEL_76 = Level(76, regions.NORTHREND)
LEVEL_77 = Level(77, regions.NORTHREND)
LEVEL_78 = Level(78, regions.NORTHREND)
LEVEL_79 = Level(79, regions.NORTHREND)
LEVEL_80 = Level(80, regions.NORTHREND)
