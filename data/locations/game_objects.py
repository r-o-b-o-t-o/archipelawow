from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from BaseClasses import LocationProgressType

from ... import regions
from .location_container import LocationContainer
from .location_registry import Location


class GameObject(Location):
    def __init__(self, name: str, entry_ids: list[int], region: str, progress_type=LocationProgressType.DEFAULT):
        super().__init__(f"Object: {name}", progress_type)
        GAME_OBJECTS_CONTAINER.add(self)
        self.entry_ids = entry_ids
        self.region = region


class GameObjectsContainer(LocationContainer):
    def build_locations(self, world: "World"):
        return [*CHESTS]

    def get_slot_data(self, world: "World"):
        return []  # TODO

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        locations = self.build_locations(world)
        return [(l.region, l) for l in locations]


GAME_OBJECTS_CONTAINER = GameObjectsContainer()

BATTERED_CHEST = GameObject("Battered Chest", [2843, 2849, 106318, 106319], regions.LEVELS_01_10, LocationProgressType.EXCLUDED)
LARGE_SOLID_CHEST = GameObject("Large Solid Chest", [74448, 75298, 75299, 75300, 153462, 153463], regions.LEVELS_01_10, LocationProgressType.EXCLUDED)
LARGE_IRON_BOUND_CHEST = GameObject("Large Iron Bound Chest", [74447, 75295, 75296, 75297], regions.LEVELS_01_10, LocationProgressType.EXCLUDED)
LARGE_MITHRIL_BOUND_CHEST = GameObject("Large Mithril Bound Chest", [131978, 153468, 153469], regions.LEVELS_01_10, LocationProgressType.EXCLUDED)

CHESTS = [BATTERED_CHEST, LARGE_SOLID_CHEST, LARGE_IRON_BOUND_CHEST, LARGE_MITHRIL_BOUND_CHEST]
