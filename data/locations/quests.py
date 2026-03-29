from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...world import World

from worlds.generic.Rules import set_rule

from ... import regions
from ...conditions import combine_rules, has_all, required_level
from ...options import CharacterClass, CharacterRace
from ..items import zones
from ..items.zones import ZONES_CONTAINER, Zone
from .location_container import LocationContainer
from .location_registry import Location


class Quest(Location):
    def __init__(self, name: str, quest_id: int | list[int], region: str, zones: list[Zone] = [], level: Optional[int] = None, display_zone=True):
        name = f"Quest: {name}"
        if display_zone and len(zones) > 0:
            name += f" ({zones[0].name})"

        super().__init__(name)
        QUESTS_CONTAINER.add(self)
        self.quest_id = quest_id
        self.region = region
        self.zones = zones
        self.level = level


class QuestsContainer(LocationContainer):
    def build_locations(self, world: "World"):
        quests: list[Quest] = []
        match world.options.character_race.value:
            case CharacterRace.option_human:
                quests += [
                    SKIRMISH_AT_ECHO_RIDGE,
                    BOUNTY_ON_GARRICK_PADFOOT,
                    REPORT_TO_GOLDSHIRE,
                    THE_FARGODEEP_MINE,
                    BOUNTY_ON_MURLOCS,
                    WANTED_HOGGER,
                ]
            case CharacterRace.option_dwarf | CharacterRace.option_gnome:
                quests += [
                    THE_STOLEN_JOURNAL,
                    SENIRS_OBSERVATION,
                    A_REFUGEES_QUANDARY,
                    FROSTMANE_HOLD,
                    STOCKING_JETSTEAM,
                    PROTECTING_THE_HERD,
                ]
            case CharacterRace.option_night_elf:
                quests += [
                    CROWN_OF_THE_EARTH,
                    IVERRONS_ANTIDOTE,
                    CROWN_OF_THE_EARTH_2,
                    THE_RELICS_OF_WAKENING,
                    ZENNS_BIDDING,
                    TWISTED_HATRED,
                ]
            case CharacterRace.option_draenei:
                quests += [
                    THE_EMITTER,
                    HEALING_THE_LAKE,
                    TRAVEL_TO_AZURE_WATCH,
                    THE_GREAT_MOONGRAZE_HUNT,
                    TOTEM_OF_VARK,
                    THE_KURKEN_IS_LURKIN,
                ]
            case CharacterRace.option_orc | CharacterRace.option_troll:
                quests += [
                    BURNING_BLADE_MEDALLION,
                    SARKOTH,
                    REPORT_TO_SENJIN_VILLAGE,
                    THWARTING_KOLKAR_AGGRESSION,
                    A_SOLVENT_SPIRIT,
                    DARK_STORMS,
                ]
            case CharacterRace.option_tauren:
                quests += [
                    BREAK_SHARPTUSK,
                    RITE_OF_STRENGTH,
                    RITES_OF_THE_EARTHMOTHER,
                    DWARVEN_DIGGING,
                    POISON_WATER,
                    SUPERVISOR_FIZSPROCKET,
                ]
            case CharacterRace.option_undead:
                quests += [
                    MARLAS_LAST_WISH,
                    THE_RED_MESSENGER,
                    VITAL_INTELLIGENCE,
                    DEATHS_IN_THE_FAMILY,
                    A_PUTRID_TASK,
                    WANTED_MAGGOT_EYE,
                ]
            case CharacterRace.option_blood_elf:
                quests += [
                    FELENDREN_THE_BANISHED,
                    SOLANIANS_BELONGINGS,
                    AIDING_THE_OUTRUNNERS,
                    DEACTIVATING_THE_SPIRE,
                    PELT_COLLECTION,
                    THE_SPEARCRAFTERS_HAMMER,
                ]

        match world.options.character_class:
            case CharacterClass.option_warrior:
                match world.options.character_race:
                    case CharacterRace.option_human:
                        quests.append(BARTLEBYS_MUG)
                    case CharacterRace.option_dwarf | CharacterRace.option_gnome:
                        quests.append(VEJREK)
                    case CharacterRace.option_night_elf:
                        quests.append(VORLUS_VILEHOOF)
                    case CharacterRace.option_draenei:
                        quests.append(STRENGTH_OF_ONE)
                    case CharacterRace.option_orc | CharacterRace.option_troll | CharacterRace.option_tauren:
                        quests.append(PATH_OF_DEFENSE)
                    case CharacterRace.option_undead:
                        quests.append(ULAG_THE_CLEAVER)
                quests.append(THE_AFFRAY)
            case CharacterClass.option_paladin:
                match world.options.character_race:
                    case CharacterRace.option_human:
                        quests.append(THE_TOME_OF_DIVINITY_HUMAN)
                    case CharacterRace.option_dwarf:
                        quests.append(THE_TOME_OF_DIVINITY_DWARF)
                    case CharacterRace.option_draenei:
                        quests.append(REDEMPTION)
                    case CharacterRace.option_blood_elf:
                        quests.append(REDEEMING_THE_DEAD)
            case CharacterClass.option_rogue:
                match world.options.character_race:
                    case CharacterRace.option_human:
                        quests.append(SNATCH_AND_GRAB)
                    case CharacterRace.option_dwarf | CharacterRace.option_gnome:
                        quests.append(ONINS_REPORT)
                    case CharacterRace.option_night_elf:
                        quests.append(DESTINY_CALLS)
                    case CharacterRace.option_orc | CharacterRace.option_troll:
                        quests.append(THE_SHATTERED_HAND)
                    case CharacterRace.option_undead:
                        quests.append(THE_DEATHSTALKERS)
                    case CharacterRace.option_blood_elf:
                        quests.append(RETURN_THE_REPORTS)
            case CharacterClass.option_hunter:
                match world.options.character_race:
                    case CharacterRace.option_dwarf:
                        quests.append(TRAINING_THE_BEAST_DWARF)
                    case CharacterRace.option_night_elf:
                        quests.append(TRAINING_THE_BEAST_NIGHT_ELF)
                    case CharacterRace.option_draenei:
                        quests.append(BEAST_TRAINING_DRAENEI)
                    case CharacterRace.option_orc | CharacterRace.option_troll:
                        quests.append(TRAINING_THE_BEAST_DUROTAR)
                    case CharacterRace.option_tauren:
                        quests.append(TRAINING_THE_BEAST_TAUREN)
                    case CharacterRace.option_blood_elf:
                        quests.append(BEAST_TRAINING_BLOOD_ELF)
            case CharacterClass.option_shaman:
                match world.options.character_race:
                    case CharacterRace.option_draenei:
                        quests += [CALL_OF_EARTH_DRAENEI, CALL_OF_FIRE_A, CALL_OF_WATER_A]
                    case CharacterRace.option_orc | CharacterRace.option_troll:
                        quests += [CALL_OF_EARTH_DUROTAR, CALL_OF_FIRE_H, CALL_OF_WATER_H]
                    case CharacterRace.option_tauren:
                        quests += [CALL_OF_EARTH_TAUREN, CALL_OF_FIRE_H, CALL_OF_WATER_H]
            case CharacterClass.option_druid:
                match world.options.character_race:
                    case CharacterRace.option_night_elf:
                        quests.append(BODY_AND_HEART_A)
                    case CharacterRace.option_tauren:
                        quests.append(BODY_AND_HEART_H)
            case CharacterClass.option_mage:
                match world.options.character_race:
                    case CharacterRace.option_human:
                        quests.append(MIRROR_LAKE)
                    case CharacterRace.option_gnome:
                        quests.append(MAGETASTIC_GIZMONITOR)
                    case CharacterRace.option_draenei:
                        quests.append(CONTROL)
                    case CharacterRace.option_undead:
                        quests.append(THE_BALNIR_FARMSTEAD)
                    case CharacterRace.option_troll:
                        quests.append(JUJU_HEAPS)
                    case CharacterRace.option_blood_elf:
                        quests.append(RECENTLY_LIVING)
            case CharacterClass.option_warlock:
                match world.options.character_race:
                    case CharacterRace.option_human | CharacterRace.option_gnome:
                        quests += [THE_BINDING_VOIDWALKER_A, THE_BINDING_SUCCUBUS_A, THE_BINDING_FELHUNTER]
                    case CharacterRace.option_orc:
                        quests += [THE_BINDING_VOIDWALKER_ORC, THE_BINDING_SUCCUBUS_H, THE_BINDING_FELHUNTER]
                    case CharacterRace.option_undead:
                        quests += [THE_BINDING_VOIDWALKER_UNDEAD, THE_BINDING_SUCCUBUS_H, THE_BINDING_FELHUNTER]
                    case CharacterRace.option_blood_elf:
                        quests += [THE_RUNE_OF_SUMMONING, THE_BINDING_SUCCUBUS_H, THE_BINDING_FELHUNTER]
            case CharacterClass.option_priest:
                match world.options.character_race:
                    case CharacterRace.option_human:
                        quests.append(GARMENTS_OF_THE_LIGHT_HUMAN)
                    case CharacterRace.option_dwarf:
                        quests.append(GARMENTS_OF_THE_LIGHT_DWARF)
                    case CharacterRace.option_night_elf:
                        quests.append(GARMENTS_OF_THE_MOON)
                    case CharacterRace.option_draenei:
                        quests.append(HELP_TAVARA)
                    case CharacterRace.option_undead:
                        quests.append(GARMENTS_OF_DARKNESS)
                    case CharacterRace.option_troll:
                        quests.append(GARMENTS_OF_SPIRITUALITY)
                    case CharacterRace.option_blood_elf:
                        quests.append(CLEANSING_THE_SCAR)

        if world.is_alliance():
            quests += [
                THE_PEOPLES_MILITIA,
                THELSAMAR_BLOOD_SAUSAGES,
                LEARNING_FROM_THE_CRYSTALS,
                TOOLS_OF_THE_HIGHBORNE,
                ASSESSING_THE_THREAT,
                THE_NIGHT_WATCH,
                CLAWS_FROM_THE_DEEP,
                THE_ZORAM_STRAND,
                RECLAIMING_THE_CHARRED_VALE,
                SALT_FLAT_VENOM,
                DOWN_THE_COAST,
                CENTAUR_BOUNTY_A,
                WORTH_ITS_WEIGHT_IN_GOLD,
                A_DWARF_AND_HIS_TOOLS,
                TRAITORS_AMONG_US,
                AGAINST_THE_HATECREST,
                WITHERBARK_CAGES,
                CLEAR_THE_WAY,
                FIFTY_YEP,
            ]
        else:
            quests += [
                INVESTIGATE_ANDAROTH,
                A_RECIPE_FOR_DEATH,
                DISRUPT_THE_ATTACKS,
                ELIXIR_OF_SUFFERING,
                NAGA_AT_THE_ZORAM_STRAND,
                ARACHNOPHOBIA,
                PACIFY_THE_CENTAUR,
                CENTAUR_BOUNTY_H,
                FOUL_MAGICS,
                BADLANDS_REAGENT_RUN,
                LACK_OF_SURPLUS,
                WAR_ON_THE_WOODPAW,
                THE_ESSENCE_OF_ENMITY,
                CANNIBALISTIC_COUSINS,
                SCARLET_DIVERSIONS,
                BROODLING_ESSENCE,
            ]
        quests += [
            TIGER_MASTERY,
            PANTHER_MASTERY,
            RAPTOR_MASTERY,
            FIERY_MENACE,
            A_LAND_FILLED_WITH_HATRED,
            WANTED_CALIPH_SCORPIDSTING,
            A_BOARS_VITALITY,
            FORCES_OF_JAEDENAR,
            ROLL_THE_BONES,
            DEFENDERS_OF_DARROWSHIRE,
            DEADLY_DESERT_VENOM,
            ARE_WE_THERE_YETI,
        ]

        return quests

    def get_slot_data(self, world: "World"):
        l: list[list[int]] = []
        for loc in self.build_locations(world):
            if isinstance(loc.quest_id, list):
                l += [[quest_id, loc.id] for quest_id in loc.quest_id]
            else:
                l.append([loc.quest_id, loc.id])
        return l

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        locations = self.build_locations(world)
        return [(l.region, l) for l in locations]

    def set_rules(self, world: "World"):
        zones_in_pool = ZONES_CONTAINER.build_pool(world)
        for q in QUESTS_CONTAINER.build_locations(world):
            if len(q.zones) > 0:
                filtered_zones = list(filter(lambda z: z in zones_in_pool, q.zones))
                zones_rule = has_all([z.name for z in filtered_zones], world)
                level_rule = required_level(q.level, world) if q.level is not None else None
                set_rule(world.get_location(q.name), combine_rules(zones_rule, level_rule))


