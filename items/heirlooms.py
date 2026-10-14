from typing import TYPE_CHECKING, NamedTuple

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
PRIEST = CharacterClass.option_priest
SHAMAN = CharacterClass.option_shaman
MAGE = CharacterClass.option_mage
WARLOCK = CharacterClass.option_warlock
DRUID = CharacterClass.option_druid

# The most Heirloom Weapons a slot receives. Classes with fewer weapons to choose from get one per weapon.
MAX_WEAPON_SLOTS = 3


class Pieces(NamedTuple):
    """The heirloom a class gets for one kind of piece, by the role the character plays: the module sends the
    one matching the player's preference when the item arrives. A class with a single role names the same piece
    twice."""

    melee: int
    caster: int


class ArmorSet(NamedTuple):
    shoulders: int
    chest: int


# The core lets warriors and paladins wear plate heirlooms, and hunters and shamans mail ones, before they learn
# that armor (see Player::CanUseItem in AzerothCore), so a warrior wears the plate set from level one and a hunter
# the mail one. Each class therefore wants the heaviest set it ends up in for the role it plays, and never a
# lighter one.
PLATE = ArmorSet(shoulders=42949, chest=48685)  # Polished Spaulders / Breastplate of Valor
MELEE_MAIL = ArmorSet(shoulders=42950, chest=48677)  # Champion Herod's Shoulder / Champion's Deathdealer Breastplate
CASTER_MAIL = ArmorSet(shoulders=42951, chest=48683)  # Mystical Pauldrons / Vest of Elements
MELEE_LEATHER = ArmorSet(shoulders=42952, chest=48689)  # Stained Shadowcraft Spaulders / Tunic
CASTER_LEATHER = ArmorSet(shoulders=42984, chest=48687)  # Preened Ironfeather Shoulders / Breastplate
CLOTH = ArmorSet(shoulders=42985, chest=48691)  # Tattered Dreadmist Mantle / Robe

# (melee, caster). The plate set carries melee stats only, so a paladin healing its way through the run wears
# the caster mail one instead.
ARMOR_SETS: dict[int, tuple[ArmorSet, ArmorSet]] = {
    WARRIOR: (PLATE, PLATE),
    PALADIN: (PLATE, CASTER_MAIL),
    HUNTER: (MELEE_MAIL, MELEE_MAIL),
    SHAMAN: (MELEE_MAIL, CASTER_MAIL),
    ROGUE: (MELEE_LEATHER, MELEE_LEATHER),
    DRUID: (MELEE_LEATHER, CASTER_LEATHER),
    PRIEST: (CLOTH, CLOTH),
    MAGE: (CLOTH, CLOTH),
    WARLOCK: (CLOTH, CLOTH),
}

SWIFT_HAND_OF_JUSTICE = 42991
DISCERNING_EYE_OF_THE_BEAST = 42992

# Which classes a weapon is offered to. Proficiency is the floor -- a class that cannot hold the weapon never
# gets it -- and on top of that a weapon whose stats are wasted is left out too: no caster staff for a warrior,
# no attack power for a mage.
HEIRLOOM_WEAPONS: list[tuple[int, list[int]]] = [
    # Bloodied Arcanite Reaper. Strength two-hander: the agility classes can hold it but gain far less from it.
    (42943, [WARRIOR, PALADIN]),
    # Balanced Heartseeker
    (42944, [WARRIOR, HUNTER, SHAMAN, DRUID, ROGUE]),
    # Venerable Dal'Rend's Sacred Charge
    (42945, [WARRIOR, PALADIN, HUNTER, ROGUE]),
    # Charmed Ancient Bone Bow
    (42946, [WARRIOR, HUNTER, ROGUE]),
    # Dignified Headmaster's Charge. Caster staff: warriors and hunters have the proficiency, but it has no
    # interesting stats for them.
    (42947, [*CharacterClass.pure_casters, SHAMAN, DRUID]),
    # Devout Aurastone Hammer
    (42948, [PALADIN, SHAMAN, DRUID, PRIEST]),
    # Venerable Mass of McGowan
    (48716, [WARRIOR, PALADIN, SHAMAN, DRUID, ROGUE]),
    # Repurposed Lava Dredger
    (48718, [WARRIOR, PALADIN, SHAMAN, DRUID]),
]


def weapon_choices(character_class: int) -> list[int]:
    return [weapon for weapon, classes in HEIRLOOM_WEAPONS if character_class in classes]


def weapon_slots(character_class: int) -> int:
    return min(MAX_WEAPON_SLOTS, len(weapon_choices(character_class)))


def trinkets(character_class: int) -> Pieces:
    if character_class in CharacterClass.pure_casters:
        return Pieces(DISCERNING_EYE_OF_THE_BEAST, DISCERNING_EYE_OF_THE_BEAST)
    if character_class in CharacterClass.hybrids:
        return Pieces(SWIFT_HAND_OF_JUSTICE, DISCERNING_EYE_OF_THE_BEAST)
    return Pieces(SWIFT_HAND_OF_JUSTICE, SWIFT_HAND_OF_JUSTICE)


class HeirloomContainer(ItemContainer["HeirloomItem"]):
    """Heirlooms of a kind rather than specific pieces. The player picks which piece each one becomes from the
    Archipelago Stone's preferences, and may change their mind until it arrives."""

    def get_slot_data(self, world: "World"):
        character_class = world.options.character_class.value
        melee, caster = ARMOR_SETS[character_class]
        return {
            "shoulders": [HEIRLOOM_SHOULDERS.id, melee.shoulders, caster.shoulders],
            "chest": [HEIRLOOM_CHEST.id, melee.chest, caster.chest],
            "trinket": [HEIRLOOM_TRINKET.id, *trinkets(character_class)],
            "weapon": [HEIRLOOM_WEAPON.id, weapon_slots(character_class), weapon_choices(character_class)],
        }

    def get_items_for_pool(self, world: "World") -> list[Item]:
        weapons = weapon_slots(world.options.character_class.value)
        return [HEIRLOOM_SHOULDERS, HEIRLOOM_CHEST, HEIRLOOM_TRINKET, *[HEIRLOOM_WEAPON] * weapons]


class HeirloomItem(Item):
    def __init__(self, name: str):
        super().__init__(name, ItemClassification.useful)
        HEIRLOOM_CONTAINER.add(self)


HEIRLOOM_CONTAINER = HeirloomContainer()

HEIRLOOM_SHOULDERS = HeirloomItem("Heirloom Shoulders")
HEIRLOOM_CHEST = HeirloomItem("Heirloom Chest")
HEIRLOOM_TRINKET = HeirloomItem("Heirloom Trinket")
HEIRLOOM_WEAPON = HeirloomItem("Heirloom Weapon")
