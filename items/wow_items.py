from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from ..glyph_model import GLYPH_MODELS, GlyphModel
from .item_container import ItemContainer
from .item_registry import Item


class WoWItemsContainer(ItemContainer["WoWItem"]):
    def build_pool(self, world: "World"):
        items: list[WoWItem] = [*BAGS, *heirlooms_for(world)]
        items += [
            glyph
            for glyph in GLYPHS
            if glyph.model.class_id == world.options.character_class.value and glyph.model.required_level <= world.level_cap()
        ]
        return items

    def get_slot_data(self, world: "World"):
        return [[item.id, item.wow_item_id] for item in self.build_pool(world)]

    def get_items_for_pool(self, world: "World") -> list[Item]:
        return list(self.build_pool(world))


class WoWItem(Item):
    def __init__(self, name: str, wow_item_id: int, classification: ItemClassification, pool_count=1):
        super().__init__(name, classification, pool_count)
        WOW_ITEMS_CONTAINER.add(self)
        self.wow_item_id = wow_item_id


class Glyph(WoWItem):
    def __init__(self, model: GlyphModel):
        super().__init__(model.name, model.id, ItemClassification.filler if model.minor else ItemClassification.useful)
        self.model = model


WOW_ITEMS_CONTAINER = WoWItemsContainer()

GLYPHS = [Glyph(model) for model in GLYPH_MODELS]

from .heirlooms import heirlooms_for

BROWN_LEATHER_SATCHEL = WoWItem("Brown Leather Satchel", 4498, ItemClassification.filler, pool_count=2)
HUGE_BROWN_SACK = WoWItem("Huge Brown Sack", 4499, ItemClassification.filler, pool_count=2)
TRAVELERS_BACKPACK = WoWItem("Traveler's Backpack", 4500, ItemClassification.filler, pool_count=2)
FROSTWEAVE_BAG = WoWItem("Frostweave Bag", 41599, ItemClassification.filler, pool_count=2)
BAGS = [BROWN_LEATHER_SATCHEL, HUGE_BROWN_SACK, TRAVELERS_BACKPACK, FROSTWEAVE_BAG]