QUESTS_CONTAINER = QuestsContainer()

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

# Alliance 01-05
SKIRMISH_AT_ECHO_RIDGE = Quest("Skirmish at Echo Ridge", 21, L01, [zones.ELWYNN_FOREST])
BOUNTY_ON_GARRICK_PADFOOT = Quest("Bounty on Garrick Padfoot", 6, L01, [zones.ELWYNN_FOREST])
REPORT_TO_GOLDSHIRE = Quest("Report to Goldshire", 54, L01, [zones.ELWYNN_FOREST])
THE_STOLEN_JOURNAL = Quest("The Stolen Journal", 218, L01, [zones.DUN_MOROGH])
SENIRS_OBSERVATION = Quest("Senir's Observations", 420, L01, [zones.DUN_MOROGH])
A_REFUGEES_QUANDARY = Quest("A Refugee's Quandary", 3361, L01, [zones.DUN_MOROGH])
CROWN_OF_THE_EARTH = Quest("Crown of the Earth", 921, L01, [zones.TELDRASSIL])
IVERRONS_ANTIDOTE = Quest("Iverron's Antidote", 3522, L01, [zones.TELDRASSIL])
CROWN_OF_THE_EARTH_2 = Quest("Crown of the Earth (2)", 928, L01, [zones.TELDRASSIL])
THE_EMITTER = Quest("The Emitter", 9312, L01, [zones.AZUREMYST_ISLE])
HEALING_THE_LAKE = Quest("Healing the Lake", 9294, L01, [zones.AZUREMYST_ISLE])
TRAVEL_TO_AZURE_WATCH = Quest("Travel to Azure Watch", 9313, L01, [zones.AZUREMYST_ISLE])

