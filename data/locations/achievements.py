from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...world import World

from worlds.generic.Rules import set_rule

from ... import regions
from ...conditions import required_level
from ..items import zones
from ..items.zones import Zone
from .location_container import LocationContainer
from .location_registry import Location


class Achievement(Location):
    def __init__(self, name: str, achievement_id: int, zone: Optional[Zone] = None, required_level: Optional[int] = None):
        super().__init__(f"Achievement: {name}")
        ACHIEVEMENTS_CONTAINER.add(self)
        self.achievement_id = achievement_id
        self.zone = zone
        self.required_level = required_level


class AchievementsContainer(LocationContainer):
    def build_locations(self, world: "World"):
        locations = [*MISC, *CLASSIC_DUNGEONS]
        if world.has_tbc_content():
            locations += OUTLAND_DUNGEONS
        if world.has_wotlk_content():
            locations += NORTHREND_DUNGEONS

        return locations

    def get_slot_data(self, world: "World"):
        return [[loc.achievement_id, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        locations = self.build_locations(world)
        result: list[tuple[str, Location]] = []

        for loc in locations:
            region = regions.LEVELS_01_10
            if loc.zone:
                if world.is_alliance() and loc.zone.region_a:
                    region = loc.zone.region_a
                elif world.is_horde() and loc.zone.region_h:
                    region = loc.zone.region_h

            result.append((region, loc))

        return result

    def set_rules(self, world: "World"):
        for ach in self.build_locations(world):
            lvl = ach.required_level or -1
            if lvl > 1:
                set_rule(world.get_location(ach.name), required_level(lvl, world))


ACHIEVEMENTS_CONTAINER = AchievementsContainer()

# Classic Dungeons
RAGEFIRE_CHASM = Achievement("Ragefire Chasm", 629, zones.RAGEFIRE_CHASM, 13)
DEADMINES = Achievement("Deadmines", 628, zones.THE_DEADMINES, 17)
WAILING_CAVERNS = Achievement("Wailing Caverns", 630, zones.WAILING_CAVERNS, 17)
SHADOWFANG_KEEP = Achievement("Shadowfang Keep", 631, zones.SHADOWFANG_KEEP, 18)
BLACKFATHOM_DEEPS = Achievement("Blackfathom Deeps", 632, zones.BLACKFATHOM_DEEPS, 21)
STORMWIND_STOCKADE = Achievement("Stormwind Stockade", 633, zones.THE_STOCKADE, 22)
RAZORFEN_KRAUL = Achievement("Razorfen Kraul", 635, zones.RAZORFEN_KRAUL, 24)
GNOMEREGAN = Achievement("Gnomeregan", 634, zones.GNOMEREGAN, 25)
RAZORFEN_DOWNS = Achievement("Razorfen Downs", 636, zones.RAZORFEN_DOWNS, 34)
SCARLET_MONASTERY = Achievement("Scarlet Monastery", 637, zones.SCARLET_MONASTERY, 29)
ULDAMAN = Achievement("Uldaman", 638, zones.ULDAMAN, 37)
ZUL_FARRAK = Achievement("Zul'Farrak", 639, zones.ZULFARRAK, 43)
MARAUDON = Achievement("Maraudon", 640, zones.MARAUDON, 41)
SUNKEN_TEMPLE = Achievement("Sunken Temple", 641, zones.SUNKEN_TEMPLE, 47)
BLACKROCK_DEPTHS = Achievement("Blackrock Depths", 642, zones.BLACKROCK_DEPTHS, 49)
KING_OF_DIRE_MAUL = Achievement("King of Dire Maul", 644, zones.DIRE_MAUL, 55)
LOWER_BLACKROCK_SPIRE = Achievement("Lower Blackrock Spire", 643, zones.BLACKROCK_SPIRE, 56)
SCHOLOMANCE = Achievement("Scholomance", 645, zones.SCHOLOMANCE, 58)
STRATHOLME = Achievement("Stratholme", 646, zones.STRATHOLME, 58)
CLASSIC_DUNGEONS = [
    RAGEFIRE_CHASM,
    DEADMINES,
    WAILING_CAVERNS,
    SHADOWFANG_KEEP,
    BLACKFATHOM_DEEPS,
    STORMWIND_STOCKADE,
    RAZORFEN_KRAUL,
    GNOMEREGAN,
    RAZORFEN_DOWNS,
    SCARLET_MONASTERY,
    ULDAMAN,
    ZUL_FARRAK,
    MARAUDON,
    SUNKEN_TEMPLE,
    BLACKROCK_DEPTHS,
    KING_OF_DIRE_MAUL,
    LOWER_BLACKROCK_SPIRE,
    SCHOLOMANCE,
    STRATHOLME,
]

# Outland Dungeons
AUCHENAI_CRYPTS = Achievement("Auchenai Crypts", 666, zones.AUCHENAI_CRYPTS, 66)
HELLFIRE_RAMPARTS = Achievement("Hellfire Ramparts", 647, zones.HELLFIRE_RAMPARTS, 61)
MAGISTERS_TERRACE = Achievement("Magister's Terrace", 661, zones.MAGISTERS_TERRACE, 68)
MANA_TOMBS = Achievement("Mana-Tombs", 651, zones.MANA_TOMBS, 65)
OPENING_OF_THE_DARK_PORTAL = Achievement("Opening of the Dark Portal", 655, zones.THE_BLACK_MORASS, 68)
SETHEKK_HALLS = Achievement("Sethekk Halls", 653, zones.SETHEKK_HALLS, 67)
SHADOW_LABYRINTH = Achievement("Shadow Labyrinth", 654, zones.SHADOW_LABYRINTH, 68)
THE_ARCATRAZ = Achievement("The Arcatraz", 660, zones.THE_ARCATRAZ, 68)
THE_BLOOD_FURNACE = Achievement("The Blood Furnace", 648, zones.THE_BLOOD_FURNACE, 62)
THE_BOTANICA = Achievement("The Botanica", 659, zones.THE_BOTANICA, 68)
THE_ESCAPE_FROM_DURNHOLDE = Achievement("The Escape From Durnholde", 652, zones.OLD_HILLSBRAD_FOOTHILLS, 67)
THE_MECHANAR = Achievement("The Mechanar", 658, zones.THE_MECHANAR, 68)
THE_SHATTERED_HALLS = Achievement("The Shattered Halls", 657, zones.THE_SHATTERED_HALLS, 68)
THE_SLAVE_PENS = Achievement("The Slave Pens", 649, zones.THE_SLAVE_PENS, 63)
THE_STEAMVAULT = Achievement("The Steamvault", 656, zones.THE_STEAMVAULT, 68)
UNDERBOG = Achievement("Underbog", 650, zones.THE_UNDERBOG, 64)
OUTLAND_DUNGEONS = [
    AUCHENAI_CRYPTS,
    HELLFIRE_RAMPARTS,
    MAGISTERS_TERRACE,
    MANA_TOMBS,
    OPENING_OF_THE_DARK_PORTAL,
    SETHEKK_HALLS,
    SHADOW_LABYRINTH,
    THE_ARCATRAZ,
    THE_BLOOD_FURNACE,
    THE_BOTANICA,
    THE_ESCAPE_FROM_DURNHOLDE,
    THE_MECHANAR,
    THE_SHATTERED_HALLS,
    THE_SLAVE_PENS,
    THE_STEAMVAULT,
    UNDERBOG,
]

# Northrend Dungeons
AHNKAHET_THE_OLD_KINGDOM = Achievement("Ahn'Kahet: The Old Kingdom", 481, zones.AHNKAHET_THE_OLD_KINGDOM, 73)
AZJOL_NERUB = Achievement("Azjol-Nerub", 480, zones.AZJOL_NERUB, 72)
DRAKTHARON_KEEP = Achievement("Drak'Tharon Keep", 482, zones.DRAKTHARON_KEEP, 73)
GUNDRAK = Achievement("Gundrak", 484, zones.GUNDRAK, 76)
HALLS_OF_LIGHTNING = Achievement("Halls of Lightning", 486, zones.HALLS_OF_LIGHTNING, 78)
HALLS_OF_STONE = Achievement("Halls of Stone", 485, zones.HALLS_OF_STONE, 76)
THE_CULLING_OF_STRATHOLME = Achievement("The Culling of Stratholme", 479, zones.THE_CULLING_OF_STRATHOLME, 78)
THE_NEXUS = Achievement("The Nexus", 478, zones.THE_NEXUS, 71)
THE_OCULUS = Achievement("The Oculus", 487, zones.THE_OCULUS, 78)
THE_VIOLET_HOLD = Achievement("The Violet Hold", 483, zones.VIOLET_HOLD, 74)
UTGARDE_KEEP = Achievement("Utgarde Keep", 477, zones.UTGARDE_KEEP, 70)
UTGARDE_PINNACLE = Achievement("Utgarde Pinnacle", 488, zones.UTGARDE_PINNACLE, 78)
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
    THE_VIOLET_HOLD,
    UTGARDE_KEEP,
    UTGARDE_PINNACLE,
]

# General
CAN_I_KEEP_HIM = Achievement("Can I Keep Him?", 1017, None, 10)
REPRESENT = Achievement("Represent", 621, None, 20)
SHAVE_AND_A_HAIRCUT = Achievement("Shave and a Haircut", 545, None, 30)
_50_QUESTS_COMPLETED = Achievement("50 Quests Completed", 503, None, 15)
_100_QUESTS_COMPLETED = Achievement("100 Quests Completed", 504, None, 30)
_250_QUESTS_COMPLETED = Achievement("250 Quests Completed", 505, None, 50)
MISC = [CAN_I_KEEP_HIM, REPRESENT, SHAVE_AND_A_HAIRCUT, _50_QUESTS_COMPLETED, _100_QUESTS_COMPLETED, _250_QUESTS_COMPLETED]
