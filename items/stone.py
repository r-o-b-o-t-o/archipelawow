from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from .item_container import ItemContainer
from .item_registry import Item


class StoneContainer(ItemContainer["StoneUnlock"]):
    """The Archipelago Stone's menus that an item unlocks."""

    def get_slot_data(self, world: "World"):
        return {"teleport_to_friend": TELEPORT_TO_FRIEND.id}

    def get_items_for_pool(self, world: "World") -> list[Item]:
        # Only worth a location with another World of Warcraft slot to teleport to.
        if len(world.multiworld.get_game_players(world.game)) > 1:
            return [TELEPORT_TO_FRIEND]

        return []


class StoneUnlock(Item):
    def __init__(self, name: str):
        super().__init__(name, ItemClassification.useful)
        STONE_CONTAINER.add(self)


STONE_CONTAINER = StoneContainer()

# Teleports to another character online and connected to a slot, on a 30 minute cooldown.
TELEPORT_TO_FRIEND = StoneUnlock("Teleport to Friend")
