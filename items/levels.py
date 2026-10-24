from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from .item_container import ItemContainer
from .item_registry import Item


class LevelsContainer(ItemContainer["Level"]):
    def build_pool(self, world: "World"):
        return [LEVEL_UP for _ in range(world.level_cap() - 1)]

    def get_slot_data(self, world: "World"):
        return LEVEL_UP.id

    def get_items_for_pool(self, world: "World") -> list[Item]:
        if not world.options.randomize_level_ups:
            return []
        return list(self.build_pool(world))

    def place_locked_items(self, world: "World") -> None:
        if world.options.randomize_level_ups:
            return

        from ..locations.levels import LEVELS_CONTAINER as LEVEL_LOCATIONS

        # One Level Up for each level from 2 to the cap. The bracket holding Level N's location asks for a level below N,
        # which the Level Ups of the levels before it give, so none is locked behind itself.
        for data, location in zip(self.build_pool(world), LEVEL_LOCATIONS.build_locations(world), strict=True):
            world.get_location(location.name).place_locked_item(world.create_item(data.name))


class Level(Item):
    def __init__(self):
        super().__init__("Level Up", ItemClassification.progression)
        LEVELS_CONTAINER.add(self)


LEVELS_CONTAINER = LevelsContainer()

LEVEL_UP = Level()
