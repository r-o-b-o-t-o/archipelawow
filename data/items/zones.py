from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from BaseClasses import ItemClassification

from ... import regions
from .item_container import ItemContainer
from .item_registry import Item


class Side(IntEnum):
    CONTESTED = 1
    ALLIANCE = 2
    HORDE = 3


class ZonesContainer(ItemContainer):
    def build_pool(self, world: "World"):
        zones: list[Zone] = []
        zones += AZEROTH
        zones += CLASSIC_DUNGEONS

        if world.has_tbc_content():
            zones += OUTLAND
            zones += OUTLAND_DUNGEONS

        if world.has_wotlk_content():
            zones += NORTHREND
            zones += NORTHREND_DUNGEONS

        zones = list(
            filter(
                lambda z: z.side == Side.CONTESTED
                or (z.side == Side.ALLIANCE and world.is_alliance())
                or (z.side == Side.HORDE and world.is_horde()),
                zones,
            )
        )
        return zones

    def get_slot_data(self, world: "World"):
        return [[item.id, item.zone_id, item.icon, item.gossip_menu, item.teleport.to_list()] for item in self.build_pool(world)]

    def get_items_for_pool(self, world: "World") -> list[Item]:
        return list(self.build_pool(world))

    def get_precollected_items(self, world: "World") -> list[Item]:
        precollected: list[Zone] = []
        if world.is_alliance():
            precollected += [z for z in [ELWYNN_FOREST, DUN_MOROGH, TELDRASSIL, AZUREMYST_ISLE]]
        else:
            precollected += [z for z in [DUROTAR, MULGORE, TIRISFAL_GLADES, EVERSONG_WOODS]]

        return list(precollected)


class Teleport:
    def __init__(self, map: int, x: float, y: float, z: float, o: float = 0.0):
        self.map = map
        self.x = x
        self.y = y
        self.z = z
        self.o = o

    def to_list(self):
        return [self.map, self.x, self.y, self.z, self.o]


class Zone(Item):
    def __init__(self, name: str, icon: str, zone_id: int, region_a: str, region_h: str, teleport: Teleport, side=Side.CONTESTED):
        super().__init__(name, ItemClassification.progression)
        ZONES_CONTAINER.add(self)
        if icon.lower().startswith("zone") or icon.lower().startswith("boss") or icon.lower().startswith("dungeon"):
            self.icon = f"Icons/Achievement_{icon}"
        else:
            self.icon = f"Icons/{icon}"
        self.zone_id = zone_id
        self.region_a = region_a
        self.region_h = region_h
        self.teleport = teleport
        self.side = side
        self.gossip_menu = 0


ZONES_CONTAINER = ZonesContainer()

L01 = regions.LEVELS_01_10
L10 = regions.LEVELS_10_15
L15 = regions.LEVELS_15_20
L20 = regions.LEVELS_20_25
L25 = regions.LEVELS_25_30
L30 = regions.LEVELS_30_35
L35 = regions.LEVELS_35_40
L40 = regions.LEVELS_40_45
L45 = regions.LEVELS_45_50
L50 = regions.LEVELS_50_55
L55 = regions.LEVELS_55_60
OL = regions.OUTLAND
NR = regions.NORTHREND
A = Side.ALLIANCE
H = Side.HORDE
TP = Teleport


