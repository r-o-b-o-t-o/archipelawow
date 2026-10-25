from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..world import World

from rule_builder.rules import Or, Rule

from .. import regions
from ..boss_model import hardest_boss_level
from ..conditions import has_zone, required_level
from ..items import zones
from ..items.zones import ZONES_CONTAINER, Zone
from ..options import Dungeonsanity
from .location_container import LocationContainer
from .location_registry import Location


class Achievement(Location):
    def __init__(
        self,
        name: str,
        achievement_id: int,
        zone: Optional[Zone] = None,
        required_level: Optional[int] = None,
        served_in: tuple[Zone, ...] = (),
    ):
        """`zone` is where the achievement is earned, and is opened with its bracket. `served_in` lists the zones
        with a vendor or barber that serves the achievement, one of which it asks for unless the character starts in one."""
        super().__init__(f"Achievement: {name}")
        ACHIEVEMENTS_CONTAINER.add(self)
        self.achievement_id = achievement_id
        self.zone = zone
        self.required_level = required_level
        self.served_in = served_in


class AchievementsContainer(LocationContainer[Achievement]):
    def build_locations(self, world: "World"):
        locations = [*MISC]
        if world.options.classic_dungeonsanity.value != Dungeonsanity.option_none:
            locations += CLASSIC_DUNGEONS
        if world.options.outland_dungeonsanity.value != Dungeonsanity.option_none:
            locations += OUTLAND_DUNGEONS
        if world.options.northrend_dungeonsanity.value != Dungeonsanity.option_none:
            locations += NORTHREND_DUNGEONS

        # The pool already leaves out the dungeons past the seed's level cap
        zones_in_pool = set(ZONES_CONTAINER.build_pool(world))
        return [
            loc
            for loc in locations
            if (loc.zone is None or loc.zone in zones_in_pool) and (loc.required_level is None or loc.required_level <= world.max_location_level())
        ]

    def get_slot_data(self, world: "World"):
        return [[loc.achievement_id, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        return [(loc.zone.region(world) if loc.zone else regions.LEVELS_01_05, loc) for loc in self.build_locations(world)]

    def set_rules(self, world: "World"):
        zones_in_pool = ZONES_CONTAINER.build_pool(world)
        starting_zones = ZONES_CONTAINER.get_precollected_items(world)
        for ach in self.build_locations(world):
            rule: Optional[Rule] = required_level(ach.required_level) if ach.required_level else None

            # The zone's bracket already asks for it, but the launcher's tracker opens a bracket on its level alone
            if ach.zone:
                zone_rule = has_zone(ach.zone, world)
                rule = zone_rule if rule is None else zone_rule & rule

            # Only the zones of the pool count, which leaves out the other faction's
            vendor_zones = [zone for zone in ach.served_in if zone in zones_in_pool]
            if vendor_zones and not any(zone in starting_zones for zone in vendor_zones):
                zone_rule = Or(*[has_zone(zone, world) for zone in vendor_zones])
                rule = zone_rule if rule is None else rule & zone_rule

            if rule is not None:
                world.set_rule(world.get_location(ach.name), rule)


ACHIEVEMENTS_CONTAINER = AchievementsContainer()


def dungeon(name: str, achievement_id: int, zone: Zone) -> Achievement:
    """A dungeon's achievement, which asks for the level of the dungeon's hardest boss. The classic and Outland ones' criteria
    only name the last boss or a few, but none of the others asks for more than the ones named."""
    return Achievement(name, achievement_id, zone, hardest_boss_level(zone.teleport.map))


# Classic Dungeons
RAGEFIRE_CHASM = dungeon("Ragefire Chasm", 629, zones.RAGEFIRE_CHASM)
DEADMINES = dungeon("Deadmines", 628, zones.THE_DEADMINES)
WAILING_CAVERNS = dungeon("Wailing Caverns", 630, zones.WAILING_CAVERNS)
SHADOWFANG_KEEP = dungeon("Shadowfang Keep", 631, zones.SHADOWFANG_KEEP)
BLACKFATHOM_DEEPS = dungeon("Blackfathom Deeps", 632, zones.BLACKFATHOM_DEEPS)
STORMWIND_STOCKADE = dungeon("Stormwind Stockade", 633, zones.THE_STOCKADE)
RAZORFEN_KRAUL = dungeon("Razorfen Kraul", 635, zones.RAZORFEN_KRAUL)
GNOMEREGAN = dungeon("Gnomeregan", 634, zones.GNOMEREGAN)
RAZORFEN_DOWNS = dungeon("Razorfen Downs", 636, zones.RAZORFEN_DOWNS)
SCARLET_MONASTERY = dungeon("Scarlet Monastery", 637, zones.SCARLET_MONASTERY)
ULDAMAN = dungeon("Uldaman", 638, zones.ULDAMAN)
ZUL_FARRAK = dungeon("Zul'Farrak", 639, zones.ZULFARRAK)
MARAUDON = dungeon("Maraudon", 640, zones.MARAUDON)
SUNKEN_TEMPLE = dungeon("Sunken Temple", 641, zones.SUNKEN_TEMPLE)
BLACKROCK_DEPTHS = dungeon("Blackrock Depths", 642, zones.BLACKROCK_DEPTHS)
KING_OF_DIRE_MAUL = dungeon("King of Dire Maul", 644, zones.DIRE_MAUL)
LOWER_BLACKROCK_SPIRE = dungeon("Lower Blackrock Spire", 643, zones.BLACKROCK_SPIRE)
SCHOLOMANCE = dungeon("Scholomance", 645, zones.SCHOLOMANCE)
STRATHOLME = dungeon("Stratholme", 646, zones.STRATHOLME)
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
AUCHENAI_CRYPTS = dungeon("Auchenai Crypts", 666, zones.AUCHENAI_CRYPTS)
HELLFIRE_RAMPARTS = dungeon("Hellfire Ramparts", 647, zones.HELLFIRE_RAMPARTS)
MAGISTERS_TERRACE = dungeon("Magister's Terrace", 661, zones.MAGISTERS_TERRACE)
MANA_TOMBS = dungeon("Mana-Tombs", 651, zones.MANA_TOMBS)
OPENING_OF_THE_DARK_PORTAL = dungeon("Opening of the Dark Portal", 655, zones.THE_BLACK_MORASS)
SETHEKK_HALLS = dungeon("Sethekk Halls", 653, zones.SETHEKK_HALLS)
SHADOW_LABYRINTH = dungeon("Shadow Labyrinth", 654, zones.SHADOW_LABYRINTH)
THE_ARCATRAZ = dungeon("The Arcatraz", 660, zones.THE_ARCATRAZ)
THE_BLOOD_FURNACE = dungeon("The Blood Furnace", 648, zones.THE_BLOOD_FURNACE)
THE_BOTANICA = dungeon("The Botanica", 659, zones.THE_BOTANICA)
THE_ESCAPE_FROM_DURNHOLDE = dungeon("The Escape From Durnholde", 652, zones.OLD_HILLSBRAD_FOOTHILLS)
THE_MECHANAR = dungeon("The Mechanar", 658, zones.THE_MECHANAR)
THE_SHATTERED_HALLS = dungeon("The Shattered Halls", 657, zones.THE_SHATTERED_HALLS)
THE_SLAVE_PENS = dungeon("The Slave Pens", 649, zones.THE_SLAVE_PENS)
THE_STEAMVAULT = dungeon("The Steamvault", 656, zones.THE_STEAMVAULT)
UNDERBOG = dungeon("Underbog", 650, zones.THE_UNDERBOG)
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
AHNKAHET_THE_OLD_KINGDOM = dungeon("Ahn'Kahet: The Old Kingdom", 481, zones.AHNKAHET_THE_OLD_KINGDOM)
AZJOL_NERUB = dungeon("Azjol-Nerub", 480, zones.AZJOL_NERUB)
DRAKTHARON_KEEP = dungeon("Drak'Tharon Keep", 482, zones.DRAKTHARON_KEEP)
GUNDRAK = dungeon("Gundrak", 484, zones.GUNDRAK)
HALLS_OF_LIGHTNING = dungeon("Halls of Lightning", 486, zones.HALLS_OF_LIGHTNING)
HALLS_OF_STONE = dungeon("Halls of Stone", 485, zones.HALLS_OF_STONE)
THE_CULLING_OF_STRATHOLME = dungeon("The Culling of Stratholme", 479, zones.THE_CULLING_OF_STRATHOLME)
THE_NEXUS = dungeon("The Nexus", 478, zones.THE_NEXUS)
THE_OCULUS = dungeon("The Oculus", 487, zones.THE_OCULUS)
THE_VIOLET_HOLD = dungeon("The Violet Hold", 483, zones.VIOLET_HOLD)
UTGARDE_KEEP = dungeon("Utgarde Keep", 477, zones.UTGARDE_KEEP)
UTGARDE_PINNACLE = dungeon("Utgarde Pinnacle", 488, zones.UTGARDE_PINNACLE)
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
# The vendors selling a pet for gold all year round. Those of the starting zones and capitals charge 20 to 60 silver, while a quest below
# level 10 pays a few silver.
PET_VENDOR_ZONES = (
    zones.DARNASSUS,
    zones.DUN_MOROGH,
    zones.ELWYNN_FOREST,
    zones.EVERSONG_WOODS,
    zones.NETHERSTORM,
    zones.ORGRIMMAR,
    zones.STORMWIND_CITY,
    zones.STRANGLETHORN_VALE,
    zones.THE_EXODAR,
    zones.THOUSAND_NEEDLES,
    zones.THUNDER_BLUFF,
    zones.UNDERCITY,
)
CAN_I_KEEP_HIM = Achievement("Can I Keep Him?", 1017, None, 10, PET_VENDOR_ZONES)
# Every capital's tabard vendor sells the Guild Tabard for 1 gold, to a character outside a guild too
REPRESENT = Achievement("Represent", 621, None, 15, tuple(zones.CAPITAL_CITIES))
# A barber charges by level, a few copper at level 5, so the capital's own level is enough
SHAVE_AND_A_HAIRCUT = Achievement(
    "Shave and a Haircut", 545, None, None, (zones.IRONFORGE, zones.NETHERSTORM, zones.ORGRIMMAR, zones.STORMWIND_CITY, zones.UNDERCITY)
)
_50_QUESTS_COMPLETED = Achievement("50 Quests Completed", 503, None, 12)
_100_QUESTS_COMPLETED = Achievement("100 Quests Completed", 504, None, 30)
_250_QUESTS_COMPLETED = Achievement("250 Quests Completed", 505, None, 50)
MISC = [CAN_I_KEEP_HIM, REPRESENT, SHAVE_AND_A_HAIRCUT, _50_QUESTS_COMPLETED, _100_QUESTS_COMPLETED, _250_QUESTS_COMPLETED]
