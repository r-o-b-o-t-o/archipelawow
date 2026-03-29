from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from BaseClasses import Location as BaseLocation
from BaseClasses import LocationProgressType

from .location_container import LocationContainer


class Location:
    def __init__(self, name: str, progress_type=LocationProgressType.DEFAULT):
        self.id = LocationRegistry.instance.get_next_id()
        self.name = name
        self.progress_type = progress_type


class LocationRegistry:
    def __init__(self):
        LocationRegistry.instance = self
        self.__next_id = 1
        self.__containers: dict[str, LocationContainer] = {}

    def load_containers(self):
        from .achievements import ACHIEVEMENTS_CONTAINER
        from .flight_paths import FLIGHT_PATHS_CONTAINER
        from .game_objects import GAME_OBJECTS_CONTAINER
        from .levels import LEVELS_CONTAINER
        from .quests import QUESTS_CONTAINER

        self.__containers["achievements"] = ACHIEVEMENTS_CONTAINER
        self.__containers["flightpaths"] = FLIGHT_PATHS_CONTAINER
        self.__containers["gameobjects"] = GAME_OBJECTS_CONTAINER
        self.__containers["levels"] = LEVELS_CONTAINER
        self.__containers["quests"] = QUESTS_CONTAINER

    def get_container(self, container_name: str):
        return self.__containers.get(container_name)

    def get_name_to_id_dict(self):
        d: dict[str, int] = {}
        for container in self.__containers.values():
            d.update(container.get_name_to_id_dict())
        return d

    def get_next_id(self):
        id = self.__next_id
        self.__next_id += 1
        return id

    def create_locations(self, world: "World"):
        data: list[tuple[str, Location]] = []

        for container in self.__containers.values():
            data += container.get_locations(world)

        for region_name, location in data:
            region = world.get_region(region_name)
            if region:
                region.add_locations({location.name: location.id}, BaseLocation)

        for _, loc in data:
            world.get_location(loc.name).progress_type = loc.progress_type

    def get_slot_data(self, world: "World"):
        slot_data = {}
        for name, container in self.__containers.items():
            slot_data[name] = container.get_slot_data(world)

        return slot_data

    def set_rules(self, world: "World"):
        for container in self.__containers.values():
            container.set_rules(world)