# Eastern Kingdoms
ARATHI_HIGHLANDS = Zone("Arathi Highlands", "Zone_ArathiHighlands_01", 45, L35, L30, TP(0, -1254, -1850, 106, 2.95))
BADLANDS = Zone("Badlands", "Zone_Badlands_01", 3, L35, L35, TP(0, -6173, -3339, 289, 3.65))
BLASTED_LANDS = Zone("Blasted Lands", "Zone_BlastedLands_01", 4, L45, L45, TP(0, -10845, -2840, 77, 3.65))
BURNING_STEPPES = Zone("Burning Steppes", "Zone_BurningSteppes_01", 46, L55, L55, TP(0, -8112.79, -2281.76, 220.73, 5.35))
DUN_MOROGH = Zone("Dun Morogh", "Zone_DunMorogh", 1, L01, "", TP(0, -6240, 331, 383, 0), A)
DUSKWOOD = Zone("Duskwood", "Zone_Duskwood", 10, L20, "", TP(0, -10864.93, 599.2, 31.35, 4.78), A)
EASTERN_PLAGUELANDS = Zone("Eastern Plaguelands", "Zone_EasternPlaguelands", 139, L55, L55, TP(0, 1924.59, -2632.02, 60.87, 4.72))
ELWYNN_FOREST = Zone("Elwynn Forest", "Zone_ElwynnForest", 12, L01, "", TP(0, -8950, -132.5, 84.5, 0.2), A)
EVERSONG_WOODS = Zone("Eversong Woods", "Zone_EversongWoods", 3430, "", L01, TP(530, 10349.6, -6357.29, 33.41, 5.32), H)
GHOSTLANDS = Zone("Ghostlands", "Zone_Ghostlands", 3433, "", L10, TP(530, 7995.21, -6879.2, 59.12, 2.98), H)
HILLSBRAD_FOOTHILLS = Zone("Hillsbrad Foothills", "Zone_HillsbradFoothills", 267, L30, L20, TP(0, -498.81, -1183.35, 80.37, 2.18))
LOCH_MODAN = Zone("Loch Modan", "Zone_LochModan", 38, L10, "", TP(0, -5634.49, -2525.38, 376.98, 4), A)
REDRIDGE_MOUNTAINS = Zone("Redridge Mountains", "Zone_RedridgeMountains", 44, L15, "", TP(0, -9619.71, -1774.12, 52.81, 4.76), A)
SEARING_GORGE = Zone("Searing Gorge", "Zone_SearingGorge_01", 51, L45, L45, TP(0, -6812.25, -1714.05, 277.11, 1.65))
SILVERPINE_FOREST = Zone("Silverpine Forest", "Zone_Silverpine_01", 130, "", L10, TP(0, 1462.47, 662.02, 46.47, 2.13), H)
STRANGLETHORN_VALE = Zone("Stranglethorn Vale", "Zone_Stranglethorn_01", 33, L30, L30, TP(0, -11965.1, -89.99, 31.56, 5.1))
SWAMP_OF_SORROWS = Zone("Swamp of Sorrows", "Zone_SwampSorrows_01", 8, "", L35, TP(0, -10515.52, -2377, 80.42, 5.79), H)
THE_HINTERLANDS = Zone("The Hinterlands", "Zone_Hinterlands_01", 47, L40, L45, TP(0, 45.39, -1953.78, 155.99, 5.98))
TIRISFAL_GLADES = Zone("Tirisfal Glades", "Zone_TirisfalGlades_01", 85, "", L01, TP(0, 1676.71, 1678.31, 121.68, 3.14), H)
WESTERN_PLAGUELANDS = Zone("Western Plaguelands", "Zone_WesternPlaguelands_01", 28, L50, L50, TP(0, 1631.83, -1393.31, 67.51, 3.58))
WESTFALL = Zone("Westfall", "Zone_WestFall_01", 40, L10, "", TP(0, -9817.96, 852.6, 26.96, 2.15), A)
WETLANDS = Zone("Wetlands", "Zone_Wetlands_01", 11, L20, "", TP(0, -4469.739, -2690.02, 266.04, 0.76), A)
EASTERN_KINGDOMS = [
    ARATHI_HIGHLANDS,
    BADLANDS,
    BLASTED_LANDS,
    BURNING_STEPPES,
    DUN_MOROGH,
    DUSKWOOD,
    EASTERN_PLAGUELANDS,
    ELWYNN_FOREST,
    EVERSONG_WOODS,
    GHOSTLANDS,
    HILLSBRAD_FOOTHILLS,
    LOCH_MODAN,
    REDRIDGE_MOUNTAINS,
    SEARING_GORGE,
    SILVERPINE_FOREST,
    STRANGLETHORN_VALE,
    SWAMP_OF_SORROWS,
    THE_HINTERLANDS,
    TIRISFAL_GLADES,
    WESTERN_PLAGUELANDS,
    WESTFALL,
    WETLANDS,
]

