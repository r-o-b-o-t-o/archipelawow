from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from ..world import World

from BaseClasses import ItemClassification

from ..options import CharacterClass
from .wow_items import WoWItem

# Which classes a heirloom is worth sending to. Proficiency is the floor -- a class that cannot hold
# the weapon never gets it -- and on top of that a piece whose stats are wasted is left out too: no
# caster gear for a warrior, no attack power for a mage.
#
# Armor needs no level thinking. A heirloom morphs down to whatever the wearer is trained for and
# back up on its own, so a warrior wears the plate ones from level one and a hunter the mail ones
# (see Player::CanUseItem in the module's core). Each class therefore wants exactly one line of
# armor -- the heaviest it ends up in -- and never the lighter line beneath it.
MELEE_PLATE = [CharacterClass.option_warrior, CharacterClass.option_paladin]
MELEE_MAIL = [CharacterClass.option_hunter, CharacterClass.option_shaman]
CASTER_MAIL = [CharacterClass.option_shaman]
MELEE_LEATHER = [CharacterClass.option_druid, CharacterClass.option_rogue]
CASTER_LEATHER = [CharacterClass.option_druid]
CASTER_CLOTH = [CharacterClass.option_mage, CharacterClass.option_warlock, CharacterClass.option_priest]

# The plate heirlooms carry melee stats only, so a paladin healing its way through the run has no
# armor line of its own. It can wear the caster mail set perfectly well, and asks for it by turning
# on the option that widens the random gear rolls the same way.
CASTER_MAIL_BY_OPTION = [CharacterClass.option_paladin]

PURE_MELEE = [CharacterClass.option_warrior, CharacterClass.option_hunter, CharacterClass.option_rogue]
PURE_CASTER = [CharacterClass.option_mage, CharacterClass.option_warlock, CharacterClass.option_priest]
HYBRID = [CharacterClass.option_paladin, CharacterClass.option_shaman, CharacterClass.option_druid]
ALL_CLASSES = PURE_MELEE + PURE_CASTER + HYBRID


class Heirloom(WoWItem):
    """A heirloom, which scales with the character rather than being outgrown.

    Only the classes in `classes` ever see it in their pool, so the seed never spends a location on
    a piece the slot cannot equip or would gain nothing from. The classes in `optional_classes` can
    make use of it too, but only get it when the player asks for the wider armor selection.
    """

    def __init__(self, name: str, wow_item_id: int, classes: Iterable[int], optional_classes: Iterable[int] = ()):
        super().__init__(name, wow_item_id, ItemClassification.useful)
        self.classes = frozenset(classes)
        self.optional_classes = frozenset(optional_classes)

    def available_to(self, character_class: int, all_armor_types: bool) -> bool:
        """Whether a run for this class should be able to receive the piece."""
        if character_class in self.classes:
            return True

        return all_armor_types and character_class in self.optional_classes


HEIRLOOM_WEAPONS = [
    # Strength two-hander: the agility classes can hold it but gain far less from it.
    Heirloom("Bloodied Arcanite Reaper", 42943, [CharacterClass.option_warrior, CharacterClass.option_paladin]),
    Heirloom(
        "Balanced Heartseeker",
        42944,
        [
            CharacterClass.option_warrior,
            CharacterClass.option_hunter,
            CharacterClass.option_shaman,
            CharacterClass.option_druid,
            CharacterClass.option_rogue,
        ],
    ),
    Heirloom(
        "Venerable Dal'Rend's Sacred Charge",
        42945,
        [CharacterClass.option_warrior, CharacterClass.option_paladin, CharacterClass.option_hunter, CharacterClass.option_rogue],
    ),
    Heirloom("Charmed Ancient Bone Bow", 42946, [CharacterClass.option_warrior, CharacterClass.option_hunter, CharacterClass.option_rogue]),
    # Caster staff: warriors and hunters have the proficiency, but it has no interesting stats for them.
    Heirloom("Dignified Headmaster's Charge", 42947, [*PURE_CASTER, CharacterClass.option_shaman, CharacterClass.option_druid]),
    Heirloom(
        "Devout Aurastone Hammer",
        42948,
        [CharacterClass.option_paladin, CharacterClass.option_shaman, CharacterClass.option_druid, CharacterClass.option_priest],
    ),
    Heirloom(
        "Venerable Mass of McGowan",
        48716,
        [
            CharacterClass.option_warrior,
            CharacterClass.option_paladin,
            CharacterClass.option_shaman,
            CharacterClass.option_druid,
            CharacterClass.option_rogue,
        ],
    ),
    Heirloom(
        "Repurposed Lava Dredger",
        48718,
        [CharacterClass.option_warrior, CharacterClass.option_paladin, CharacterClass.option_shaman, CharacterClass.option_druid],
    ),
]

HEIRLOOM_ARMOR = [
    Heirloom("Polished Spaulders of Valor", 42949, MELEE_PLATE),
    Heirloom("Polished Breastplate of Valor", 48685, MELEE_PLATE),
    Heirloom("Champion Herod's Shoulder", 42950, MELEE_MAIL),
    Heirloom("Champion's Deathdealer Breastplate", 48677, MELEE_MAIL),
    Heirloom("Mystical Pauldrons of Elements", 42951, CASTER_MAIL, CASTER_MAIL_BY_OPTION),
    Heirloom("Mystical Vest of Elements", 48683, CASTER_MAIL, CASTER_MAIL_BY_OPTION),
    Heirloom("Stained Shadowcraft Spaulders", 42952, MELEE_LEATHER),
    Heirloom("Stained Shadowcraft Tunic", 48689, MELEE_LEATHER),
    Heirloom("Preened Ironfeather Shoulders", 42984, CASTER_LEATHER),
    Heirloom("Preened Ironfeather Breastplate", 48687, CASTER_LEATHER),
    Heirloom("Tattered Dreadmist Mantle", 42985, CASTER_CLOTH),
    Heirloom("Tattered Dreadmist Robe", 48691, CASTER_CLOTH),
]

HEIRLOOM_JEWELLERY = [
    Heirloom("Swift Hand of Justice", 42991, PURE_MELEE + HYBRID),
    Heirloom("Discerning Eye of the Beast", 42992, PURE_CASTER + HYBRID),
    Heirloom("Dread Pirate Ring", 50255, ALL_CLASSES),
]

ALL_HEIRLOOMS = [*HEIRLOOM_WEAPONS, *HEIRLOOM_ARMOR, *HEIRLOOM_JEWELLERY]


def heirlooms_for(world: "World") -> list[Heirloom]:
    """The heirlooms this slot's class can make use of."""
    character_class = world.options.character_class.value
    all_armor_types = bool(world.options.gear_include_all_armor_types)
    return [heirloom for heirloom in ALL_HEIRLOOMS if heirloom.available_to(character_class, all_armor_types)]
