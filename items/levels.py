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
        return list(self.build_pool(world))


class Level(Item):
    def __init__(self):
        super().__init__("Level Up", ItemClassification.progression)
        LEVELS_CONTAINER.add(self)


LEVELS_CONTAINER = LevelsContainer()

LEVEL_UP = Level()
