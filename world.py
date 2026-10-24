import logging
import math
from collections import Counter
from collections.abc import Mapping
from typing import Any

from BaseClasses import Item as BaseItem
from BaseClasses import Location as BaseLocation
from BaseClasses import MultiWorld
from Options import OptionError
from worlds.AutoWorld import World as BaseWorld

from . import constants, options, regions, rules
from .items.item_registry import ItemRegistry
from .locations.location_registry import LocationRegistry
from .logic_export import export_logic
from .options import FACTIONS, PLAYABLE_COMBINATIONS, CharacterClass, CharacterRace, Goal, playable_weights, reroll_into_faction
from .web_world import WebWorld


class Item(BaseItem):
    game = constants.GAME_NAME


class Location(BaseLocation):
    game = constants.GAME_NAME


class World(BaseWorld):
    """
    World of Warcraft is a 2004 massively multiplayer online role-playing game set in the Warcraft fantasy universe.
    """

    game = constants.GAME_NAME
    web = WebWorld()
    options_dataclass = options.Options
    options: options.Options  # pyright: ignore[reportIncompatibleVariableOverride]

    items = ItemRegistry.instance
    item_name_to_id = items.get_name_to_id_dict()
    locations = LocationRegistry.instance
    location_name_to_id = locations.get_name_to_id_dict()
    origin_region_name = regions.LEVELS_01_05

    # Copies of each item dropped from an overflowing pool, by name -- see ItemRegistry.trim_pool
    trimmed_items: Counter[str]

    def generate_early(self) -> None:
        self.trimmed_items = Counter()

        # Options.__post_init__ has already rerolled any pair the YAML weights allow a playable one for.
        race, character_class = self.options.character_race, self.options.character_class
        if (race.value, character_class.value) not in PLAYABLE_COMBINATIONS:
            races = " or ".join(CharacterRace.get_option_name(value) for value in race.weights)
            classes = " or ".join(CharacterClass.get_option_name(value) for value in character_class.weights)
            raise OptionError(f"{self.player_name}: {classes} is not available for {races}.")

    @classmethod
    def stage_generate_early(cls, multiworld: MultiWorld) -> None:
        # Every player's race is rolled on its own as their options are assembled, so the factions can only be lined up once all
        # are in. That is after --csv_output has been written, which may list a race this then rerolled.
        worlds = [world for world in multiworld.get_game_worlds(cls.game) if isinstance(world, World)]
        faction_weights = {
            world: {
                name: sum(playable_weights(world.options.character_race, world.options.character_class, races).values())
                for name, races in FACTIONS.items()
            }
            for world in worlds
        }
        # A player whose YAML can only land on one faction has picked it, whatever their own option says
        picked = {
            world: next(name for name, weight in weights.items() if weight) for world, weights in faction_weights.items() if not all(weights.values())
        }
        followers = [world for world in worlds if world not in picked and world.options.same_faction]
        if not followers:
            return

        faction = None
        picks = Counter(picked.values()).most_common()
        if len(picks) == 1 or (len(picks) == 2 and picks[0][1] > picks[1][1]):
            faction = picks[0][0]
        if len(picks) == 2:
            names = ", ".join(f"{world.player_name} ({name})" for world, name in picked.items())
            outcome = f"join the {faction}" if faction else "are rolled onto one faction together, since neither has more picks"
            logging.warning(f"{cls.game}: the races picked are on both factions, {names}; the races picked at random {outcome}.")

        if faction is None:
            rolled = {next(name for name, races in FACTIONS.items() if world.options.character_race.value in races) for world in followers}
            if len(rolled) == 1:
                # Rolls that already agree are as fair a draw as rerolling them until they do
                faction = rolled.pop()
            else:
                # The chance of each faction being the one every follower lands on, rolling on their own
                chances = [math.prod(faction_weights[world][name] / sum(faction_weights[world].values()) for world in followers) for name in FACTIONS]
                faction = multiworld.random.choices(list(FACTIONS), chances)[0]

        for world in followers:
            reroll_into_faction(world.options.character_race, world.options.character_class, FACTIONS[faction], multiworld.random)

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        self.locations.create_locations(self)

    def set_rules(self) -> None:
        self.locations.set_rules(self)
        rules.set_spell_placement_rules(self)
        rules.set_completion_conditions(self)

    def create_items(self) -> None:
        self.items.create_all_items(self)

    def create_item(self, name: str):
        data = self.items.get_item_by_name(name)
        if data is None:
            raise Exception(f'Could not find "{name}" in item container')
        return Item(name, data.classification, data.id, self.player)

    def get_filler_item_name(self) -> str:
        return self.items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "options": self.options.as_dict(
                "character_race",
                "character_class",
                "death_link",
                "gear_reward_level_window",
                "spells_randomize_starter_abilities",
            ),
            "locations": self.locations.get_slot_data(self),
            "items": self.items.get_slot_data(self),
            "goal": self.options.goal.value,
            "maxlevel": self.level_cap(),
            "logic": export_logic(self),
        }

    def level_cap(self) -> int:
        return Goal.level_caps[self.options.goal.value]

    def max_location_level(self) -> int:
        """The highest level a check or reward may ask for: a level goal is won the moment the character reaches the cap."""
        return self.level_cap() - 1 if self.options.goal.value in Goal.level_goals else self.level_cap()

    def is_alliance(self):
        return self.options.character_race.value in CharacterRace.alliance

    def is_horde(self):
        return self.options.character_race.value in CharacterRace.horde

    def uses_mana(self):
        return self.options.character_class.value not in CharacterClass.no_mana

    def has_tbc_content(self):
        return self.level_cap() > 60

    def has_wotlk_content(self):
        return self.level_cap() > 70
