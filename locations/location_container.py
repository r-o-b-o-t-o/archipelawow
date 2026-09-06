from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from ..world import World
    from .location_registry import Location

# What a container holds. A container is written for one kind of location, and saying so is what lets
# it narrow add() and the lookups to that kind without promising the base class something wider.
LocationT = TypeVar("LocationT", bound="Location")


class LocationContainer(Generic[LocationT]):
    def __init__(self) -> None:
        self.__all_locations: dict[int, LocationT] = {}
        self.__name_to_id: dict[str, int] = {}

    def get_name_to_id_dict(self):
        return dict(self.__name_to_id)

    def get_location_by_name(self, name: str):
        id = self.__name_to_id.get(name)
        if id is None:
            return None
        return self.__all_locations.get(id)

    def add(self, location: LocationT, /):
        self.__all_locations[location.id] = location
        self.__name_to_id[location.name] = location.id

    def get_slot_data(self, world: "World") -> Any:
        return None

    def get_locations(self, world: "World") -> list[tuple[str, "Location"]]:
        return []

    def set_rules(self, world: "World"):
        pass
