from dataclasses import dataclass

from Options import Accessibility, Choice, DeathLink, NamedRange, OptionGroup, PerGameCommonOptions, ProgressionBalancing, StartInventoryPool, Toggle


class Goal(Choice):
    """
    Your goal for this playthrough.
    Classic Dungeonmaster: Clear the classic 5-man dungeons
    Outland Dungeonmaster: Clear the Burning Crusade 5-man dungeons
    Northrend Dungeonmaster: Clear the Wrath of the Lich King 5-man dungeons
    Level 60: Reach level 60
    Level 70: Reach level 70
    Level 80: Reach level 80
    """

    display_name = "Goal"

    option_classic_dungeonmaster = 1283
    option_outland_dungeonmaster = 1284
    option_northrend_dungeonmaster = 1288
    option_level_60 = 11
    option_level_70 = 12
    option_level_80 = 13

    default = option_classic_dungeonmaster


class CharacterRace(Choice):
    """
    Your character's race.
    """

    display_name = "Race"

    option_human = 1
    option_dwarf = 3
    option_night_elf = 4
    option_gnome = 7
    option_draenei = 11
    option_orc = 2
    option_undead = 5
    option_tauren = 6
    option_troll = 8
    option_blood_elf = 10

    default = option_human
    alliance = [option_human, option_dwarf, option_night_elf, option_gnome, option_draenei]
    horde = [option_orc, option_undead, option_tauren, option_troll, option_blood_elf]


class CharacterClass(Choice):
    """
    Your character's class.
    """

    display_name = "Class"

    option_warrior = 1
    option_paladin = 2
    option_hunter = 3
    option_rogue = 4
    option_priest = 5
    option_shaman = 7
    option_mage = 8
    option_warlock = 9
    option_druid = 11

    default = option_warrior
    # Warriors run on rage and rogues on energy, so anything that restores mana is dead weight
    # for them.
    no_mana = [option_warrior, option_rogue]


class QuestsAllStartingZones(Toggle):
    """
    Include quests from other races' starting zones (levels 1-10).
    """

    display_name = "All starting zones"


class QuestsIncludeDungeons(Toggle):
    """
    Include quests that take place inside dungeons.
    """

    display_name = "Dungeons"


class QuestsDensity(NamedRange):
    """
    Percentage of the available quests turned into locations.
    Quests are picked at random, with a quota per level bracket so that every bracket keeps a comparable share of locations.
    Brackets will always have at least 5 quests, no matter how low this is set.
    """

    display_name = "Quest density"

    range_start = 10
    range_end = 100
    default = 25

    special_range_names = {
        "minimal": 10,
        "sparse": 25,
        "half": 50,
        "most": 75,
        "all": 100,
    }


class QuestsMaxPartySize(NamedRange):
    """
    Highest suggested party size for a quest to become a location.
    "Solo" keeps only the quests one player can finish alone, and every step above it opens up the group quests written for that many players.
    """

    display_name = "Maximum party size"

    range_start = 1
    range_end = 5
    default = 1

    special_range_names = {
        "solo": 1,
        "duo": 2,
        "full_group": 5,
    }


class GearRewardLevelWindow(NamedRange):
    """
    How many levels away you can be from a piece of gear's required level for it to be included in the random gear pool.
    The window widens automatically until it has at least a few gear pieces to choose from, so a low setting value is a preference rather than a guarantee.
    """

    display_name = "Reward level window"

    range_start = 0
    range_end = 10
    default = 3

    special_range_names = {
        "closest": 0,
        "narrow": 1,
        "standard": 3,
        "wide": 5,
        "very_wide": 10,
    }


class GearIncludeAllArmorTypes(Toggle):
    """
    Include armor of any type your class can wear, instead of only the heaviest one available. Can be worth enabling if you intend on playing a caster specialization.

    No: a paladin would receive mail then plate around level 40; a druid would only ever receive leather.
    Yes: a paladin would receive cloth, leather, mail and plate; a druid would receive cloth and leather.
    """

    display_name = "All armor types"


class SpellsRandomizeStarterAbilities(Toggle):
    """
    Shuffle away the abilities your character should have on creation, such as a mage's Fireball or a warrior's Heroic Strike.

    No: you keep your starting kit, and only the spells you would normally train become checks.
    Yes: your starting abilities are moved to the multiworld, and your class trainer sells their checks like any other spell.
    """

    display_name = "Randomize starter abilities"


@dataclass
class Options(PerGameCommonOptions):
    goal: Goal
    character_race: CharacterRace
    character_class: CharacterClass
    quests_density: QuestsDensity
    quests_all_starting_zones: QuestsAllStartingZones
    quests_include_dungeons: QuestsIncludeDungeons
    quests_max_party_size: QuestsMaxPartySize
    gear_reward_level_window: GearRewardLevelWindow
    gear_include_all_armor_types: GearIncludeAllArmorTypes
    spells_randomize_starter_abilities: SpellsRandomizeStarterAbilities
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool


option_groups = [
    OptionGroup("General Options", [Goal]),
    OptionGroup("Character Options", [CharacterRace, CharacterClass]),
    OptionGroup("Quest Options", [QuestsDensity, QuestsAllStartingZones, QuestsMaxPartySize, QuestsIncludeDungeons]),
    OptionGroup("Gear Options", [GearRewardLevelWindow, GearIncludeAllArmorTypes]),
    OptionGroup("Spell Options", [SpellsRandomizeStarterAbilities]),
    OptionGroup("Advanced Options", [DeathLink, ProgressionBalancing, Accessibility]),
]

option_presets = {}
