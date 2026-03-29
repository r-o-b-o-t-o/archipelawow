from .data.items.item_registry import ItemRegistry
from .data.locations.location_registry import LocationRegistry

# Initialize singletons
item_registry = ItemRegistry()
item_registry.load_containers()

location_registry = LocationRegistry()
location_registry.load_containers()

from .world import World as World
