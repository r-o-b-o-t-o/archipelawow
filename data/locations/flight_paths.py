from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from ...conditions import set_location_rule
from ...options import CharacterRace
from ..items import zones
from ..items.zones import ZONES_CONTAINER, Zone
from .location_container import LocationContainer
from .location_registry import Location


class Side(IntEnum):
    BOTH = 1
    ALLIANCE = 2
    HORDE = 3


class FlightPath(Location):
    def __init__(self, name: str, zone: Zone, node_id: int, side: Side):
        super().__init__(f"Flight Path: {name} ({zone.name})")
        FLIGHT_PATHS_CONTAINER.add(self)
        self.zone = zone
        self.node_id = node_id
        self.side = side


class FlightPathsContainer(LocationContainer):
    def build_locations(self, world: "World"):
        locations = [*EASTERN_KINGDOMS, *KALIMDOR]
        if world.has_tbc_content():
            locations += OUTLAND
        if world.has_wotlk_content():
            locations += NORTHREND

        exclude: list[FlightPath] = []
        if world.is_alliance():
            exclude += list(filter(lambda loc: loc.side == Side.HORDE, locations))
        else:
            exclude += list(filter(lambda loc: loc.side == Side.ALLIANCE, locations))

        match world.options.character_race.value:
            case CharacterRace.option_human:
                exclude.append(STORMWIND)
            case CharacterRace.option_dwarf | CharacterRace.option_gnome:
                exclude.append(IRONFORGE)
            case CharacterRace.option_night_elf:
                exclude += [RUTTHERAN_VILLAGE, AUBERDINE]
            case CharacterRace.option_draenei:
                exclude.append(THE_EXODAR)
            case CharacterRace.option_orc | CharacterRace.option_troll:
                exclude.append(ORGRIMMAR)
            case CharacterRace.option_undead:
                exclude.append(UNDERCITY)
            case CharacterRace.option_tauren:
                exclude.append(THUNDER_BLUFF)
            case CharacterRace.option_blood_elf:
                exclude.append(SILVERMOON_CITY)

        exclude_set = set([x.id for x in exclude])
        return [loc for loc in locations if loc.id not in exclude_set]

    def get_slot_data(self, world: "World"):
        return [[loc.node_id, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        locations = self.build_locations(world)
        result: list[tuple[str, Location]] = []

        for loc in locations:
            region: str | None = None
            if loc.zone:
                if world.is_alliance() and loc.zone.region_a:
                    region = loc.zone.region_a
                elif world.is_horde() and loc.zone.region_h:
                    region = loc.zone.region_h
            if region:
                result.append((region, loc))

        return result

    def set_rules(self, world: "World"):
        zones_in_pool = ZONES_CONTAINER.build_pool(world)
        zone_ids = set([zone.id for zone in zones_in_pool])

        for fp in self.build_locations(world):
            if fp.zone.id in zone_ids:
                set_location_rule(fp.name, fp.zone.name, world)


FLIGHT_PATHS_CONTAINER = FlightPathsContainer()

# Eastern Kingdoms
AERIE_PEAK = FlightPath("Aerie Peak", zones.THE_HINTERLANDS, 43, Side.ALLIANCE)
BOOTY_BAY_A = FlightPath("Booty Bay [A]", zones.STRANGLETHORN_VALE, 19, Side.ALLIANCE)
CHILLWIND_CAMP = FlightPath("Chillwind Camp", zones.WESTERN_PLAGUELANDS, 66, Side.ALLIANCE)
DARKSHIRE = FlightPath("Darkshire", zones.DUSKWOOD, 12, Side.ALLIANCE)
IRONFORGE = FlightPath("Ironforge", zones.DUN_MOROGH, 6, Side.ALLIANCE)
LAKESHIRE = FlightPath("Lakeshire", zones.REDRIDGE_MOUNTAINS, 5, Side.ALLIANCE)
LIGHTS_HOPE_CHAPEL_A = FlightPath("Light's Hope Chapel [A]", zones.EASTERN_PLAGUELANDS, 67, Side.ALLIANCE)
MENETHIL_HARBOR = FlightPath("Menethil Harbor", zones.WETLANDS, 7, Side.ALLIANCE)
MORGANS_VIGIL = FlightPath("Morgan's Vigil", zones.BURNING_STEPPES, 71, Side.ALLIANCE)
NETHERGARDE_KEEP = FlightPath("Nethergarde Keep", zones.BLASTED_LANDS, 45, Side.ALLIANCE)
REBEL_CAMP = FlightPath("Rebel Camp", zones.STRANGLETHORN_VALE, 195, Side.ALLIANCE)
REFUGE_POINTE = FlightPath("Refuge Pointe", zones.ARATHI_HIGHLANDS, 16, Side.ALLIANCE)
SENTINEL_HILL = FlightPath("Sentinel Hill", zones.WESTFALL, 4, Side.ALLIANCE)
SOUTHSHORE = FlightPath("Southshore", zones.HILLSBRAD_FOOTHILLS, 14, Side.ALLIANCE)
STORMWIND = FlightPath("Stormwind", zones.ELWYNN_FOREST, 2, Side.ALLIANCE)
THELSAMAR = FlightPath("Thelsamar", zones.LOCH_MODAN, 8, Side.ALLIANCE)
THORIUM_POINT_A = FlightPath("Thorium Point [A]", zones.SEARING_GORGE, 74, Side.ALLIANCE)

BOOTY_BAY_H = FlightPath("Booty Bay [H]", zones.STRANGLETHORN_VALE, 18, Side.HORDE)
FLAME_CREST = FlightPath("Flame Crest", zones.BURNING_STEPPES, 70, Side.HORDE)
GROMGOL = FlightPath("Grom'gol", zones.STRANGLETHORN_VALE, 20, Side.HORDE)
HAMMERFALL = FlightPath("Hammerfall", zones.ARATHI_HIGHLANDS, 17, Side.HORDE)
KARGATH = FlightPath("Kargath", zones.BADLANDS, 21, Side.HORDE)
LIGHTS_HOPE_CHAPEL_H = FlightPath("Light's Hope Chapel [H]", zones.EASTERN_PLAGUELANDS, 68, Side.HORDE)
REVANTUSK_VILLAGE = FlightPath("Revantusk Village", zones.THE_HINTERLANDS, 76, Side.HORDE)
SILVERMOON_CITY = FlightPath("Silvermoon City", zones.EVERSONG_WOODS, 82, Side.HORDE)
STONARD = FlightPath("Stonard", zones.SWAMP_OF_SORROWS, 56, Side.HORDE)
TARREN_MILL = FlightPath("Tarren Mill", zones.HILLSBRAD_FOOTHILLS, 13, Side.HORDE)
THE_BULWARK = FlightPath("The Bulwark", zones.TIRISFAL_GLADES, 384, Side.HORDE)
THE_SEPULCHER = FlightPath("The Sepulcher", zones.SILVERPINE_FOREST, 10, Side.HORDE)
THORIUM_POINT_H = FlightPath("Thorium Point [H]", zones.SEARING_GORGE, 75, Side.HORDE)
TRANQUILLIEN = FlightPath("Tranquillien", zones.GHOSTLANDS, 83, Side.HORDE)
UNDERCITY = FlightPath("Undercity", zones.TIRISFAL_GLADES, 11, Side.HORDE)

THONDRORIL_RIVER = FlightPath("Thondroril River", zones.WESTERN_PLAGUELANDS, 383, Side.BOTH)

EASTERN_KINGDOMS = [
    AERIE_PEAK,
    BOOTY_BAY_A,
    CHILLWIND_CAMP,
    DARKSHIRE,
    IRONFORGE,
    LAKESHIRE,
    LIGHTS_HOPE_CHAPEL_A,
    MENETHIL_HARBOR,
    MORGANS_VIGIL,
    NETHERGARDE_KEEP,
    REBEL_CAMP,
    REFUGE_POINTE,
    SENTINEL_HILL,
    SOUTHSHORE,
    STORMWIND,
    THELSAMAR,
    THORIUM_POINT_A,
    BOOTY_BAY_H,
    FLAME_CREST,
    GROMGOL,
    HAMMERFALL,
    KARGATH,
    LIGHTS_HOPE_CHAPEL_H,
    REVANTUSK_VILLAGE,
    SILVERMOON_CITY,
    STONARD,
    TARREN_MILL,
    THE_BULWARK,
    THE_SEPULCHER,
    THORIUM_POINT_H,
    TRANQUILLIEN,
    UNDERCITY,
    THONDRORIL_RIVER,
]

# Kalimdor
ASTRANAAR = FlightPath("Astranaar", zones.ASHENVALE, 28, Side.ALLIANCE)
AUBERDINE = FlightPath("Auberdine", zones.DARKSHORE, 26, Side.ALLIANCE)
BLOODWATCH = FlightPath("Blood Watch", zones.BLOODMYST_ISLE, 93, Side.ALLIANCE)
CENARION_HOLD_A = FlightPath("Cenarion Hold [A]", zones.SILITHUS, 73, Side.ALLIANCE)
EVERLOOK_A = FlightPath("Everlook [A]", zones.WINTERSPRING, 52, Side.ALLIANCE)
FEATHERMOON = FlightPath("Feathermoon", zones.FERALAS, 41, Side.ALLIANCE)
FOREST_SONG = FlightPath("Forest Song", zones.ASHENVALE, 167, Side.ALLIANCE)
GADGETZAN_A = FlightPath("Gadgetzan [A]", zones.TANARIS, 39, Side.ALLIANCE)
NIJELS_POINT = FlightPath("Nijel's Point", zones.DESOLACE, 37, Side.ALLIANCE)
RUTTHERAN_VILLAGE = FlightPath("Rut'theran Village", zones.TELDRASSIL, 27, Side.ALLIANCE)
STONETALON_PEAK = FlightPath("Stonetalon Peak", zones.STONETALON_MOUNTAINS, 33, Side.ALLIANCE)
TALONBRANCH_GLADE = FlightPath("Talonbranch Glade", zones.FELWOOD, 65, Side.ALLIANCE)
TALRENDIS_POINT = FlightPath("Talrendis Point", zones.AZSHARA, 64, Side.ALLIANCE)
THALANAAR = FlightPath("Thalanaar", zones.FERALAS, 31, Side.ALLIANCE)
THERAMORE_ISLE = FlightPath("Theramore Isle", zones.DUSTWALLOW_MARSH, 32, Side.ALLIANCE)
THE_EXODAR = FlightPath("The Exodar", zones.AZUREMYST_ISLE, 94, Side.ALLIANCE)

BLOODVENOM_POST = FlightPath("Bloodvenom Post", zones.FELWOOD, 48, Side.HORDE)
BRACKENWALL_VILLAGE = FlightPath("Brackenwall Village", zones.DUSTWALLOW_MARSH, 55, Side.HORDE)
CAMP_MOJACHE = FlightPath("Camp Mojache", zones.FERALAS, 42, Side.HORDE)
CAMP_TAURAJO = FlightPath("Camp Taurajo", zones.THE_BARRENS, 77, Side.HORDE)
CENARION_HOLD_H = FlightPath("Cenarion Hold [H]", zones.SILITHUS, 72, Side.HORDE)
EVERLOOK_H = FlightPath("Everlook [H]", zones.WINTERSPRING, 53, Side.HORDE)
FREEWIND_POST = FlightPath("Freewind Post", zones.THOUSAND_NEEDLES, 30, Side.HORDE)
GADGETZAN_H = FlightPath("Gadgetzan [H]", zones.TANARIS, 40, Side.HORDE)
ORGRIMMAR = FlightPath("Orgrimmar", zones.DUROTAR, 23, Side.HORDE)
RATCHET = FlightPath("Ratchet", zones.THE_BARRENS, 80, Side.HORDE)
SHADOWPREY_VILLAGE = FlightPath("Shadowprey Village", zones.DESOLACE, 38, Side.HORDE)
SPLINTERTREE_POST = FlightPath("Splintertree Post", zones.ASHENVALE, 61, Side.HORDE)
SUN_ROCK_RETREAT = FlightPath("Sun Rock Retreat", zones.STONETALON_MOUNTAINS, 29, Side.HORDE)
THE_CROSSROADS = FlightPath("Crossroads", zones.THE_BARRENS, 25, Side.HORDE)
THUNDER_BLUFF = FlightPath("Thunder Bluff", zones.MULGORE, 22, Side.HORDE)
VALORMOK = FlightPath("Valormok", zones.AZSHARA, 44, Side.HORDE)
ZORAMGAR_OUTPOST = FlightPath("Zoram'gar Outpost", zones.ASHENVALE, 58, Side.HORDE)

EMERALD_SANCTUARY = FlightPath("Emerald Sanctuary", zones.FELWOOD, 166, Side.BOTH)
MARSHALS_REFUGE = FlightPath("Marshal's Refuge", zones.UNGORO_CRATER, 79, Side.BOTH)
MUDSPROCKET = FlightPath("Mudsprocket", zones.DUSTWALLOW_MARSH, 179, Side.BOTH)

KALIMDOR = [
    ASTRANAAR,
    AUBERDINE,
    BLOODWATCH,
    CENARION_HOLD_A,
    EVERLOOK_A,
    FEATHERMOON,
    FOREST_SONG,
    GADGETZAN_A,
    NIJELS_POINT,
    RUTTHERAN_VILLAGE,
    STONETALON_PEAK,
    TALONBRANCH_GLADE,
    TALRENDIS_POINT,
    THALANAAR,
    THERAMORE_ISLE,
    THE_EXODAR,
    BLOODVENOM_POST,
    BRACKENWALL_VILLAGE,
    CAMP_MOJACHE,
    CAMP_TAURAJO,
    CENARION_HOLD_H,
    EVERLOOK_H,
    FREEWIND_POST,
    GADGETZAN_H,
    ORGRIMMAR,
    RATCHET,
    SHADOWPREY_VILLAGE,
    SPLINTERTREE_POST,
    SUN_ROCK_RETREAT,
    THE_CROSSROADS,
    THUNDER_BLUFF,
    VALORMOK,
    ZORAMGAR_OUTPOST,
    EMERALD_SANCTUARY,
    MARSHALS_REFUGE,
    MUDSPROCKET,
]

# Outland
ALLERIAN_STRONGHOLD = FlightPath("Allerian Stronghold", zones.TEROKKAR_FOREST, 121, Side.ALLIANCE)
OREBOR_HARBORAGE = FlightPath("Orebor Harborage", zones.ZANGARMARSH, 164, Side.ALLIANCE)
SHATTER_POINT = FlightPath("Shatter Point", zones.HELLFIRE_PENINSULA, 149, Side.ALLIANCE)
SYLVANAAR = FlightPath("Sylvanaar", zones.BLADES_EDGE_MOUNTAINS, 125, Side.ALLIANCE)
TELAAR = FlightPath("Telaar", zones.NAGRAND, 119, Side.ALLIANCE)
TELREDOR = FlightPath("Telredor", zones.ZANGARMARSH, 117, Side.ALLIANCE)
TEMPLE_OF_TELHAMAT = FlightPath("Temple of Telhamat", zones.HELLFIRE_PENINSULA, 101, Side.ALLIANCE)
THE_DARK_PORTAL_A = FlightPath("The Dark Portal [A]", zones.HELLFIRE_PENINSULA, 129, Side.ALLIANCE)
TOSHLEYS_STATION = FlightPath("Toshley's Station", zones.BLADES_EDGE_MOUNTAINS, 156, Side.ALLIANCE)
WILDHAMMER_STRONGHOLD = FlightPath("Wildhammer Stronghold", zones.SHADOWMOON_VALLEY, 124, Side.ALLIANCE)

FALCON_WATCH = FlightPath("Falcon Watch", zones.HELLFIRE_PENINSULA, 102, Side.HORDE)
GARADAR = FlightPath("Garadar", zones.NAGRAND, 120, Side.HORDE)
SHADOWMOON_VILLAGE = FlightPath("Shadowmoon Village", zones.SHADOWMOON_VALLEY, 123, Side.HORDE)
SPINEBREAKER_POST = FlightPath("Spinebreaker Post", zones.HELLFIRE_PENINSULA, 141, Side.HORDE)
STONEBREAKER_HOLD = FlightPath("Stonebreaker Hold", zones.TEROKKAR_FOREST, 127, Side.HORDE)
SWAMPRAT_POST = FlightPath("Swamprat Post", zones.ZANGARMARSH, 151, Side.HORDE)
THE_DARK_PORTAL_H = FlightPath("The Dark Portal [H]", zones.HELLFIRE_PENINSULA, 130, Side.HORDE)
THUNDERLORD_STRONGHOLD = FlightPath("Thunderlord Stronghold", zones.BLADES_EDGE_MOUNTAINS, 126, Side.HORDE)
ZABRAJIN = FlightPath("Zabra'Jin", zones.ZANGARMARSH, 118, Side.HORDE)

AREA_52 = FlightPath("Area 52", zones.NETHERSTORM, 122, Side.BOTH)
COSMOWRENCH = FlightPath("Cosmowrench", zones.NETHERSTORM, 150, Side.BOTH)
EVERGROVE = FlightPath("Evergrove", zones.BLADES_EDGE_MOUNTAINS, 160, Side.BOTH)
STORMSPIRE = FlightPath("Stormspire", zones.NETHERSTORM, 139, Side.BOTH)

OUTLAND = [
    ALLERIAN_STRONGHOLD,
    OREBOR_HARBORAGE,
    SHATTER_POINT,
    SYLVANAAR,
    TELAAR,
    TELREDOR,
    TEMPLE_OF_TELHAMAT,
    THE_DARK_PORTAL_A,
    TOSHLEYS_STATION,
    WILDHAMMER_STRONGHOLD,
    FALCON_WATCH,
    GARADAR,
    SHADOWMOON_VILLAGE,
    SPINEBREAKER_POST,
    STONEBREAKER_HOLD,
    SWAMPRAT_POST,
    THE_DARK_PORTAL_H,
    THUNDERLORD_STRONGHOLD,
    ZABRAJIN,
    AREA_52,
    COSMOWRENCH,
    EVERGROVE,
    STORMSPIRE,
]

# Northrend
AMBERPINE_LODGE = FlightPath("Amberpine Lodge", zones.GRIZZLY_HILLS, 253, Side.ALLIANCE)
FIZZCRANK_AIRSTRIP = FlightPath("Fizzcrank Airstrip", zones.BOREAN_TUNDRA, 246, Side.ALLIANCE)
FORDRAGON_HOLD = FlightPath("Fordragon Hold", zones.DRAGONBLIGHT, 251, Side.ALLIANCE)
FORT_WILDERVAR = FlightPath("Fort Wildervar", zones.HOWLING_FJORD, 184, Side.ALLIANCE)
FROSTHOLD = FlightPath("Frosthold", zones.THE_STORM_PEAKS, 321, Side.ALLIANCE)
STARS_REST = FlightPath("Star's Rest", zones.DRAGONBLIGHT, 247, Side.ALLIANCE)
VALGARDE = FlightPath("Valgarde", zones.HOWLING_FJORD, 183, Side.ALLIANCE)
VALIANCE_KEEP = FlightPath("Valiance Keep", zones.BOREAN_TUNDRA, 245, Side.ALLIANCE)
WESTFALL_BRIGADE = FlightPath("Westfall Brigade", zones.GRIZZLY_HILLS, 255, Side.ALLIANCE)
WESTGUARD_KEEP = FlightPath("Westguard Keep", zones.HOWLING_FJORD, 185, Side.ALLIANCE)
WINTERGARDE_KEEP = FlightPath("Wintergarde Keep", zones.DRAGONBLIGHT, 244, Side.ALLIANCE)

AGMARS_HAMMER = FlightPath("Agmar's Hammer", zones.DRAGONBLIGHT, 256, Side.HORDE)
APOTHECARY_CAMP = FlightPath("Apothecary Camp", zones.HOWLING_FJORD, 248, Side.HORDE)
BORGOROK_OUTPOST = FlightPath("Bor'gorok Outpost", zones.BOREAN_TUNDRA, 259, Side.HORDE)
CAMP_ONEQWAH = FlightPath("Camp Oneqwah", zones.GRIZZLY_HILLS, 249, Side.HORDE)
CAMP_TUNKALO = FlightPath("Camp Tunka'lo", zones.THE_STORM_PEAKS, 324, Side.HORDE)
CAMP_WINTERHOOF = FlightPath("Camp Winterhoof", zones.HOWLING_FJORD, 192, Side.HORDE)
CONQUEST_HOLD = FlightPath("Conquest Hold", zones.GRIZZLY_HILLS, 250, Side.HORDE)
GROMARSH_CRASH_SITE = FlightPath("Grom'arsh Crash-Site", zones.THE_STORM_PEAKS, 323, Side.HORDE)
KORKRON_VANGUARD = FlightPath("Kor'kron Vanguard", zones.DRAGONBLIGHT, 260, Side.HORDE)
NEW_AGAMAND = FlightPath("New Agamand", zones.HOWLING_FJORD, 190, Side.HORDE)
TAUNKALE_VILLAGE = FlightPath("Taunka'le Village", zones.BOREAN_TUNDRA, 258, Side.HORDE)
VENGEANCE_LANDING = FlightPath("Vengeance Landing", zones.HOWLING_FJORD, 191, Side.HORDE)
VENOMSPITE = FlightPath("Venomspite", zones.DRAGONBLIGHT, 254, Side.HORDE)
WARSONG_HOLD = FlightPath("Warsong Hold", zones.BOREAN_TUNDRA, 257, Side.HORDE)

AMBER_LEDGE = FlightPath("Amber Ledge", zones.BOREAN_TUNDRA, 289, Side.BOTH)
BOULDERCRAGS_REFUGE = FlightPath("Bouldercrag's Refuge", zones.THE_STORM_PEAKS, 327, Side.BOTH)
DEATHS_RISE = FlightPath("Death's Rise", zones.ICECROWN, 325, Side.BOTH)
EBON_WATCH = FlightPath("Ebon Watch", zones.ZULDRAK, 305, Side.BOTH)
GUNDRAK = FlightPath("Gundrak", zones.ZULDRAK, 331, Side.BOTH)
K3 = FlightPath("K3", zones.THE_STORM_PEAKS, 320, Side.BOTH)
KAMAGUA = FlightPath("Kamagua", zones.HOWLING_FJORD, 295, Side.BOTH)
LIGHTS_BREACH = FlightPath("Light's Breach", zones.ZULDRAK, 306, Side.BOTH)
MOAKI_HARBOR = FlightPath("Moa'ki Harbor", zones.DRAGONBLIGHT, 294, Side.BOTH)
NESINGWARY_BASE_CAMP = FlightPath("Nesingwary Base Camp", zones.SHOLAZAR_BASIN, 309, Side.BOTH)
RIVERS_HEART = FlightPath("River's Heart", zones.SHOLAZAR_BASIN, 308, Side.BOTH)
THE_ARGENT_STAND = FlightPath("The Argent Stand", zones.ZULDRAK, 304, Side.BOTH)
THE_ARGENT_VANGUARD = FlightPath("The Argent Vanguard", zones.ICECROWN, 334, Side.BOTH)
TRANSITUS_SHIELD = FlightPath("Transitus Shield", zones.BOREAN_TUNDRA, 226, Side.BOTH)
UNUPE = FlightPath("Unu'pe", zones.BOREAN_TUNDRA, 296, Side.BOTH)
WYRMREST_TEMPLE = FlightPath("Wyrmrest Temple", zones.DRAGONBLIGHT, 252, Side.BOTH)
ZIMTORGA = FlightPath("Zim'Torga", zones.ZULDRAK, 307, Side.BOTH)

NORTHREND = [
    AMBERPINE_LODGE,
    FIZZCRANK_AIRSTRIP,
    FORDRAGON_HOLD,
    FORT_WILDERVAR,
    FROSTHOLD,
    STARS_REST,
    VALGARDE,
    VALIANCE_KEEP,
    WESTFALL_BRIGADE,
    WESTGUARD_KEEP,
    WINTERGARDE_KEEP,
    AGMARS_HAMMER,
    APOTHECARY_CAMP,
    BORGOROK_OUTPOST,
    CAMP_ONEQWAH,
    CAMP_TUNKALO,
    CAMP_WINTERHOOF,
    CONQUEST_HOLD,
    GROMARSH_CRASH_SITE,
    KORKRON_VANGUARD,
    NEW_AGAMAND,
    TAUNKALE_VILLAGE,
    VENGEANCE_LANDING,
    VENOMSPITE,
    WARSONG_HOLD,
    AMBER_LEDGE,
    BOULDERCRAGS_REFUGE,
    DEATHS_RISE,
    EBON_WATCH,
    GUNDRAK,
    K3,
    KAMAGUA,
    LIGHTS_BREACH,
    MOAKI_HARBOR,
    NESINGWARY_BASE_CAMP,
    RIVERS_HEART,
    THE_ARGENT_STAND,
    THE_ARGENT_VANGUARD,
    TRANSITUS_SHIELD,
    UNUPE,
    WYRMREST_TEMPLE,
    ZIMTORGA,
]
