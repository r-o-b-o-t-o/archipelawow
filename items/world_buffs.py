from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from ..options import CharacterClass
from .item_container import ItemContainer
from .item_registry import Item

WARRIOR = CharacterClass.option_warrior
PALADIN = CharacterClass.option_paladin
HUNTER = CharacterClass.option_hunter
ROGUE = CharacterClass.option_rogue
SHAMAN = CharacterClass.option_shaman
DRUID = CharacterClass.option_druid

# Spell ids of the buffs a Random World Buff draws from
EVERYONE_BUFFS = [
    22888,  # Rallying Cry of the Dragonslayer
    24425,  # Spirit of Zandalar
    23768,  # Sayge's Dark Fortune of Damage
    23737,  # Sayge's Dark Fortune of Stamina
    22818,  # Mol'dar's Moxie
]
CASTER_BUFFS = [
    23766,  # Sayge's Dark Fortune of Intelligence
    22820,  # Slip'kik's Savvy
]
MELEE_BUFFS = [
    23767,  # Sayge's Dark Fortune of Armor
    22817,  # Fengus' Ferocity
]
# Melee buffs only offered to the classes that make use of their stat
MELEE_CLASS_BUFFS: list[tuple[int, list[int]]] = [
    (23735, [WARRIOR, PALADIN]),  # Sayge's Dark Fortune of Strength
    (23736, [HUNTER, ROGUE, SHAMAN, DRUID]),  # Sayge's Dark Fortune of Agility
]


def melee_buffs(character_class: int) -> list[int]:
    return [*EVERYONE_BUFFS, *MELEE_BUFFS, *[spell for spell, classes in MELEE_CLASS_BUFFS if character_class in classes]]


def caster_buffs() -> list[int]:
    return [*EVERYONE_BUFFS, *CASTER_BUFFS]


class WorldBuffContainer(ItemContainer["WorldBuffItem"]):
    def get_slot_data(self, world: "World"):
        # (melee, caster), like the heirlooms: the module applies the buffs of the role the player picks in the
        # Archipelago Stone's preferences, and classes with a single role name the same buffs twice.
        character_class = world.options.character_class.value
        melee = caster_buffs() if character_class in CharacterClass.pure_casters else melee_buffs(character_class)
        caster = caster_buffs() if character_class in [*CharacterClass.pure_casters, *CharacterClass.hybrids] else melee
        return [RANDOM_WORLD_BUFF.id, melee, caster]

    def get_filler_weights(self, world: "World") -> dict[str, int]:
        return {RANDOM_WORLD_BUFF.name: RANDOM_WORLD_BUFF.filler_weight}


class WorldBuffItem(Item):
    """Applies a world buff picked when the item arrives, out of the ones for the role the player chose."""

    def __init__(self, name: str, filler_weight: int):
        super().__init__(name, ItemClassification.filler)
        WORLD_BUFF_CONTAINER.add(self)
        self.filler_weight = filler_weight


WORLD_BUFF_CONTAINER = WorldBuffContainer()

# Weighted against the Gold Pouch in money.py, like the consumables in wow_items.py
RANDOM_WORLD_BUFF = WorldBuffItem("Random World Buff", filler_weight=6)