# Horde 01-05
BURNING_BLADE_MEDALLION = Quest("Burning Blade Medallion", 794, L01, [zones.DUROTAR])
SARKOTH = Quest("Sarkoth", 790, L01, [zones.DUROTAR])
REPORT_TO_SENJIN_VILLAGE = Quest("Report to Sen'jin Village", 805, L01, [zones.DUROTAR])
BREAK_SHARPTUSK = Quest("Break Sharptusk!", 3376, L01, [zones.MULGORE])
RITE_OF_STRENGTH = Quest("Rite of Strength", 757, L01, [zones.MULGORE])
RITES_OF_THE_EARTHMOTHER = Quest("Rites of the Earthmother", 763, L01, [zones.MULGORE])
MARLAS_LAST_WISH = Quest("Marla's Last Wish", 6395, L01, [zones.TIRISFAL_GLADES])
THE_RED_MESSENGER = Quest("The Red Messenger", 382, L01, [zones.TIRISFAL_GLADES])
VITAL_INTELLIGENCE = Quest("Vital Intelligence", 383, L01, [zones.TIRISFAL_GLADES])
FELENDREN_THE_BANISHED = Quest("Felendren the Banished", 8335, L01, [zones.EVERSONG_WOODS])
SOLANIANS_BELONGINGS = Quest("Solanian's Belongings", 8330, L01, [zones.EVERSONG_WOODS])
AIDING_THE_OUTRUNNERS = Quest("Aiding the Outrunners", 8347, L01, [zones.EVERSONG_WOODS])