# Kalimdor
ASHENVALE = Zone("Ashenvale", "Zone_Ashenvale_01", 331, L20, L20, TP(1, 2361.25, -1568.67, 125.29, 4.5))
AZSHARA = Zone("Azshara", "Zone_Azshara_01", 16, L45, L45, TP(1, 2805.87, -3806.56, 86.04, 4.07))
AZUREMYST_ISLE = Zone("Azuremyst Isle", "Zone_AzuremystIsle_01", 3524, L01, "", TP(530, -3961.6, -13931.2, 101, 2.1), A)
BLOODMYST_ISLE = Zone("Bloodmyst Isle", "Zone_BloodmystIsle_01", 3525, L10, "", TP(530, -2794, -12209.33, 16.31, 0.05), A)
DARKSHORE = Zone("Darkshore", "Zone_Darkshore_01", 148, L10, "", TP(1, 6452.3, 657.38, 9.91, 4.39), A)
DESOLACE = Zone("Desolace", "Zone_Desolace", 405, L30, L30, TP(1, 275.81, 1834.67, 86.12, 3.44))
DUROTAR = Zone("Durotar", "Zone_Durotar", 14, "", L01, TP(1, -618.52, -4251.67, 38.72, 0), H)
DUSTWALLOW_MARSH = Zone("Dustwallow Marsh", "Zone_DustwallowMarsh", 15, L35, L40, TP(1, -3040.83, -3098.25, 65.06, 4.28))
FELWOOD = Zone("Felwood", "Zone_Felwood", 361, L50, L50, TP(1, 3589.11, -1516.15, 169.88, 0.13))
FERALAS = Zone("Feralas", "Zone_Feralas", 357, L40, L40, TP(1, -4273.42, -713.23, -26.89, 1.55))
MULGORE = Zone("Mulgore", "Zone_Mulgore_01", 215, "", L01, TP(1, -2917.58, -257.98, 53, 0), H)
SILITHUS = Zone("Silithus", "Zone_Silithus_01", 1377, L55, L55, TP(1, -6309.21, -357.35, -1.02, 2.21))
STONETALON_MOUNTAINS = Zone("Stonetalon Mountains", "Zone_Stonetalon_01", 406, L20, L20, TP(1, -217.57, -744, 4.63, 1))
TANARIS = Zone("Tanaris", "Zone_Tanaris_01", 440, L45, L45, TP(1, -6853.43, -3754.62, 36.03, 3.16))
TELDRASSIL = Zone("Teldrassil", "Zone_Darnassus", 141, L01, "", TP(1, 10311.3, 832.5, 1327, 5.7), A)
THE_BARRENS = Zone("The Barrens", "Zone_Barrens_01", 17, "", L10, TP(1, 315.04, -3742.17, 35.11, 1.62), H)
THOUSAND_NEEDLES = Zone("Thousand Needles", "Zone_ThousandNeedles_01", 400, L25, L25, TP(1, -4586.42, -1858.81, 86.2, 2.91))
UNGORO_CRATER = Zone("Un'Goro Crater", "Zone_UnGoroCrater_01", 490, L50, L50, TP(1, -7944.5, -2119.57, -218.12, 0.41))
WINTERSPRING = Zone("Winterspring", "Zone_Winterspring", 618, L55, L55, TP(1, 6892.34, -2302.42, 585.38, 3.5))
KALIMDOR = [
    ASHENVALE,
    AZSHARA,
    AZUREMYST_ISLE,
    BLOODMYST_ISLE,
    DARKSHORE,
    DESOLACE,
    DUROTAR,
    DUSTWALLOW_MARSH,
    FELWOOD,
    FERALAS,
    MULGORE,
    SILITHUS,
    STONETALON_MOUNTAINS,
    TANARIS,
    TELDRASSIL,
    THE_BARRENS,
    THOUSAND_NEEDLES,
    UNGORO_CRATER,
    WINTERSPRING,
]

