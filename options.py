import random
from collections import Counter
from dataclasses import dataclass
from typing import Any, Self

from Options import (
    Accessibility,
    Choice,
    DeathLink,
    NamedRange,
    OptionError,
    OptionGroup,
    PerGameCommonOptions,
    ProgressionBalancing,
    StartInventoryPool,
    Toggle,
)


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


class RerollableChoice(Choice):
    """A choice that keeps the YAML weight of each value, so the world may reroll it from them."""

    # Generate.py then hands from_any the YAML value as written instead of drawing one from its weights.
    supports_weighting = False

    def __init__(self, value: int):
        super().__init__(value)
        self.weights: dict[int, float] = {value: 1}

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, list):
            data = Counter(data)
        elif not isinstance(data, dict):
            data = {data: 1}
        weights: dict[int, float] = {}
        for key, weight in data.items():
            values = list(cls.name_lookup) if str(key).lower() == "random" else [super().from_any(key).value]
            for value in values:
                weights[value] = weights.get(value, 0) + int(weight) / len(values)
        weights = {value: weight for value, weight in weights.items() if weight > 0}
        if not weights:
            raise OptionError("All options are weighted as zero.")
        option = cls(random.choices(list(weights), list(weights.values()))[0])
        option.weights = weights
        return option


class CharacterRace(RerollableChoice):
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


class CharacterClass(RerollableChoice):
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
    # The races each class is open to, by CharacterRace value.
    races = {
        option_warrior: [1, 2, 3, 4, 5, 6, 7, 8, 11],
        option_paladin: [1, 3, 10, 11],
        option_hunter: [2, 3, 4, 6, 8, 10, 11],
        option_rogue: [1, 2, 3, 4, 5, 7, 8, 10],
        option_priest: [1, 3, 4, 5, 8, 10, 11],
        option_shaman: [2, 6, 8, 11],
        option_mage: [1, 5, 7, 8, 10, 11],
        option_warlock: [1, 2, 5, 7, 10],
        option_druid: [4, 6],
    }


# Every (race, class) pair a character can be created as.
PLAYABLE_COMBINATIONS = [(race, character_class) for character_class, races in CharacterClass.races.items() for race in races]


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

    def __post_init__(self) -> None:
        # Rerolled as the options are assembled rather than in generate_early, so that what reads them first (such as
        # --csv_output) already sees the final pair. Like the YAML draw itself, this uses Archipelago's seeded global random.
        race, character_class = self.character_race, self.character_class
        if (race.value, character_class.value) in PLAYABLE_COMBINATIONS:
            return

        combinations = [
            (race_id, class_id) for race_id, class_id in PLAYABLE_COMBINATIONS if race_id in race.weights and class_id in character_class.weights
        ]
        # With nothing to reroll into, the pair is left for generate_early to report under the player's name.
        if combinations:
            # Weighting each combination by the YAML weights of its race and class is the same as rerolling both until they make one.
            weights = [race.weights[race_id] * character_class.weights[class_id] for race_id, class_id in combinations]
            race.value, character_class.value = random.choices(combinations, weights)[0]


option_groups = [
    OptionGroup("General Options", [Goal]),
    OptionGroup("Character Options", [CharacterRace, CharacterClass]),
    OptionGroup("Quest Options", [QuestsDensity, QuestsAllStartingZones, QuestsMaxPartySize, QuestsIncludeDungeons]),
    OptionGroup("Gear Options", [GearRewardLevelWindow, GearIncludeAllArmorTypes]),
    OptionGroup("Spell Options", [SpellsRandomizeStarterAbilities]),
    OptionGroup("Advanced Options", [DeathLink, ProgressionBalancing, Accessibility]),
]

option_presets = {}