# Alliance 05-10
THE_FARGODEEP_MINE = Quest("The Fargodeep Mine", 62, L01, [zones.ELWYNN_FOREST])
BOUNTY_ON_MURLOCS = Quest("Bounty on Murlocs", 46, L01, [zones.ELWYNN_FOREST])
WANTED_HOGGER = Quest('Wanted: "Hogger"', 176, L01, [zones.ELWYNN_FOREST])
FROSTMANE_HOLD = Quest("Frostmane Hold", 287, L01, [zones.DUN_MOROGH])
STOCKING_JETSTEAM = Quest("Stocking Jetsteam", 317, L01, [zones.DUN_MOROGH])
PROTECTING_THE_HERD = Quest("Protecting the Herd", 314, L01, [zones.DUN_MOROGH])
THE_RELICS_OF_WAKENING = Quest("The Relics of Wakening", 483, L01, [zones.TELDRASSIL])
ZENNS_BIDDING = Quest("Zenn's Bidding", 488, L01, [zones.TELDRASSIL])
TWISTED_HATRED = Quest("Twisted Hatred", 932, L01, [zones.TELDRASSIL])
THE_GREAT_MOONGRAZE_HUNT = Quest("The Great Moongraze Hunt", 9454, L01, [zones.AZUREMYST_ISLE])
TOTEM_OF_VARK = Quest("Totem of Vark", 9542, L01, [zones.AZUREMYST_ISLE])
THE_KURKEN_IS_LURKIN = Quest("The Kurken is Lurkin'", 9570, L01, [zones.AZUREMYST_ISLE])

