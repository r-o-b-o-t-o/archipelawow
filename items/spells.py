from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from .. import regions
from ..spell_model import SPELL_DISPLAY_NAMES, SPELL_MODELS, SpellKind, SpellModel
from .item_container import ItemContainer
from .item_registry import Item

# The bracket a weapon skill counts as, for the rule that opens the next one.
#
# A weapon master sells almost every weapon skill from level 1, so left alone they would all land in
# the very first bracket and be asked for before level 10, which is no ask at all. Filing them here
# means a character has to have picked its weapons up before it climbs past 20 instead. The one
# weapon skill that does carry a level -- Polearms, at 20 -- is left to fall where its level puts it.
WEAPON_SKILL_LOGIC_REGION = regions.LEVELS_10_15

# How far below a spell's own level this world will hand it over, in levels.
#
# The region rules already say when a spell is needed by; this says how early it may turn up. Spells
# are the one reward whose power is written for a level -- a shaman handed Lava Burst, trained at 75,
# would one-shot everything a level 10 character meets -- so the fill is refused any location whose
# bracket starts more than this far under the level the trainer would ask for. Two brackets of slack
# leaves the fill room while keeping a spell within sight of the level it was written for.
#
# Only this world's locations can be constrained this way. A spell placed in somebody else's game
# answers to their rules, not ours, so it can still turn up early there.
PLACEMENT_LEVEL_WINDOW = 10


class SpellsContainer(ItemContainer):
    def __init__(self) -> None:
        super().__init__()
        self.all_spells: list["SpellItem"] = []

    def add(self, item: "SpellItem"):
        super().add(item)
        self.all_spells.append(item)

    def build_pool(self, world: "World") -> list["SpellItem"]:
        # Riding is not here: its ranks are a ladder, so they are handed out as the progressive item
        # in progressive.py rather than as one item each.
        return [item for item in self.all_spells
                if item.data.kind != SpellKind.RIDING and item.data.is_learnable_by(world)]

    def get_slot_data(self, world: "World"):
        # The taught spells matter for the handful of trainer entries that are a wrapper: the game
        # teaches those by casting the entry rather than learning it, so the server has to know what
        # comes out the other side to keep it out of the character's hands until the item arrives.
        return [[item.id, item.data.id, item.data.req_level, list(item.data.taught_spells)]
                for item in self.build_pool(world)]

    def get_items_for_pool(self, world: "World") -> list[Item]:
        # One copy per spell, matching the one location the seed opens for it
        return list(self.build_pool(world))

    def names_for_region(self, region: str, world: "World") -> list[str]:
        """The spells of this seed whose trainer teaches them inside `region`.

        Feeding these into the rule that opens the next bracket is what keeps a character's kit in
        step with its level: the abilities of a bracket have to be in hand before the seed considers
        the one above it reachable. Unlike a rule on where an item may be placed, this binds the
        whole multiworld -- the fill has to keep the slot beatable wherever it puts the item.
        """
        return [item.name for item in self.build_pool(world) if item.logic_region == region]

    def can_place_at_level(self, item_name: str, region_level: int, world: "World") -> bool:
        """Whether a spell of this seed may be placed in a bracket starting at `region_level`."""
        item = self.get_item_by_name(item_name)
        if not isinstance(item, SpellItem):
            return True

        return item.data.req_level - PLACEMENT_LEVEL_WINDOW <= region_level


class SpellItem(Item):
    """A spell or skill the character learns the moment the multiworld hands it over.

    Only first ranks are shuffled. Once the character has one, its trainer will sell the higher ranks
    as usual, so a single item is enough to open a whole spell up.
    """

    def __init__(self, data: SpellModel):
        # The spell's own name, like every other item. The locations are prefixed so that a tracker
        # groups them together, but an item is read one at a time and the prefix only gets in the way.
        super().__init__(SPELL_DISPLAY_NAMES[(data.class_id, data.id)], ItemClassification.progression)
        SPELLS_CONTAINER.add(self)
        self.data = data
        # The bracket this spell is asked for in, which is the one it is trained in except for the
        # weapon skills -- see WEAPON_SKILL_LOGIC_REGION. It says nothing about where the spell's own
        # check sits: that follows the level its trainer asks for, and is worked out per location.
        self.logic_region = (WEAPON_SKILL_LOGIC_REGION
                             if data.kind == SpellKind.WEAPON and data.req_level <= 1
                             else regions.get_region_by_level(data.req_level))


SPELLS_CONTAINER = SpellsContainer()

for spell in SPELL_MODELS:
    SpellItem(spell)
