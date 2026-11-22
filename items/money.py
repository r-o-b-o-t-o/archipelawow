from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from .item_container import ItemContainer
from .item_registry import Item


class MoneyContainer(ItemContainer["GoldPouch"]):
    def get_slot_data(self, world: "World"):
        return GOLD_POUCH.id

    def get_items_for_pool(self, world: "World") -> list[Item]:
        if not has_gold_pouches(world):
            return []
        return [GOLD_POUCH]

    def get_filler_weights(self, world: "World") -> dict[str, int]:
        if not has_gold_pouches(world):
            return {}
        return {GOLD_POUCH.name: GOLD_POUCH_FILLER_WEIGHT}


def has_gold_pouches(world: "World") -> bool:
    # A pouch contains the price of a shop item, so free shop items leave it empty as well
    return world.options.gold_pouch_multiplier.value > 0 and world.options.stone_shop_price_multiplier.value > 0


class GoldPouch(Item):
    def __init__(self):
        super().__init__("Gold Pouch", ItemClassification.filler)
        MONEY_CONTAINER.add(self)


MONEY_CONTAINER = MoneyContainer()

# The reference weight the gear fillers in gear.py are set against.
GOLD_POUCH_FILLER_WEIGHT = 8

GOLD_POUCH = GoldPouch()