# Horde 05-10
THWARTING_KOLKAR_AGGRESSION = Quest("Thwarting Kolkar Aggression", 786, L01, [zones.DUROTAR])
A_SOLVENT_SPIRIT = Quest("A Solvent Spirit", 818, L01, [zones.DUROTAR])
DARK_STORMS = Quest("Dark Storms", 806, L01, [zones.DUROTAR])
DWARVEN_DIGGING = Quest("Dwarven Digging", 746, L01, [zones.MULGORE])
POISON_WATER = Quest("Poison Water", 748, L01, [zones.MULGORE])
SUPERVISOR_FIZSPROCKET = Quest("Supervisor Fizsprocket", 765, L01, [zones.MULGORE])
DEATHS_IN_THE_FAMILY = Quest("Deaths in the Family", 354, L01, [zones.TIRISFAL_GLADES])
A_PUTRID_TASK = Quest("A Putrid Task", 404, L01, [zones.TIRISFAL_GLADES])
WANTED_MAGGOT_EYE = Quest("Wanted: Maggot Eye", 398, L01, [zones.TIRISFAL_GLADES])
DEACTIVATING_THE_SPIRE = Quest("Deactivating the Spire", 8889, L01, [zones.EVERSONG_WOODS])
PELT_COLLECTION = Quest("Pelt Collection", 8491, L01, [zones.EVERSONG_WOODS])
THE_SPEARCRAFTERS_HAMMER = Quest("The Spearcrafter's Hammer", 8477, L01, [zones.EVERSONG_WOODS])

# Alliance 10-15
THE_PEOPLES_MILITIA = Quest("The People's Militia", 12, L10, [zones.WESTFALL])
THELSAMAR_BLOOD_SAUSAGES = Quest("Thelsamar Blood Sausages", 418, L10, [zones.LOCH_MODAN])
LEARNING_FROM_THE_CRYSTALS = Quest("Learning from the Crystals", 9581, L10, [zones.BLOODMYST_ISLE])
TOOLS_OF_THE_HIGHBORNE = Quest("Tools of the Highborne", 958, L10, [zones.DARKSHORE])

# Horde 10-15
INVESTIGATE_ANDAROTH = Quest("Investigate An'daroth", 9160, L10, [zones.GHOSTLANDS])
A_RECIPE_FOR_DEATH = Quest("A Recipe For Death", 447, L10, [zones.SILVERPINE_FOREST])
DISRUPT_THE_ATTACKS = Quest("Disrupt the Attacks", 871, L10, [zones.THE_BARRENS])

# Alliance 15-20
ASSESSING_THE_THREAT = Quest("Assessing the Threat", 246, L15, [zones.REDRIDGE_MOUNTAINS])

# Alliance 20-25
THE_NIGHT_WATCH = Quest("The Night Watch", 56, L20, [zones.DUSKWOOD])
CLAWS_FROM_THE_DEEP = Quest("Claws from the Deep", 279, L20, [zones.WETLANDS])
THE_ZORAM_STRAND = Quest("The Zoram Strand", 1008, L20, [zones.ASHENVALE])
RECLAIMING_THE_CHARRED_VALE = Quest("Reclaiming the Charred Vale", 1057, L20, [zones.STONETALON_MOUNTAINS])

# Horde 20-25
ELIXIR_OF_SUFFERING = Quest("Elixir of Suffering", 496, L20, [zones.HILLSBRAD_FOOTHILLS])
NAGA_AT_THE_ZORAM_STRAND = Quest("Naga at the Zoram Strand", 6442, L20, [zones.ASHENVALE])
ARACHNOPHOBIA = Quest("Arachnophobia", 6284, L20, [zones.STONETALON_MOUNTAINS])

