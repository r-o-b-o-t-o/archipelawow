from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from BaseClasses import ItemClassification

from .item_container import ItemContainer
from .item_registry import Item


class LevelsContainer(ItemContainer):
    def build_pool(self, world: "World"):
        levels = 59

        if world.has_tbc_content():
            levels += 10

        if world.has_wotlk_content():
            levels += 10

        return [LEVEL_UP for _ in range(levels)]

    def get_slot_data(self, world: "World"):
        return LEVEL_UP.id

    def get_items_for_pool(self, world: "World") -> list[Item]:
        return list(self.build_pool(world))


class Level(Item):
    def __init__(self):
        super().__init__("Level Up", ItemClassification.progression)
        LEVELS_CONTAINER.add(self)


LEVELS_CONTAINER = LevelsContainer()

LEVEL_UP = Level()
