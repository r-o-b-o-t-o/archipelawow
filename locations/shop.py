from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from .. import regions
from ..options import StoneShopItemsPerTier
from .location_container import LocationContainer
from .location_registry import Location

MAX_ITEMS_PER_TIER = StoneShopItemsPerTier.range_end


class ShopItem(Location):
    def __init__(self, level: int, slot: int, region: str):
        super().__init__(f"Stone Shop: Level {level:02d} Item {slot}")
        SHOP_CONTAINER.add(self)
        self.level = level
        self.slot = slot
        self.region = region


class ShopContainer(LocationContainer[ShopItem]):
    """Checks bought with gold from the Archipelago Stone, a tier of them per level bracket. Gold is not tracked by the logic."""

    def __init__(self) -> None:
        super().__init__()
        self.all_items: list[ShopItem] = []

    def add(self, location: ShopItem):
        super().add(location)
        self.all_items.append(location)

    def build_locations(self, world: "World"):
        count = world.options.stone_shop_items_per_tier.value
        return [loc for loc in self.all_items if loc.slot <= count and loc.level <= world.max_location_level()]

    def get_slot_data(self, world: "World"):
        return [[loc.level, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        return [(loc.region, loc) for loc in self.build_locations(world)]


SHOP_CONTAINER = ShopContainer()

# A tier opens as its bracket does, so its items sit in that bracket's region without a rule of their own.
SHOP_ITEMS = [
    ShopItem(max(1, regions.REGION_LEVELS[region]), slot, region) for region in regions.ALL_REGIONS for slot in range(1, MAX_ITEMS_PER_TIER + 1)
]