# Alliance 25-30
SALT_FLAT_VENOM = Quest("Salt Flat Venom", 1104, L25, [zones.THOUSAND_NEEDLES])

# Horde 25-30
PACIFY_THE_CENTAUR = Quest("Pacify the Centaur", 4841, L25, [zones.THOUSAND_NEEDLES])

# 30-35
DOWN_THE_COAST = Quest("Down the Coast", 536, L30, [zones.HILLSBRAD_FOOTHILLS])
TIGER_MASTERY = Quest("Tiger Mastery", 188, L30, [zones.STRANGLETHORN_VALE])
CENTAUR_BOUNTY_A = Quest("Centaur Bounty [A]", 1387, L30, [zones.DESOLACE])
CENTAUR_BOUNTY_H = Quest("Centaur Bounty [H]", 1366, L30, [zones.DESOLACE])
FOUL_MAGICS = Quest("Foul Magics", 671, L30, [zones.ARATHI_HIGHLANDS])

# 35-40
WORTH_ITS_WEIGHT_IN_GOLD = Quest("Worth Its Weight in Gold", 691, L35, [zones.ARATHI_HIGHLANDS])
A_DWARF_AND_HIS_TOOLS = Quest("A Dwarf and His Tools", 719, L35, [zones.BADLANDS])
TRAITORS_AMONG_US = Quest("Traitors Among Us", 11126, L35, [zones.DUSTWALLOW_MARSH])
PANTHER_MASTERY = Quest("Panther Mastery", 193, L35, [zones.STRANGLETHORN_VALE])
BADLANDS_REAGENT_RUN = Quest("Badlands Reagent Run", 2258, L35, [zones.BADLANDS])
LACK_OF_SURPLUS = Quest("Lack of Surplus", 698, L35, [zones.SWAMP_OF_SORROWS])

# 40-45
AGAINST_THE_HATECREST = Quest("Against the Hatecrest", 2869, L40, [zones.FERALAS])
WAR_ON_THE_WOODPAW = Quest("War on the Woodpaw", 2862, L40, [zones.FERALAS])
THE_ESSENCE_OF_ENMITY = Quest("The Essence of Enmity", 11161, L40, [zones.DUSTWALLOW_MARSH])
RAPTOR_MASTERY = Quest("Raptor Mastery", 197, L40, [zones.STRANGLETHORN_VALE])
WITHERBARK_CAGES = Quest("Witherbark Cages", 2988, L40, [zones.THE_HINTERLANDS])

# 45-50
FIERY_MENACE = Quest("Fiery Menace!", 7724, L45, [zones.SEARING_GORGE])
A_LAND_FILLED_WITH_HATRED = Quest("A Land Filled with Hatred", 5536, L45, [zones.AZSHARA])
WANTED_CALIPH_SCORPIDSTING = Quest("WANTED: Caliph Scorpidsting", 2781, L45, [zones.TANARIS])
CANNIBALISTIC_COUSINS = Quest("Cannibalistic Cousins", 7844, L45, [zones.THE_HINTERLANDS])
A_BOARS_VITALITY = Quest("A Boar's Vitality", 2583, L45, [zones.BLASTED_LANDS])

# 50-55
FORCES_OF_JAEDENAR = Quest("Forces of Jaedenar", 5155, L50, [zones.FELWOOD])
ROLL_THE_BONES = Quest("Roll the Bones", 3882, L50, [zones.UNGORO_CRATER])
SCARLET_DIVERSIONS = Quest("Scarlet Diversions", 5096, L50, [zones.WESTERN_PLAGUELANDS, zones.TIRISFAL_GLADES])
CLEAR_THE_WAY = Quest("Clear the Way", 5092, L50, [zones.WESTERN_PLAGUELANDS])

# 55-60
FIFTY_YEP = Quest("FIFTY! YEP!", 4283, L55, [zones.BURNING_STEPPES])
BROODLING_ESSENCE = Quest("Broodling Essence", 4726, L55, [zones.BURNING_STEPPES])
DEFENDERS_OF_DARROWSHIRE = Quest("Defenders of Darrowshire", 5211, L55, [zones.EASTERN_PLAGUELANDS])
DEADLY_DESERT_VENOM = Quest("Deadly Desert Venom", 8277, L55, [zones.SILITHUS])
ARE_WE_THERE_YETI = Quest("Are We There, Yeti?", 3783, L55, [zones.WINTERSPRING])

