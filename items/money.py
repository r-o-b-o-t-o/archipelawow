from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from .item_container import ItemContainer
from .item_registry import Item


class MoneyContainer(ItemContainer):
    def get_slot_data(self, world: "World"):
        return GOLD_POUCH.id

    def get_items_for_pool(self, world: "World") -> list[Item]:
        return [GOLD_POUCH]

    def get_filler_weights(self, world: "World") -> dict[str, int]:
        return {GOLD_POUCH.name: GOLD_POUCH_FILLER_WEIGHT}


class GoldPouch(Item):
    def __init__(self):
        super().__init__("Gold Pouch", ItemClassification.filler)
        MONEY_CONTAINER.add(self)


MONEY_CONTAINER = MoneyContainer()

# The reference weight the gear fillers in gear.py are set against.
GOLD_POUCH_FILLER_WEIGHT = 15

GOLD_POUCH = GoldPouch()
