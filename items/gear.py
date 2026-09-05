from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from .item_container import ItemContainer
from .item_registry import Item


class GearCategory(IntEnum):
    """The bucket a gear item rolls from. Kept in step with GearCategory in the module's AP_Gear.h.

    Shields and off-hand holdables count as weapons, and relics -- librams, idols, totems, sigils --
    as jewellery, which is how a player thinks of them even though the game files call them armor.
    """

    WEAPON = 1
    ARMOR = 2
    JEWELLERY = 3


class GearQuality(IntEnum):
    UNCOMMON = 2
    RARE = 3


class GearContainer(ItemContainer):
    def build_pool(self, world: "World"):
        return list(ALL_GEAR)

    def get_slot_data(self, world: "World"):
        return [[item.id, item.category, item.quality] for item in self.build_pool(world)]

    def get_items_for_pool(self, world: "World") -> list[Item]:
        # Gear never takes a guaranteed slot in the pool. It only shows up as filler, so a seed
        # spends its locations on the things that gate progress and fills the rest with rewards.
        return []

    def get_filler_weights(self, world: "World") -> dict[str, int]:
        return {item.name: item.filler_weight for item in self.build_pool(world)}


class GearItem(Item):
    """A promise of a gear piece rather than a specific one.

    The server picks the actual item when the player receives this, out of what the character's
    class can wear at the level it has reached by then -- neither of which is known at generation.
    """

    def __init__(self, name: str, category: GearCategory, quality: GearQuality, filler_weight: int):
        super().__init__(name, ItemClassification.filler)
        GEAR_CONTAINER.add(self)
        self.category = category
        self.quality = quality
        self.filler_weight = filler_weight


GEAR_CONTAINER = GearContainer()

# Weights are relative to the Gold Pouch's, and together they come to the same total, so gear and
# gold split the filler slots evenly. Rare is rolled less often than uncommon, and armor more often
# than weapons or jewellery, matching how many slots of each a character actually wears.
RANDOM_UNCOMMON_WEAPON = GearItem("Random Uncommon Weapon", GearCategory.WEAPON, GearQuality.UNCOMMON, filler_weight=16)
RANDOM_RARE_WEAPON = GearItem("Random Rare Weapon", GearCategory.WEAPON, GearQuality.RARE, filler_weight=12)
RANDOM_UNCOMMON_ARMOR = GearItem("Random Uncommon Armor", GearCategory.ARMOR, GearQuality.UNCOMMON, filler_weight=20)
RANDOM_RARE_ARMOR = GearItem("Random Rare Armor", GearCategory.ARMOR, GearQuality.RARE, filler_weight=16)
RANDOM_UNCOMMON_JEWELLERY = GearItem("Random Uncommon Jewellery", GearCategory.JEWELLERY, GearQuality.UNCOMMON, filler_weight=12)
RANDOM_RARE_JEWELLERY = GearItem("Random Rare Jewellery", GearCategory.JEWELLERY, GearQuality.RARE, filler_weight=9)

ALL_GEAR = [
    RANDOM_UNCOMMON_WEAPON,
    RANDOM_RARE_WEAPON,
    RANDOM_UNCOMMON_ARMOR,
    RANDOM_RARE_ARMOR,
    RANDOM_UNCOMMON_JEWELLERY,
    RANDOM_RARE_JEWELLERY,
]
