from dataclasses import dataclass

from Options import Accessibility, Choice, DeathLink, OptionGroup, PerGameCommonOptions, ProgressionBalancing, StartInventoryPool


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


@dataclass
class Options(PerGameCommonOptions):
    goal: Goal
    character_race: CharacterRace
    character_class: CharacterClass
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool


option_groups = [
    OptionGroup("General Options", [Goal]),
    OptionGroup("Character Options", [CharacterRace, CharacterClass]),
    OptionGroup("Advanced Options", [DeathLink, ProgressionBalancing, Accessibility]),
]

option_presets = {}