# Class quests
# Warrior
BARTLEBYS_MUG = Quest("Bartleby's Mug", 1665, L01, [zones.ELWYNN_FOREST], level=10)
VEJREK = Quest("Vejrek", 1678, L01, [zones.DUN_MOROGH], level=10)
VORLUS_VILEHOOF = Quest("Vorlus Vilehoof", 1683, L01, [zones.TELDRASSIL], level=10)
STRENGTH_OF_ONE = Quest("Strength of One", 9582, L01, [zones.AZUREMYST_ISLE], level=10)
PATH_OF_DEFENSE = Quest("Path of Defense", 1498, L01, [zones.THE_BARRENS], level=10)
ULAG_THE_CLEAVER = Quest("Ulag the Cleaver", 1819, L01, [zones.TIRISFAL_GLADES], level=10)
THE_AFFRAY = Quest("The Affray", 1719, L30, [zones.THE_BARRENS], level=30)

# Paladin
THE_TOME_OF_DIVINITY_HUMAN = Quest("The Tome of Divinity", 1788, L10, [zones.ELWYNN_FOREST], level=12)
THE_TOME_OF_DIVINITY_DWARF = Quest("The Tome of Divinity", 1785, L10, [zones.DUN_MOROGH], level=12)
REDEMPTION = Quest("Redemption", 9600, L10, [zones.AZUREMYST_ISLE, zones.BLOODMYST_ISLE], level=12)
REDEEMING_THE_DEAD = Quest("Redeeming the Dead", 9685, L10, [zones.EVERSONG_WOODS], level=12)

# Priest
GARMENTS_OF_THE_LIGHT_HUMAN = Quest("Garments of the Light", 5624, L01, [zones.ELWYNN_FOREST], level=5)
GARMENTS_OF_THE_LIGHT_DWARF = Quest("Garments of the Light", 5625, L01, [zones.DUN_MOROGH], level=5)
GARMENTS_OF_THE_MOON = Quest("Garments of the Moon", 5621, L01, [zones.TELDRASSIL], level=5)
HELP_TAVARA = Quest("Help Tavara", 9586, L01, [zones.AZUREMYST_ISLE], level=5)
GARMENTS_OF_DARKNESS = Quest("Garments of Darkness", 5650, L01, [zones.TIRISFAL_GLADES], level=5)
GARMENTS_OF_SPIRITUALITY = Quest("Garments of Spirituality", 5648, L01, [zones.DUROTAR], level=5)
CLEANSING_THE_SCAR = Quest("Cleansing the Scar", 9489, L01, [zones.EVERSONG_WOODS], level=5)

# Mage
MIRROR_LAKE = Quest("Mirror Lake", 1861, L01, [zones.ELWYNN_FOREST], level=10)
MAGETASTIC_GIZMONITOR = Quest("Mage-tastic Gizmonitor", 1880, L01, [zones.DUN_MOROGH], level=10)
CONTROL = Quest("Control", 9595, L01, [zones.AZUREMYST_ISLE], level=10)
THE_BALNIR_FARMSTEAD = Quest("The Balnir Farmstead", 1882, L01, [zones.TIRISFAL_GLADES], level=10)
JUJU_HEAPS = Quest("Ju-Ju Heaps", 1884, L01, [zones.DUROTAR], level=10)
RECENTLY_LIVING = Quest("Recently Living", 9404, L01, [zones.EVERSONG_WOODS], level=10)

# Hunter
TRAINING_THE_BEAST_DWARF = Quest("Training the Beast", 6086, L01, [zones.DUN_MOROGH], level=10)
TRAINING_THE_BEAST_NIGHT_ELF = Quest("Training the Beast", 6103, L01, [zones.TELDRASSIL], level=10)
BEAST_TRAINING_DRAENEI = Quest("Beast Training", 9675, L01, [zones.AZUREMYST_ISLE], level=10)
TRAINING_THE_BEAST_DUROTAR = Quest("Training the Beast", 6081, L01, [zones.DUROTAR], level=10)
TRAINING_THE_BEAST_TAUREN = Quest("Training the Beast", 6089, L01, [zones.MULGORE], level=10)
BEAST_TRAINING_BLOOD_ELF = Quest("Beast Training", 9673, L01, [zones.EVERSONG_WOODS], level=10)

