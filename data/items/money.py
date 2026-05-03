from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from BaseClasses import ItemClassification

from .item_container import ItemContainer
from .item_registry import Item


class MoneyContainer(ItemContainer):
    def get_slot_data(self, world: "World"):
        return GOLD_POUCH.id

    def get_items_for_pool(self, world: "World") -> list[Item]:
        return [GOLD_POUCH]


class GoldPouch(Item):
    def __init__(self):
        super().__init__("Gold Pouch", ItemClassification.filler)
        MONEY_CONTAINER.add(self)


MONEY_CONTAINER = MoneyContainer()

GOLD_POUCH = GoldPouch()
