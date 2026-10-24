import random
from collections import Counter
from dataclasses import dataclass
from typing import Any, Self

from Options import (
    Accessibility,
    Choice,
    DeathLink,
    DefaultOnToggle,
    NamedRange,
    OptionCounter,
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
    Level 10 to 80: Reach that level, which the seed is capped at
    """

    display_name = "Goal"

    # Each value is the id of the achievement that completes the goal
    option_classic_dungeonmaster = 1283
    option_outland_dungeonmaster = 1284
    option_northrend_dungeonmaster = 1288
    option_level_10 = 6
    option_level_20 = 7
    option_level_30 = 8
    option_level_40 = 9
    option_level_50 = 10
    option_level_60 = 11
    option_level_70 = 12
    option_level_80 = 13

    default = option_level_60

    level_caps = {
        option_classic_dungeonmaster: 60,
        option_outland_dungeonmaster: 70,
        option_northrend_dungeonmaster: 80,
        option_level_10: 10,
        option_level_20: 20,
        option_level_30: 30,
        option_level_40: 40,
        option_level_50: 50,
        option_level_60: 60,
        option_level_70: 70,
        option_level_80: 80,
    }

    # Won the moment the character reaches the cap, so nothing asking for the cap itself is ever played
    level_goals = [
        option_level_10,
        option_level_20,
        option_level_30,
        option_level_40,
        option_level_50,
        option_level_60,
        option_level_70,
        option_level_80,
    ]


class RandomizeLevelUps(DefaultOnToggle):
    """
    Shuffle the Level Up items into the multiworld.

    No: each "Level" location holds a Level Up, so earning the experience for a level gives you that level, as in the base game.
    Yes: your Level Ups can be found anywhere in the multiworld, and the "Level" locations can hold any item.
    """

    display_name = "Randomize level-ups"


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
    # Classes that fight with spells rather than weapons, so Wands is their only skill with locations
    pure_casters = [option_priest, option_mage, option_warlock]
    # Classes that can play either as casters or in melee, and pick which from the Archipelago Stone's preferences
    hybrids = [option_paladin, option_shaman, option_druid]
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

FACTIONS = {"Alliance": CharacterRace.alliance, "Horde": CharacterRace.horde}


def playable_weights(race: CharacterRace, character_class: CharacterClass, faction: list[int] | None = None) -> dict[tuple[int, int], float]:
    """The playable (race, class) pairs the YAML weights allow, optionally on one faction, each weighted by its race's and its class's weight."""
    return {
        (race_id, class_id): race.weights[race_id] * character_class.weights[class_id]
        for race_id, class_id in PLAYABLE_COMBINATIONS
        if race_id in race.weights and class_id in character_class.weights and (faction is None or race_id in faction)
    }


def reroll_into_faction(race: CharacterRace, character_class: CharacterClass, faction: list[int], rng: random.Random) -> None:
    # A pair already on the faction is as fair a draw as a reroll restricted to it would be, so it stays.
    if race.value in faction:
        return
    combinations = playable_weights(race, character_class, faction)
    race.value, character_class.value = rng.choices(list(combinations), list(combinations.values()))[0]


class SameFaction(DefaultOnToggle):
    """
    Put your character on the same faction as the other World of Warcraft players when your race is picked at random.

    No: your race is rolled on its own.
    Yes: you join the faction of the races the other players picked. If some picked an Alliance race and others a Horde race, you join the faction more of them picked, or a random one on a tie.
    When all races are picked at random, everyone is rolled onto one faction together.
    """

    display_name = "Same faction"


class QuestsAllStartingZones(Toggle):
    """
    Include quests from other races' starting zones (levels 1-10).
    """

    display_name = "All starting zones"


class QuestsIncludeDungeons(Toggle):
    """
    Include quests that take place inside dungeons.
    """

    display_name = "Dungeon quests"


class Questsanity(NamedRange):
    """
    Percentage of the available quests turned into locations.
    """

    display_name = "Questsanity"

    range_start = 0
    range_end = 100
    default = 25

    special_range_names = {
        "none": 0,
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


class Explorersanity(NamedRange):
    """
    Percentage of the subzones from the exploration achievements turned into locations.
    """

    display_name = "Explorersanity"

    range_start = 0
    range_end = 100
    default = 0

    special_range_names = {
        "none": 0,
        "minimal": 10,
        "sparse": 25,
        "half": 50,
        "most": 75,
        "all": 100,
    }


class Dungeonsanity(Choice):
    option_none = 0
    option_completion = 1
    option_all = 2

    default = option_none


class ClassicDungeonsanity(Dungeonsanity):
    """
    What becomes a location in the classic dungeons.
    None: nothing.
    Completion: completing each dungeon, through its achievement.
    All: completing each dungeon, and defeating each of its bosses.
    """

    display_name = "Classic dungeonsanity"


class OutlandDungeonsanity(Dungeonsanity):
    """
    What becomes a location in the Burning Crusade dungeons.
    None: nothing.
    Completion: completing each dungeon, through its achievement.
    All: completing each dungeon, and defeating each of its bosses.
    """

    display_name = "Outland dungeonsanity"


class NorthrendDungeonsanity(Dungeonsanity):
    """
    What becomes a location in the Wrath of the Lich King dungeons.
    None: nothing.
    Completion: completing each dungeon, through its achievement.
    All: completing each dungeon, and defeating each of its bosses.
    The Violet Hold's First and Second Prisoner are left out, since the run picks its prisoners at random.
    """

    display_name = "Northrend dungeonsanity"


class StoneShopItemsPerTier(NamedRange):
    """
    How many items the Archipelago Stone's shop sells for each level bracket. Each one is a location bought with gold.
    """

    display_name = "Shop items per tier"

    range_start = 0
    # The vendor window the module shows the shop in holds 150 items, room for 9 in each of the 16 tiers of a level 80 seed.
    range_end = 9
    default = 3

    special_range_names = {
        "none": 0,
        "few": 1,
        "some": 3,
        "many": 6,
        "most": 9,
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


# The trap items, by the key the module knows each one by. items/traps.py makes an item of each.
TRAPS = {
    "dazed": "Dazed Trap",
    "shackle": "Shackle Trap",
    "sheep": "Sheep Trap",
    "poison": "Poison Trap",
    "teleport": "Teleport Trap",
    "ambush": "Ambush Trap",
    "disarm": "Disarming Trap",
    "bombs": "Bombs Trap",
}


class TrapPercentage(NamedRange):
    """
    Percentage of the filler items replaced with traps.

    Dazed Trap: slows you down for 30 seconds.
    Shackle Trap: roots you in place for 15 seconds. You can still attack and cast.
    Sheep Trap: turns you into a sheep for 15 seconds, or until you take damage.
    Poison Trap: deals 40% of your maximum health over 30 seconds.
    Teleport Trap: sends you to a random spot out in the wild of a zone you have unlocked, dungeons aside.
    Ambush Trap: two or three hostile creatures of your level appear around you and attack.
    Disarming Trap: moves your weapons from your hands to your bags, as far as they have room.
    Bombs Trap: bombs rain around you for 10 seconds, each blast taking 60% of your maximum health. Fire on the ground shows where each lands.

    No dispel or immunity removes a trap's effect.
    """

    display_name = "Trap percentage"

    range_start = 0
    range_end = 100
    default = 10

    special_range_names = {
        "none": 0,
        "few": 10,
        "some": 25,
        "half": 50,
        "all": 100,
    }


class TrapWeights(OptionCounter):
    """
    How often each trap is picked, relative to the others. A trap with a weight of 0 is never picked.
    """

    display_name = "Trap weights"
    valid_keys = list(TRAPS.values())
    min = 0
    default = {name: 1 for name in TRAPS.values()}


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
    randomize_level_ups: RandomizeLevelUps
    character_race: CharacterRace
    character_class: CharacterClass
    same_faction: SameFaction
    questsanity: Questsanity
    quests_all_starting_zones: QuestsAllStartingZones
    quests_include_dungeons: QuestsIncludeDungeons
    quests_max_party_size: QuestsMaxPartySize
    classic_dungeonsanity: ClassicDungeonsanity
    outland_dungeonsanity: OutlandDungeonsanity
    northrend_dungeonsanity: NorthrendDungeonsanity
    explorersanity: Explorersanity
    stone_shop_items_per_tier: StoneShopItemsPerTier
    gear_reward_level_window: GearRewardLevelWindow
    spells_randomize_starter_abilities: SpellsRandomizeStarterAbilities
    trap_percentage: TrapPercentage
    trap_weights: TrapWeights
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool

    def __post_init__(self) -> None:
        # Rerolled as the options are assembled rather than in generate_early, so that what reads them first (such as
        # --csv_output) already sees the final pair. Like the YAML draw itself, this uses Archipelago's seeded global random.
        race, character_class = self.character_race, self.character_class
        if (race.value, character_class.value) in PLAYABLE_COMBINATIONS:
            return

        # Weighting each combination by the YAML weights of its race and class is the same as rerolling both until they make one.
        combinations = playable_weights(race, character_class)
        # With nothing to reroll into, the pair is left for generate_early to report under the player's name.
        if combinations:
            race.value, character_class.value = random.choices(list(combinations), list(combinations.values()))[0]


option_groups = [
    OptionGroup("General Options", [Goal, RandomizeLevelUps]),
    OptionGroup("Character Options", [CharacterRace, CharacterClass, SameFaction]),
    OptionGroup("Quest Options", [Questsanity, QuestsAllStartingZones, QuestsMaxPartySize, QuestsIncludeDungeons]),
    OptionGroup("Dungeon Options", [ClassicDungeonsanity, OutlandDungeonsanity, NorthrendDungeonsanity]),
    OptionGroup("Exploration Options", [Explorersanity]),
    OptionGroup("Shop Options", [StoneShopItemsPerTier]),
    OptionGroup("Gear Options", [GearRewardLevelWindow]),
    OptionGroup("Spell Options", [SpellsRandomizeStarterAbilities]),
    OptionGroup("Trap Options", [TrapPercentage, TrapWeights]),
    OptionGroup("Advanced Options", [DeathLink, ProgressionBalancing, Accessibility]),
]

option_presets = {
    "Classic Dungeonmaster": {
        "goal": Goal.option_classic_dungeonmaster,
        "quests_include_dungeons": True,
        "classic_dungeonsanity": ClassicDungeonsanity.option_all,
    },
    "Outland Dungeonmaster": {
        "goal": Goal.option_outland_dungeonmaster,
        "quests_include_dungeons": True,
        "classic_dungeonsanity": ClassicDungeonsanity.option_completion,
        "outland_dungeonsanity": OutlandDungeonsanity.option_all,
    },
    "Northrend Dungeonmaster": {
        "goal": Goal.option_northrend_dungeonmaster,
        "quests_include_dungeons": True,
        "classic_dungeonsanity": ClassicDungeonsanity.option_completion,
        "outland_dungeonsanity": OutlandDungeonsanity.option_completion,
        "northrend_dungeonsanity": NorthrendDungeonsanity.option_all,
    },
}
