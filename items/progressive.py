from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from ..spell_model import SPELL_MODELS, SpellExpansion, SpellKind, SpellModel
from .item_container import ItemContainer
from .item_registry import Item


class ProgressiveType(IntEnum):
    """The track a progressive item upgrades. Kept in step with ProgressiveType in the module's
    AP_Progressive.h."""

    MOVEMENT_SPEED = 1
    EXPERIENCE_RATE = 2
    FOOD = 3
    DRINK = 4
    RIDING = 5


class ProgressiveContainer(ItemContainer["ProgressiveItem"]):
    def build_pool(self, world: "World"):
        pool = list(ALL_PROGRESSIVE)

        # A warrior or a rogue has no mana bar for a drink to refill, so the whole track would be
        # six dead items in their seed.
        if not world.uses_mana():
            pool.remove(PROGRESSIVE_DRINK)

        return pool

    def get_slot_data(self, world: "World"):
        return [[item.id, item.type, item.steps_for(world), item.levels_for(world)] for item in self.build_pool(world)]

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

    def __init__(
        self, name: str, type: ProgressiveType, steps: list[int], req_levels: list[int] | None = None, classification=ItemClassification.useful
    ):
        super().__init__(name, classification)
        PROGRESSIVE_CONTAINER.add(self)
        self.type = type
        self.steps = steps
        self.req_levels = req_levels

    def steps_for(self, world: "World") -> list[int]:
        """The steps this seed actually hands out.

        A track with required levels only keeps the steps whose level is below the seed's level cap.
        """
        steps = list(self.steps)
        if self.req_levels is not None:
            steps = [step for step, level in zip(steps, self.req_levels, strict=True) if level < world.level_cap()]

        # Copies trimmed from an overflowing pool take the top steps with them
        return steps[: len(steps) - world.trimmed_items[self.name]]

    def levels_for(self, world: "World") -> list[int]:
        """The character level each step is worth reaching, where a track has one. Empty otherwise."""
        return []


def _riding_ladder() -> list:
    """Every riding rank the game has, slowest first, whatever a given seed can reach."""
    return sorted((spell for spell in SPELL_MODELS if spell.kind == SpellKind.RIDING), key=lambda spell: spell.req_level)


# Artisan Riding, the fastest rank there is. It is the one rung the region rules never ask for: it
# only makes a mount the character already flies go faster, so it is a bonus to come across rather
# than something to gate the run behind. Read off the ladder rather than named by id, so that a
# change to the extract carries through on its own.
UNGATED_RIDING_RANK_ID = _riding_ladder()[-1].id


class ProgressiveRidingItem(ProgressiveItem):
    """The riding ladder, handed out one rank at a time.

    Apprentice, Journeyman, Expert and then Artisan, in that order, so a copy is never the rank above
    one the character has not got yet. Which rungs a seed carries is the spell extract's answer rather
    than a list here. The ground ranks are in every seed whatever its level cap, as a quality of life
    item: the module teaches a mount with each rank, since the mount items ask for a level. The flying
    ranks are only sold in Outland, so a seed that stops short of it drops them. Cold Weather Flying is
    no part of this -- it is a permit to fly over Northrend rather than a faster mount, and an Expert
    rider can buy it without ever reaching Artisan.
    """

    def __init__(self):
        super().__init__("Progressive Riding Skill", ProgressiveType.RIDING, [], classification=ItemClassification.progression)

    def ranks_for(self, world: "World"):
        return sorted(
            (spell for spell in SPELL_MODELS if spell.kind == SpellKind.RIDING and self.is_rank_in_seed(spell, world)),
            key=lambda spell: spell.req_level,
        )

    @staticmethod
    def is_rank_in_seed(spell: SpellModel, world: "World") -> bool:
        return spell.expansion == SpellExpansion.CLASSIC or spell.is_learnable_by(world)

    def steps_for(self, world: "World") -> list[int]:
        return [spell.id for spell in self.ranks_for(world)]

    def levels_for(self, world: "World") -> list[int]:
        return [spell.req_level for spell in self.ranks_for(world)]

    def required_count_for_region(self, region: str, world: "World") -> int:
        """How many copies a character is expected to hold to be let into `region`.

        A rank is asked for at the level its own trainer sells it, so the ladder keeps pace with the
        character instead of arriving all at once. Every rank counts except Artisan Riding -- see
        UNGATED_RIDING_RANK_ID -- whatever the seed's level cap leaves at the top of its ladder.
        """
        from .. import regions

        level = regions.REGION_LEVELS.get(region)
        if level is None:
            return 0

        return sum(1 for rank in self.ranks_for(world) if rank.id != UNGATED_RIDING_RANK_ID and rank.req_level <= level)


PROGRESSIVE_CONTAINER = ProgressiveContainer()

# Movement speed multiplies whatever the character is already moving at, mount speed included, so
# the last step makes a ground mount 60% faster. Experience rate multiplies the hidden Archipelago
# experience that levels the slot up -- the character's own experience bar never moves -- so the
# last step cuts the grind between level checks by more than half.
PROGRESSIVE_MOVEMENT_SPEED = ProgressiveItem("Progressive Movement Speed", ProgressiveType.MOVEMENT_SPEED, [20, 40, 60])
PROGRESSIVE_EXPERIENCE_RATE = ProgressiveItem("Progressive Experience Rate", ProgressiveType.EXPERIENCE_RATE, [40, 80, 120])

# Eternal food and drink: each step is a WoW item with unlimited uses that restores more than the
# one before it, and the server swaps the old one out as the new one lands. The item templates are
# defined by the module's archipelawow_world_005 database update, which also documents which vendor
# spell each tier carries. A tier only goes to seeds whose level cap is above the required level of
# the vendor item its spell comes from -- see steps_for().
FOOD_AND_DRINK_REQ_LEVELS = [15, 35, 45, 55, 65, 75]

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
    req_levels=FOOD_AND_DRINK_REQ_LEVELS,
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
    req_levels=FOOD_AND_DRINK_REQ_LEVELS,
)

PROGRESSIVE_RIDING = ProgressiveRidingItem()

ALL_PROGRESSIVE = [
    PROGRESSIVE_MOVEMENT_SPEED,
    PROGRESSIVE_EXPERIENCE_RATE,
    PROGRESSIVE_FOOD,
    PROGRESSIVE_DRINK,
    PROGRESSIVE_RIDING,
]
