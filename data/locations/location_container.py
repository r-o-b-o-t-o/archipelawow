from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...world import World
    from .location_registry import Location


class LocationContainer:
    def __init__(self) -> None:
        self.__all_locations: dict[int, "Location"] = {}
        self.__name_to_id: dict[str, int] = {}

    def get_name_to_id_dict(self):
        return dict(self.__name_to_id)

    def get_location_by_name(self, name: str):
        id = self.__name_to_id.get(name)
        if id is None:
            return None
        return self.__all_locations.get(id)

    def add(self, location: "Location"):
        self.__all_locations[location.id] = location
        self.__name_to_id[location.name] = location.id

    def get_slot_data(self, world: "World") -> Any:
        return None

    def get_locations(self, world: "World") -> list[tuple[str, "Location"]]:
        return []

    def set_rules(self, world: "World"):
        pass