# Outland
BLADES_EDGE_MOUNTAINS = Zone("Blade's Edge Mountains", "Zone_BladesEdgeMtns_01", 3522, OL, OL, TP(530, 1066.78, 7095.34, 117.9, 6.05))
HELLFIRE_PENINSULA = Zone("Hellfire Peninsula", "Zone_HellfirePeninsula_01", 3483, OL, OL, TP(530, -248.15, 921.88, 84.39, 1.57))
NAGRAND = Zone("Nagrand", "Zone_Nagrand_01", 3518, OL, OL, TP(530, -1226.59, 6220.22, 58.53, 2.56))
NETHERSTORM = Zone("Netherstorm", "Zone_Netherstorm_01", 3523, OL, OL, TP(530, 3374.05, 4332.54, 122.65, 4.82))
SHADOWMOON_VALLEY = Zone("Shadowmoon Valley", "Zone_Shadowmoon", 3520, OL, OL, TP(530, -2822.06, 3225.49, 10.93, 4))
TEROKKAR_FOREST = Zone("Terokkar Forest", "Zone_Terrokar", 3519, OL, OL, TP(530, -1219.57, 5298.67, 36.03, 3.86))
ZANGARMARSH = Zone("Zangarmarsh", "Zone_Zangarmarsh", 3521, OL, OL, TP(530, -232.09, 5331.92, 25.55, 1.32))

# Northrend
BOREAN_TUNDRA = Zone("Borean Tundra", "Zone_BoreanTundra_01", 3537, NR, NR, TP(571, 2380.61, 5699.21, 75.45, 4.41))
DRAGONBLIGHT = Zone("Dragonblight", "Zone_DragonBlight_02", 65, NR, NR, TP(571, 3528.04, 3127.36, 21, 4.82))
GRIZZLY_HILLS = Zone("Grizzly Hills", "Zone_GrizzlyHills_01", 394, NR, NR, TP(571, 3180.80, -1622.80, 39, 4.72))
HOWLING_FJORD = Zone("Howling Fjord", "Zone_HowlingFjord_01", 495, NR, NR, TP(571, 1033.55, -4683.43, 198.42, 4.88))
ICECROWN = Zone("Icecrown", "Zone_IceCrown_01", 210, NR, NR, TP(571, 6048.83, -133.33, 330.7, 0.71))
SHOLAZAR_BASIN = Zone("Sholazar Basin", "Zone_Sholazar_01", 3711, NR, NR, TP(571, 4766.95, 5549.36, -11.43, 6))
THE_STORM_PEAKS = Zone("The Storm Peaks", "Zone_StormPeaks_03", 67, NR, NR, TP(571, 5987.38, -513.54, 341.73, 5.7))
ZULDRAK = Zone("Zul'Drak", "Zone_ZulDrak_02", 66, NR, NR, TP(571, 4825.15, -1495.77, 248.51, 5.54))

