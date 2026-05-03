from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from BaseClasses import Item as BaseItem
from BaseClasses import ItemClassification

from .item_container import ItemContainer


class Item:
    def __init__(self, name: str, classification: ItemClassification, pool_count=1):
        self.id = ItemRegistry.instance.get_next_id()
        self.name = name
        self.classification = classification
        self.pool_count = pool_count


class ItemRegistry:
    def __init__(self):
        ItemRegistry.instance = self
        self.__next_id = 1
        self.__containers: dict[str, ItemContainer] = {}

    def load_containers(self):
        from .levels import LEVELS_CONTAINER
        from .money import MONEY_CONTAINER
        from .wow_items import WOW_ITEMS_CONTAINER
        from .zones import ZONES_CONTAINER

        self.__containers["levels"] = LEVELS_CONTAINER
        self.__containers["items"] = WOW_ITEMS_CONTAINER
        self.__containers["zones"] = ZONES_CONTAINER
        self.__containers["money"] = MONEY_CONTAINER

    def get_container(self, container_name: str):
        return self.__containers.get(container_name)

    def get_name_to_id_dict(self):
        d: dict[str, int] = {}
        for container in self.__containers.values():
            d.update(container.get_name_to_id_dict())
        return d

    def get_item_by_name(self, name: str):
        for container in self.__containers.values():
            item = container.get_item_by_name(name)
            if item:
                return item

    def get_next_id(self):
        id = self.__next_id
        self.__next_id += 1
        return id

    def get_slot_data(self, world: "World"):
        slot_data = {}
        for name, container in self.__containers.items():
            slot_data[name] = container.get_slot_data(world)

        return slot_data

    def get_random_filler_item_name(self, world: "World") -> str:
        # TODO: add fillers and weights for random pick
        return "Gold Pouch"  # TODO: move to item containers

    def get_items_for_pool(self, world: "World"):
        items: list[Item] = []
        for container in self.__containers.values():
            items += container.get_items_for_pool(world)

        return items

    def create_items_pool(self, world: "World"):
        items = self.get_items_for_pool(world)
        pool: list[BaseItem] = []

        for data in items:
            for _ in range(data.pool_count):
                pool.append(world.create_item(data.name))

        return pool

    def get_precollected_items(self, world: "World"):
        precollected: list[Item] = []
        for container in self.__containers.values():
            precollected += container.get_precollected_items(world)

        return precollected

    def create_all_items(self, world: "World"):
        # Create world items
        pool = self.create_items_pool(world)
        pool_ids = [item.code for item in pool]

        # Add precollected items to starting inventory and remove from pool
        for precollected_item in self.get_precollected_items(world):
            idx = pool_ids.index(precollected_item.id)
            item = pool.pop(idx)
            pool_ids.pop(idx)
            world.push_precollected(item)

        # Create filler items
        number_of_items = len(pool)
        number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
        needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
        pool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

        # Submit items to the multiworld pool
        world.multiworld.itempool += pool
