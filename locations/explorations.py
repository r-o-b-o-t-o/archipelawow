import math
from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from ..world import World

from ..conditions import has_zone
from ..exploration_model import EXPLORATION_MODELS
from ..items.zones import ZONES_CONTAINER, Zone
from .location_container import LocationContainer
from .location_registry import Location


class Exploration(Location):
    def __init__(self, name: str, criteria_id: int, zone: Zone):
        super().__init__(f"Exploration: {name}" if name == zone.name else f"Exploration: {name} ({zone.name})")
        EXPLORATIONS_CONTAINER.add(self)
        self.criteria_id = criteria_id
        self.zone = zone


class ExplorationsContainer(LocationContainer[Exploration]):
    def __init__(self) -> None:
        super().__init__()
        self.explorations: list[Exploration] = []
        # The container is a singleton shared by every player, and the roll must not be re-rolled per caller
        self.__locations_cache: "WeakKeyDictionary[World, list[Exploration]]" = WeakKeyDictionary()

    def add(self, exploration: Exploration):
        super().add(exploration)
        self.explorations.append(exploration)

    def build_locations(self, world: "World") -> list[Exploration]:
        """The subzones that become locations for this world, rolled once so that every caller sees the same set."""
        locations = self.__locations_cache.get(world)
        if locations is None:
            locations = self.pick_locations(world)
            self.__locations_cache[world] = locations

        return locations

    def pick_locations(self, world: "World") -> list[Exploration]:
        # A zone can be in the pool with no bracket for the faction, such as Westfall for the Horde
        zones_in_pool = set(ZONES_CONTAINER.build_pool(world))
        available = [e for e in self.explorations if e.zone in zones_in_pool and e.zone.region(world)]
        count = math.ceil(len(available) * world.options.explorersanity.value / 100)
        return sorted(world.random.sample(available, count), key=lambda e: e.id)

    def get_slot_data(self, world: "World"):
        return [[loc.criteria_id, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        return [(loc.zone.region(world), loc) for loc in self.build_locations(world)]

    def set_rules(self, world: "World"):
        for loc in self.build_locations(world):
            world.set_rule(world.get_location(loc.name), has_zone(loc.zone, world))


EXPLORATIONS_CONTAINER = ExplorationsContainer()

for model in EXPLORATION_MODELS:
    # A zone with no item, such as Moonglade or Deadwind Pass, is open to anyone and has no bracket to file it under
    zone = ZONES_CONTAINER.zones.get(model.zone_id)
    if zone is not None:
        Exploration(model.name, model.id, zone)