# Classic Dungeons
BLACKFATHOM_DEEPS = Zone("Blackfathom Deeps", "Boss_Bazil_Akumai", 719, L20, L20, TP(48, -151.9, 107, -38.8, 4.53))
BLACKROCK_DEPTHS = Zone("Blackrock Depths", "Boss_EmperorDagranThaurissan", 1584, L50, L50, TP(230, 458.3, 26.5, -69.7, 4.95))
BLACKROCK_SPIRE = Zone("Blackrock Spire", "Boss_Overlord_Wyrmthalak", 1583, L55, L55, TP(229, 78.2, -225, 50.8, 4.73))
DIRE_MAUL = Zone("Dire Maul", "Ability_Warrior_DecisiveStrike", 2557, L55, L55, TP(429, 255.2, -16.1, -1.6, 4.7))
GNOMEREGAN = Zone("Gnomeregan", "Boss_Mekgineer_Thermaplugg ", 721, L25, L25, TP(90, -332.2, -2.3, -151.8, 2.77))
MARAUDON = Zone("Maraudon", "Boss_PrincessTheradras", 2100, L40, L40, TP(349, 752.9, -616.5, -32.1, 1.37))
RAGEFIRE_CHASM = Zone("Ragefire Chasm", "Spell_Shadow_SummonFelGuard", 2437, L10, L10, TP(389, 3.81, -14.8, -16.8, 4.39))
RAZORFEN_DOWNS = Zone("Razorfen Downs", "Boss_Amnennar_the_Coldbringer", 722, L35, L35, TP(129, 2592.6, 1107.5, 52.29, 4.74))
RAZORFEN_KRAUL = Zone("Razorfen Kraul", "Boss_CharlgaRazorflank", 491, L25, L25, TP(47, 1943, 1544.63, 83, 1.38))
SCARLET_MONASTERY = Zone("Scarlet Monastery", "INV_Helmet_52", 796, L30, L30, TP(189, 1689, 1053.5, 19.68, 0))
SCHOLOMANCE = Zone("Scholomance", "Spell_Holy_SenseUndead", 2057, L55, L55, TP(289, 196.37, 127.05, 135.91, 6.09))
SHADOWFANG_KEEP = Zone("Shadowfang Keep", "Boss_ArchmageArugal", 209, L15, L15, TP(33, -228.24, 2111.87, 77.9, 5.92))
STRATHOLME = Zone("Stratholme", "Spell_DeathKnight_ArmyOfTheDead", 2017, L55, L55, TP(329, 3395.1, -3380.25, 143.7, 0))
SUNKEN_TEMPLE = Zone("Sunken Temple", "Boss_ShadeOfEranikus", 1417, L45, L45, TP(109, -319.2, 100, -130.8, 3.19))
THE_DEADMINES = Zone("The Deadmines", "Boss_EdwinVancleef", 1581, L15, L15, TP(36, -16.4, -383.1, 62.78, 1.86))
THE_STOCKADE = Zone("The Stockade", "Boss_Bazil_Thredd", 717, L20, L20, TP(34, 54.2, 0.68, -17.3, 0))
ULDAMAN = Zone("Uldaman", "Boss_Archaedas", 1337, L35, L35, TP(70, -226.8, 49.1, -45, 1.39))
WAILING_CAVERNS = Zone("Wailing Caverns", "Boss_Mutanus_the_Devourer", 718, L15, L15, TP(43, -163.5, 132.9, -72.7, 5.83))
ZULFARRAK = Zone("Zul'Farrak", "Boss_ChiefUkorzSandscalp", 1176, L40, L40, TP(209, 1215.59, 841.36, 10.82, 6.14))
CLASSIC_DUNGEONS = [
    BLACKFATHOM_DEEPS,
    BLACKROCK_DEPTHS,
    BLACKROCK_SPIRE,
    DIRE_MAUL,
    GNOMEREGAN,
    MARAUDON,
    RAGEFIRE_CHASM,
    RAZORFEN_DOWNS,
    RAZORFEN_KRAUL,
    SCARLET_MONASTERY,
    SCHOLOMANCE,
    SHADOWFANG_KEEP,
    STRATHOLME,
    SUNKEN_TEMPLE,
    THE_DEADMINES,
    THE_STOCKADE,
    ULDAMAN,
    WAILING_CAVERNS,
    ZULFARRAK,
]
AZEROTH = [*EASTERN_KINGDOMS, *KALIMDOR]

