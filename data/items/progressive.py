from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from BaseClasses import ItemClassification

from .item_container import ItemContainer
from .item_registry import Item


class ProgressiveType(IntEnum):
    """The track a progressive item upgrades. Kept in step with ProgressiveType in the module's
    AP_Progressive.h."""

    MOVEMENT_SPEED = 1
    EXPERIENCE_RATE = 2
    FOOD = 3
    DRINK = 4


class ProgressiveContainer(ItemContainer):
    def build_pool(self, world: "World"):
        pool = list(ALL_PROGRESSIVE)

        # A warrior or a rogue has no mana bar for a drink to refill, so the whole track would be
        # six dead items in their seed.
        if not world.uses_mana():
            pool.remove(PROGRESSIVE_DRINK)

        return pool

    def get_slot_data(self, world: "World"):
        return [[item.id, item.type, item.steps_for(world)] for item in self.build_pool(world)]

    def get_items_for_pool(self, world: "World") -> list[Item]:
        # One copy per step, so a track that lost its top rungs to the seed's goal puts that many
        # fewer items in the pool.
        items: list[Item] = []
        for item in self.build_pool(world):
            items += [item for _ in item.steps_for(world)]

        return items


class ProgressiveItem(Item):
    """An upgrade the seed hands out several times over, each copy moving its track one step on.

    A copy is never wasted the way a duplicate one-shot reward would be. What a step is worth
    depends on the track: the rate tracks read it as a percentage, the food and drink tracks as the
    WoW item to hand over. The server holds on the last step if a stray extra copy ever shows up.
    """

    def __init__(self, name: str, type: ProgressiveType, steps: list[int], expansion_gated=False):
        super().__init__(name, ItemClassification.useful)
        PROGRESSIVE_CONTAINER.add(self)
        self.type = type
        self.steps = steps
        self.expansion_gated = expansion_gated

    def steps_for(self, world: "World") -> list[int]:
        """The steps this seed actually hands out.

        The food and drink ladders climb out of Azeroth: their fifth rung is a Burning Crusade
        vendor spell and their sixth a Wrath one. A seed whose goal stops short of that content
        stops at the rung before it, rather than promising a character food from a continent the
        seed never opens.
        """
        steps = list(self.steps)
        if self.expansion_gated:
            # Sliced rather than popped: a slice is still well defined on a ladder too short to
            # have the rung being dropped.
            if not world.has_wotlk_content():
                steps = steps[:-1]
            if not world.has_tbc_content():
                steps = steps[:-1]

        return steps


PROGRESSIVE_CONTAINER = ProgressiveContainer()

# Movement speed multiplies whatever the character is already moving at, mount speed included, so
# the last step makes a ground mount half again as fast. Experience rate multiplies the hidden
# Archipelago experience that levels the slot up -- the character's own experience bar never moves
# -- so the last step halves the grind between level checks.
PROGRESSIVE_MOVEMENT_SPEED = ProgressiveItem("Progressive Movement Speed", ProgressiveType.MOVEMENT_SPEED, [10, 20, 30, 40, 50])
PROGRESSIVE_EXPERIENCE_RATE = ProgressiveItem("Progressive Experience Rate", ProgressiveType.EXPERIENCE_RATE, [20, 40, 60, 80, 100])

# Eternal food and drink: each step is a WoW item with unlimited uses that restores more than the
# one before it, and the server swaps the old one out as the new one lands. The item templates are
# defined by the module's archipelawow_world_005 database update, which also documents which vendor
# spell each tier carries. The last two rungs of each ladder are the Burning Crusade and Wrath
# spells, and drop out of seeds that never reach that content -- see steps_for().
PROGRESSIVE_FOOD = ProgressiveItem(
    "Progressive Food",
    ProgressiveType.FOOD,
    [
        19063,  # The Immortal Crust
        40843,  # Suspiciously Regrowing Berries
        34770,  # Fillet of Neverfin
        35710,  # Helboar Shank of Infinite Regret
        43496,  # Cinderfowl Drumstick
        36831,  # Ribs of the Endless Banquet
    ],
    expansion_gated=True,
)
PROGRESSIVE_DRINK = ProgressiveItem(
    "Progressive Drink",
    ProgressiveType.DRINK,
    [
        33062,  # Never-Empty Mug of Tavern Runoff
        37103,  # Basin of Lesser Miracles
        23704,  # Bottomless Bottle of Dubious Vintage
        32913,  # Perpetually Overflowing Tankard
        41374,  # Netherbloom Nectar
        42548,  # Elixir of the Everlasting Toast
    ],
    expansion_gated=True,
)

ALL_PROGRESSIVE = [
    PROGRESSIVE_MOVEMENT_SPEED,
    PROGRESSIVE_EXPERIENCE_RATE,
    PROGRESSIVE_FOOD,
    PROGRESSIVE_DRINK,
]
