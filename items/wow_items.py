from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from ..glyph_model import GLYPH_MODELS, GlyphModel
from .item_container import ItemContainer
from .item_registry import Item


class WoWItemsContainer(ItemContainer["WoWItem"]):
    def build_pool(self, world: "World"):
        items: list[WoWItem] = [*BAGS, DREAD_PIRATE_RING]
        items += [
            glyph
            for glyph in GLYPHS
            if glyph.model.class_id == world.options.character_class.value and glyph.model.required_level <= world.max_location_level()
        ]
        return items

    def get_slot_data(self, world: "World"):
        return [[item.id, item.wow_item_id] for item in [*self.build_pool(world), *CONSUMABLES]]

    def get_items_for_pool(self, world: "World") -> list[Item]:
        return list(self.build_pool(world))

    def get_filler_weights(self, world: "World") -> dict[str, int]:
        # An option of 0 takes its consumable out of the pool
        enabled = {
            SCROLL_OF_DIVINATION.name: world.options.scroll_of_divination_hints.value > 0,
            TOME_OF_INSIGHT.name: world.options.tome_of_insight_experience.value > 0,
            ENDURING_SOULSTONE.name: world.options.enduring_soulstone_duration.value > 0,
        }
        return {item.name: item.filler_weight for item in CONSUMABLES if enabled[item.name]}


class WoWItem(Item):
    def __init__(self, name: str, wow_item_id: int, classification: ItemClassification, pool_count=1):
        super().__init__(name, classification, pool_count)
        WOW_ITEMS_CONTAINER.add(self)
        self.wow_item_id = wow_item_id


class Consumable(WoWItem):
    """A filler item whose effect the module applies when it is used up. Its item template is defined by
    the module's database updates."""

    def __init__(self, name: str, wow_item_id: int, filler_weight: int):
        super().__init__(name, wow_item_id, ItemClassification.filler)
        self.filler_weight = filler_weight


class Glyph(WoWItem):
    def __init__(self, model: GlyphModel):
        super().__init__(model.name, model.id, ItemClassification.filler if model.minor else ItemClassification.useful)
        self.model = model


WOW_ITEMS_CONTAINER = WoWItemsContainer()

GLYPHS = [Glyph(model) for model in GLYPH_MODELS]

BROWN_LEATHER_SATCHEL = WoWItem("Brown Leather Satchel", 4498, ItemClassification.filler, pool_count=2)
HUGE_BROWN_SACK = WoWItem("Huge Brown Sack", 4499, ItemClassification.filler, pool_count=2)
TRAVELERS_BACKPACK = WoWItem("Traveler's Backpack", 4500, ItemClassification.filler, pool_count=2)
FROSTWEAVE_BAG = WoWItem("Frostweave Bag", 41599, ItemClassification.filler, pool_count=2)
BAGS = [BROWN_LEATHER_SATCHEL, HUGE_BROWN_SACK, TRAVELERS_BACKPACK, FROSTWEAVE_BAG]

# The one heirloom every class wants as it is, so unlike the others (see heirlooms.py) it is sent as itself.
DREAD_PIRATE_RING = WoWItem("Dread Pirate Ring", 50255, ItemClassification.useful)

# Weighted against the Gold Pouch in money.py. How many locations the scroll hints, how much of the experience
# to the next Archipelago level the tome gives and how long the soulstone stores a soul are player options,
# which the module reads from the slot data.
SCROLL_OF_DIVINATION = Consumable("Scroll of Divination", 4427, filler_weight=10)
TOME_OF_INSIGHT = Consumable("Tome of Insight", 1335, filler_weight=10)
ENDURING_SOULSTONE = Consumable("Enduring Soulstone", 2767, filler_weight=10)
CONSUMABLES = [SCROLL_OF_DIVINATION, TOME_OF_INSIGHT, ENDURING_SOULSTONE]