# Outland Dungeons
AUCHENAI_CRYPTS = Zone("Auchenai Crypts", "Boss_Exarch_Maladaar", 3790, OL, OL, TP(558, -20.62, 0.14, -0.11, 0))
HELLFIRE_RAMPARTS = Zone("Hellfire Ramparts", "Boss_OmarTheUnscarred_01", 3562, OL, OL, TP(543, -1355.24, 1641.12, 68.26, 0.67))
MAGISTERS_TERRACE = Zone("Magisters' Terrace", "Boss_Kael'thasSunstrider_01", 4131, OL, OL, TP(585, 7.09, -0.45, -2.7, 0))
MANA_TOMBS = Zone("Mana-Tombs", "Boss_Nexus_Prince_Shaffar", 3792, OL, OL, TP(557, -2.21, 0.95, -0.94, 3.14))
OLD_HILLSBRAD_FOOTHILLS = Zone("Old Hillsbrad Foothills", "Boss_EpochHunter", 2367, OL, OL, TP(560, 2741.87, 1315.25, 14.03, 2.96))
SETHEKK_HALLS = Zone("Sethekk Halls", "Boss_TalonKingIkiss", 3791, OL, OL, TP(556, -4.68, -0.09, 0.01, 0))
SHADOW_LABYRINTH = Zone("Shadow Labyrinth", "Boss_Murmur_01", 3789, OL, OL, TP(555, -0.19, -0.21, -1.11, 3.14))
THE_ARCATRAZ = Zone("The Arcatraz", "Boss_Harbinger_Skyriss", 3848, OL, OL, TP(552, -1.23, 0.01, -0.19, 0))
THE_BLACK_MORASS = Zone("The Black Morass", "Boss_Aeonus_01", 2366, OL, OL, TP(269, -1496.24, 7034.7, 32.55, 1.76))
THE_BLOOD_FURNACE = Zone("The Blood Furnace", "Boss_KelidanTheBreaker", 3713, OL, OL, TP(542, -4, 14.64, -44.7, 4.89))
THE_BOTANICA = Zone("The Botanica", "Boss_WarpSplinter", 3847, OL, OL, TP(553, 40.04, -28.6, -1.10, 2.36))
THE_MECHANAR = Zone("The Mechanar", "Boss_PathaleonTheCalculator", 3849, OL, OL, TP(554, -28.91, 0.68, -1.80, 0))
THE_SHATTERED_HALLS = Zone("The Shattered Halls", "Boss_KargathBladefist_01", 3714, OL, OL, TP(540, -40.87, -19.75, -13.79, 1.11))
THE_SLAVE_PENS = Zone("The Slave Pens", "Boss_Quagmirran", 3717, OL, OL, TP(547, 120.1, -131.96, -0.79, 1.48))
THE_STEAMVAULT = Zone("The Steamvault", "Boss_Warlord_Kalithresh", 3715, OL, OL, TP(545, -13.84, 6.75, -4.24, 0))
THE_UNDERBOG = Zone("The Underbog", "Boss_theBlackStalker", 3716, OL, OL, TP(546, 16.27, -22.44, -2.74, 5.78))
OUTLAND_DUNGEONS = [
    AUCHENAI_CRYPTS,
    HELLFIRE_RAMPARTS,
    MAGISTERS_TERRACE,
    MANA_TOMBS,
    OLD_HILLSBRAD_FOOTHILLS,
    SETHEKK_HALLS,
    SHADOW_LABYRINTH,
    THE_ARCATRAZ,
    THE_BLACK_MORASS,
    THE_BLOOD_FURNACE,
    THE_BOTANICA,
    THE_MECHANAR,
    THE_SHATTERED_HALLS,
    THE_SLAVE_PENS,
    THE_STEAMVAULT,
    THE_UNDERBOG,
]
OUTLAND = [
    BLADES_EDGE_MOUNTAINS,
    HELLFIRE_PENINSULA,
    NAGRAND,
    NETHERSTORM,
    SHADOWMOON_VALLEY,
    TEROKKAR_FOREST,
    ZANGARMARSH,
]

