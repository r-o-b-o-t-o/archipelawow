from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from BaseClasses import ItemClassification

from ...options import CharacterClass
from .item_container import ItemContainer
from .item_registry import Item


class WoWItemsContainer(ItemContainer):
    def build_pool(self, world: "World"):
        items = [*BAGS, GOLD_POUCH]

        match world.options.character_class:
            case CharacterClass.option_warrior:
                items += GLYPHS_WARRIOR
            case CharacterClass.option_paladin:
                items += GLYPHS_PALADIN
            case CharacterClass.option_hunter:
                items += GLYPHS_HUNTER
            case CharacterClass.option_shaman:
                items += GLYPHS_SHAMAN
            case CharacterClass.option_rogue:
                items += GLYPHS_ROGUE
            case CharacterClass.option_druid:
                items += GLYPHS_DRUID
            case CharacterClass.option_mage:
                items += GLYPHS_MAGE
            case CharacterClass.option_warlock:
                items += GLYPHS_WARLOCK
            case CharacterClass.option_priest:
                items += GLYPHS_PRIEST

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


WOW_ITEMS_CONTAINER = WoWItemsContainer()

from .glyphs.druid import GLYPHS_DRUID
from .glyphs.hunter import GLYPHS_HUNTER
from .glyphs.mage import GLYPHS_MAGE
from .glyphs.paladin import GLYPHS_PALADIN
from .glyphs.priest import GLYPHS_PRIEST
from .glyphs.rogue import GLYPHS_ROGUE
from .glyphs.shaman import GLYPHS_SHAMAN
from .glyphs.warlock import GLYPHS_WARLOCK
from .glyphs.warrior import GLYPHS_WARRIOR

BROWN_LEATHER_SATCHEL = WoWItem("Brown Leather Satchel", 4498, ItemClassification.filler, pool_count=2)
HUGE_BROWN_SACK = WoWItem("Huge Brown Sack", 4499, ItemClassification.filler, pool_count=2)
TRAVELERS_BACKPACK = WoWItem("Traveler's Backpack", 4500, ItemClassification.filler, pool_count=2)
FROSTWEAVE_BAG = WoWItem("Frostweave Bag", 41599, ItemClassification.filler, pool_count=2)
BAGS = [BROWN_LEATHER_SATCHEL, HUGE_BROWN_SACK, TRAVELERS_BACKPACK, FROSTWEAVE_BAG]

GOLD_POUCH = WoWItem("Gold Pouch", 38539, ItemClassification.filler, pool_count=1)  # TODO: create actual item