# Shaman
CALL_OF_EARTH_DUROTAR = Quest("Call of Earth", 1518, L01, [zones.DUROTAR], level=4)
CALL_OF_EARTH_TAUREN = Quest("Call of Earth", 1521, L01, [zones.MULGORE], level=4)
CALL_OF_EARTH_DRAENEI = Quest("Call of Earth", 9451, L01, [zones.AZUREMYST_ISLE], level=4)
CALL_OF_FIRE_A = Quest("Call of Fire", 9555, L01, [zones.AZUREMYST_ISLE], level=10)
CALL_OF_FIRE_H = Quest("Call of Fire", 1527, L10, [zones.DUROTAR, zones.THE_BARRENS], level=10)
CALL_OF_WATER_A = Quest("Call of Water", 9509, L15, [zones.BLOODMYST_ISLE, zones.AZUREMYST_ISLE], level=20)
CALL_OF_WATER_H = Quest("Call of Water", 96, L15, [zones.THE_BARRENS, zones.SILVERPINE_FOREST], level=20)
CALL_OF_AIR_A = Quest("Call of Air", 9554, L25, [zones.AZUREMYST_ISLE], level=30)
CALL_OF_AIR_H = Quest("Call of Air", [1531, 1532], L25, [zones.THOUSAND_NEEDLES, zones.MULGORE, zones.DUROTAR], level=30)

# Druid
BODY_AND_HEART_A = Quest("Body and Heart", 6001, L01, [zones.TELDRASSIL, zones.DARKSHORE], level=10)
BODY_AND_HEART_H = Quest("Body and Heart", 6002, L01, [zones.MULGORE, zones.THE_BARRENS], level=10)

# Warlock
THE_BINDING_VOIDWALKER_A = Quest("The Binding (1)", 1689, L01, [zones.ELWYNN_FOREST], level=10)
THE_BINDING_VOIDWALKER_ORC = Quest("The Binding (1)", 1504, L01, [zones.DUROTAR], level=10)
THE_BINDING_VOIDWALKER_UNDEAD = Quest("The Binding (1)", 1471, L01, [zones.TIRISFAL_GLADES], level=10)
THE_RUNE_OF_SUMMONING = Quest("The Rune of Summoning", 9619, L01, [zones.EVERSONG_WOODS, zones.GHOSTLANDS], level=10)
THE_BINDING_SUCCUBUS_A = Quest("The Binding (2)", 1739, L15, [zones.ELWYNN_FOREST, zones.ASHENVALE], level=20)
THE_BINDING_SUCCUBUS_H = Quest(
    "The Binding (2)",
    [1513, 1474],
    L15,
    [zones.DUROTAR, zones.THE_BARRENS, zones.STONETALON_MOUNTAINS, zones.TIRISFAL_GLADES, zones.SILVERPINE_FOREST],
    level=20,
)
THE_BINDING_FELHUNTER = Quest(
    "The Binding (3)",
    1795,
    L25,
    [
        zones.THE_BARRENS,
        zones.HILLSBRAD_FOOTHILLS,
        zones.THOUSAND_NEEDLES,
        zones.WETLANDS,
        zones.ELWYNN_FOREST,
        zones.DUN_MOROGH,
        zones.TIRISFAL_GLADES,
    ],
    level=30,
)

# Rogue
SNATCH_AND_GRAB = Quest("Snatch and Grab", 2206, L01, [zones.ELWYNN_FOREST], level=10)
ONINS_REPORT = Quest("Onin's Report", 2239, L01, [zones.DUN_MOROGH], level=10)
DESTINY_CALLS = Quest("Destiny Calls", 2242, L01, [zones.TELDRASSIL], level=10)
THE_SHATTERED_HAND = Quest("The Shattered Hand", 1858, L01, [zones.DUROTAR, zones.THE_BARRENS], level=10)
THE_DEATHSTALKERS = Quest("The Deathstalkers", 14418, L01, [zones.TIRISFAL_GLADES], level=10)
RETURN_THE_REPORTS = Quest("Return the Reports", 9618, L01, [zones.GHOSTLANDS, zones.EVERSONG_WOODS], level=10)
