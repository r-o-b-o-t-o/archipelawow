from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from ..options import TRAPS
from .item_container import ItemContainer
from .item_registry import Item


class TrapContainer(ItemContainer["TrapItem"]):
    def get_slot_data(self, world: "World"):
        return {trap.key: trap.id for trap in TRAP_ITEMS}

    def get_random_trap_name(self, world: "World") -> str | None:
        """A trap drawn by the player's weights, or None when every weight is 0. Traps take the place of filler at the
        rate of the trap percentage option, so they offer no filler weight of their own."""
        weights = world.options.trap_weights.value
        traps = [trap.name for trap in TRAP_ITEMS if weights.get(trap.name, 0) > 0]
        if not traps:
            return None
        return world.random.choices(traps, weights=[weights[name] for name in traps], k=1)[0]


class TrapItem(Item):
    """Springs on the character when it arrives, or once it can: the module holds a trap while the character is dead, on
    a flight path, a vehicle or in a battleground, and some traps in more cases, such as the Bombs Trap on a mount."""

    def __init__(self, key: str, name: str):
        super().__init__(name, ItemClassification.trap)
        TRAP_CONTAINER.add(self)
        self.key = key


TRAP_CONTAINER = TrapContainer()

TRAP_ITEMS = [TrapItem(key, name) for key, name in TRAPS.items()]
