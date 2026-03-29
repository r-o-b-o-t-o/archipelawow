from collections.abc import Mapping
from typing import Any

from BaseClasses import Item as BaseItem
from BaseClasses import Location as BaseLocation
from worlds.AutoWorld import World as BaseWorld

from . import constants, options, regions, rules
from .data.items.item_registry import ItemRegistry
from .data.locations.location_registry import LocationRegistry
from .options import CharacterRace, Goal
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
    options: options.Options

    items = ItemRegistry.instance
    item_name_to_id = items.get_name_to_id_dict()
    locations = LocationRegistry.instance
    location_name_to_id = locations.get_name_to_id_dict()
    origin_region_name = regions.LEVELS_01_10

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        self.locations.create_locations(self)
        self.get_data_package_data()

    def set_rules(self) -> None:
        self.locations.set_rules(self)
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
            "options": self.options.as_dict("character_race", "character_class", "death_link"),
            "locations": self.locations.get_slot_data(self),
            "items": self.items.get_slot_data(self),
            "goal": self.options.goal.value,
            "maxlevel": self.level_cap(),
        }

    def level_cap(self) -> int:
        match self.options.goal.value:
            case Goal.option_outland_dungeonmaster | Goal.option_level_70:
                return 70
            case Goal.option_northrend_dungeonmaster | Goal.option_level_80:
                return 80
        return 60

    def is_alliance(self):
        return self.options.character_race.value in CharacterRace.alliance

    def is_horde(self):
        return self.options.character_race.value in CharacterRace.horde

    def has_tbc_content(self):
        return self.level_cap() > 60

    def has_wotlk_content(self):
        return self.level_cap() > 70