# Northrend Dungeons
AHNKAHET_THE_OLD_KINGDOM = Zone("Ahn'kahet: The Old Kingdom", "Dungeon_AzjolLowercity_Normal", 4494, NR, NR, TP(619, 340.76, -1105.37, 63.03, 0.55))
AZJOL_NERUB = Zone("Azjol-Nerub", "Dungeon_AzjolUppercity_Normal", 4277, NR, NR, TP(601, 413.31, 795.97, 831.36, 5.5))
DRAKTHARON_KEEP = Zone("Drak'Tharon Keep", "Dungeon_Drak'Tharon_Normal", 4196, NR, NR, TP(600, -517.34, -487.98, 11, 4.83))
GUNDRAK = Zone("Gundrak", "Dungeon_Gundrak_Normal", 4416, NR, NR, TP(604, 1891.84, 832.17, 176.67, 2.1))
HALLS_OF_LIGHTNING = Zone("Halls of Lightning", "Dungeon_Ulduar80_Normal", 4272, NR, NR, TP(602, 1331.47, 259.62, 53.4, 4.71))
HALLS_OF_STONE = Zone("Halls of Stone", "Dungeon_Ulduar77_Normal", 4264, NR, NR, TP(599, 1153.24, 806.16, 195.94, 4.71))
THE_CULLING_OF_STRATHOLME = Zone("The Culling of Stratholme", "Dungeon_CoTStratholme_Normal", 4100, NR, NR, TP(595, 1431.1, 556.92, 36.7, 5.16))
THE_NEXUS = Zone("The Nexus", "Dungeon_Nexus70_Normal", 4265, NR, NR, TP(576, 145.87, -10.55, -16.62, 1.53))
THE_OCULUS = Zone("The Oculus", "Dungeon_Nexus80_Normal", 4228, NR, NR, TP(578, 1055.93, 986.85, 361.1, 5.745))
UTGARDE_KEEP = Zone("Utgarde Keep", "Dungeon_UtgardeKeep_Normal", 206, NR, NR, TP(574, 153.79, -86.55, 12.56, 0.3))
UTGARDE_PINNACLE = Zone("Utgarde Pinnacle", "Dungeon_UtgardePinnacle_Normal", 1196, NR, NR, TP(575, 584.12, -327.97, 110.14, 3.12))
VIOLET_HOLD = Zone("Violet Hold", "Dungeon_TheVioletHold_Normal", 4415, NR, NR, TP(608, 1808.82, 803.93, 44.37, 0))
NORTHREND_DUNGEONS = [
    AHNKAHET_THE_OLD_KINGDOM,
    AZJOL_NERUB,
    DRAKTHARON_KEEP,
    GUNDRAK,
    HALLS_OF_LIGHTNING,
    HALLS_OF_STONE,
    THE_CULLING_OF_STRATHOLME,
    THE_NEXUS,
    THE_OCULUS,
    UTGARDE_KEEP,
    UTGARDE_PINNACLE,
    VIOLET_HOLD,
]
NORTHREND = [
    BOREAN_TUNDRA,
    DRAGONBLIGHT,
    GRIZZLY_HILLS,
    HOWLING_FJORD,
    ICECROWN,
    SHOLAZAR_BASIN,
    THE_STORM_PEAKS,
    ZULDRAK,
]


for z in EASTERN_KINGDOMS:
    z.gossip_menu = 2

for z in KALIMDOR:
    z.gossip_menu = 3

for z in OUTLAND:
    z.gossip_menu = 4

for z in NORTHREND:
    z.gossip_menu = 5

for z in CLASSIC_DUNGEONS:
    z.gossip_menu = 7

for z in OUTLAND_DUNGEONS:
    z.gossip_menu = 8

for z in NORTHREND_DUNGEONS:
    z.gossip_menu = 9
