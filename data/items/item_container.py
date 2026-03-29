from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...world import World
    from .item_registry import Item


class ItemContainer:
    def __init__(self) -> None:
        self.__all_items: dict[int, "Item"] = {}
        self.__name_to_id: dict[str, int] = {}

    def get_name_to_id_dict(self):
        return dict(self.__name_to_id)

    def get_item_by_name(self, name: str):
        id = self.__name_to_id.get(name)
        if id is None:
            return None
        return self.__all_items.get(id)

    def add(self, item: "Item"):
        self.__all_items[item.id] = item
        self.__name_to_id[item.name] = item.id

    def get_slot_data(self, world: "World") -> Any:
        return None

    def get_items_for_pool(self, world: "World") -> list["Item"]:
        return []

    def get_precollected_items(self, world: "World") -> list["Item"]:
        return []
