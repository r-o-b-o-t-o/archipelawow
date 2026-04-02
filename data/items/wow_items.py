from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

from BaseClasses import ItemClassification

from ...options import CharacterClass
from .item_container import ItemContainer
from .item_registry import Item


class WoWItemsContainer(ItemContainer):
    def build_pool(self, world: "World"):
        items = [*BAGS, GOLD_POUCH]

        match world.options.character_class:
            case CharacterClass.option_warrior:
                items += GLYPHS_WARRIOR
            case CharacterClass.option_paladin:
                items += GLYPHS_PALADIN

        return items

    def get_slot_data(self, world: "World"):
        return [[item.id, item.wow_item_id] for item in self.build_pool(world)]

    def get_items_for_pool(self, world: "World") -> list[Item]:
        return list(self.build_pool(world))


class WoWItem(Item):
    def __init__(self, name: str, wow_item_id: int, classification: ItemClassification, pool_count=1):
        super().__init__(name, classification, pool_count)
        WOW_ITEMS_CONTAINER.add(self)
        self.wow_item_id = wow_item_id


WOW_ITEMS_CONTAINER = WoWItemsContainer()

BROWN_LEATHER_SATCHEL = WoWItem("Brown Leather Satchel", 4498, ItemClassification.filler, pool_count=2)
HUGE_BROWN_SACK = WoWItem("Huge Brown Sack", 4499, ItemClassification.filler, pool_count=2)
TRAVELERS_BACKPACK = WoWItem("Traveler's Backpack", 4500, ItemClassification.filler, pool_count=2)
FROSTWEAVE_BAG = WoWItem("Frostweave Bag", 41599, ItemClassification.filler, pool_count=2)
BAGS = [BROWN_LEATHER_SATCHEL, HUGE_BROWN_SACK, TRAVELERS_BACKPACK, FROSTWEAVE_BAG]

GOLD_POUCH = WoWItem("Gold Pouch", 38539, ItemClassification.filler, pool_count=1)  # TODO: create actual item

# GLYPH_MAJOR_WARRIOR_INTERVENE = WoWItem("Glyph of Intervene", 43419, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_DEVASTATE = WoWItem("Glyph of Devastate", 43415, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_SHIELD_WALL = WoWItem("Glyph of Shield Wall", 45797, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_SPELL_REFLECTION = WoWItem("Glyph of Spell Reflection", 45795, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_ENRAGED_REGENERATION = WoWItem("Glyph of Enraged Regeneration", 45794, ItemClassification.useful)
# GLYPH_MAJOR_WARRIOR_VIGILANCE = WoWItem("Glyph of Vigilance", 45793, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_SHOCKWAVE = WoWItem("Glyph of Shockwave", 45792, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_BLADESTORM = WoWItem("Glyph of Bladestorm", 45790, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_BLOCKING = WoWItem("Glyph of Blocking", 43425, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_BLOODTHIRST = WoWItem("Glyph of Bloodthirst", 43412, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_MORTAL_STRIKE = WoWItem("Glyph of Mortal Strike", 43421, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_WHIRLWIND = WoWItem("Glyph of Whirlwind", 43432, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_SWEEPING_STRIKES = WoWItem("Glyph of Sweeping Strikes", 43428, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_EXECUTION = WoWItem("Glyph of Execution", 43416, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_LAST_STAND = WoWItem("Glyph of Last Stand", 43426, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_CLEAVING = WoWItem("Glyph of Cleaving", 43414, ItemClassification.useful)
# GLYPH_MAJOR_WARRIOR_BARBARIC_INSULTS = WoWItem("Glyph of Barbaric Insults", 43420, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_VICTORY_RUSH = WoWItem("Glyph of Victory Rush", 43431, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_REVENGE = WoWItem("Glyph of Revenge", 43424, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_OVERPOWER = WoWItem("Glyph of Overpower", 43422, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_SUNDER_ARMOR = WoWItem("Glyph of Sunder Armor", 43427, ItemClassification.useful)
# GLYPH_MAJOR_WARRIOR_TAUNT = WoWItem("Glyph of Taunt", 43429, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_HAMSTRING = WoWItem("Glyph of Hamstring", 43417, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_RESONATING_POWER = WoWItem("Glyph of Resonating Power", 43430, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_RAPID_CHARGE = WoWItem("Glyph of Rapid Charge", 43413, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_RENDING = WoWItem("Glyph of Rending", 43423, ItemClassification.useful)
GLYPH_MAJOR_WARRIOR_HEROIC_STRIKE = WoWItem("Glyph of Heroic Strike", 43418, ItemClassification.useful)
GLYPH_MINOR_WARRIOR_COMMAND = WoWItem("Glyph of Command", 49084, ItemClassification.filler)
GLYPH_MINOR_WARRIOR_ENDURING_VICTORY = WoWItem("Glyph of Enduring Victory", 43400, ItemClassification.filler)
GLYPH_MINOR_WARRIOR_MOCKING_BLOW = WoWItem("Glyph of Mocking Blow", 43398, ItemClassification.filler)
GLYPH_MINOR_WARRIOR_BLOODRAGE = WoWItem("Glyph of Bloodrage", 43396, ItemClassification.filler)
GLYPH_MINOR_WARRIOR_THUNDER_CLAP = WoWItem("Glyph of Thunder Clap", 43399, ItemClassification.filler)
GLYPH_MINOR_WARRIOR_CHARGE = WoWItem("Glyph of Charge", 43397, ItemClassification.filler)
GLYPH_MINOR_WARRIOR_BATTLE = WoWItem("Glyph of Battle", 43395, ItemClassification.filler)
GLYPHS_WARRIOR = [
    # GLYPH_MAJOR_WARRIOR_INTERVENE,
    GLYPH_MAJOR_WARRIOR_DEVASTATE,
    GLYPH_MAJOR_WARRIOR_SHIELD_WALL,
    GLYPH_MAJOR_WARRIOR_SPELL_REFLECTION,
    GLYPH_MAJOR_WARRIOR_ENRAGED_REGENERATION,
    # GLYPH_MAJOR_WARRIOR_VIGILANCE,
    GLYPH_MAJOR_WARRIOR_SHOCKWAVE,
    GLYPH_MAJOR_WARRIOR_BLADESTORM,
    GLYPH_MAJOR_WARRIOR_BLOCKING,
    GLYPH_MAJOR_WARRIOR_BLOODTHIRST,
    GLYPH_MAJOR_WARRIOR_MORTAL_STRIKE,
    GLYPH_MAJOR_WARRIOR_WHIRLWIND,
    GLYPH_MAJOR_WARRIOR_SWEEPING_STRIKES,
    GLYPH_MAJOR_WARRIOR_EXECUTION,
    GLYPH_MAJOR_WARRIOR_LAST_STAND,
    GLYPH_MAJOR_WARRIOR_CLEAVING,
    # GLYPH_MAJOR_WARRIOR_BARBARIC_INSULTS,
    GLYPH_MAJOR_WARRIOR_VICTORY_RUSH,
    GLYPH_MAJOR_WARRIOR_REVENGE,
    GLYPH_MAJOR_WARRIOR_OVERPOWER,
    GLYPH_MAJOR_WARRIOR_SUNDER_ARMOR,
    # GLYPH_MAJOR_WARRIOR_TAUNT,
    GLYPH_MAJOR_WARRIOR_HAMSTRING,
    GLYPH_MAJOR_WARRIOR_RESONATING_POWER,
    GLYPH_MAJOR_WARRIOR_RAPID_CHARGE,
    GLYPH_MAJOR_WARRIOR_RENDING,
    GLYPH_MAJOR_WARRIOR_HEROIC_STRIKE,
    GLYPH_MINOR_WARRIOR_COMMAND,
    GLYPH_MINOR_WARRIOR_ENDURING_VICTORY,
    GLYPH_MINOR_WARRIOR_MOCKING_BLOW,
    GLYPH_MINOR_WARRIOR_BLOODRAGE,
    GLYPH_MINOR_WARRIOR_THUNDER_CLAP,
    GLYPH_MINOR_WARRIOR_CHARGE,
    GLYPH_MINOR_WARRIOR_BATTLE,
]

GLYPH_MAJOR_PALADIN_AVENGING_WRATH = WoWItem("Glyph of Avenging Wrath", 41107, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_AVENGERS_SHIELD = WoWItem("Glyph of Avenger's Shield", 41101, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_SEAL_OF_VENGEANCE = WoWItem("Glyph of Seal of Vengeance", 43869, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_SEAL_OF_RIGHTEOUSNESS = WoWItem("Glyph of Seal of Righteousness", 43868, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_HOLY_WRATH = WoWItem("Glyph of Holy Wrath", 43867, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_HAMMER_OF_WRATH = WoWItem("Glyph of Hammer of Wrath", 41097, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_SALVATION = WoWItem("Glyph of Salvation", 45747, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_HOLY_SHOCK = WoWItem("Glyph of Holy Shock", 45746, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_DIVINE_PLEA = WoWItem("Glyph of Divine Plea", 45745, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_SHIELD_OF_RIGHTEOUSNESS = WoWItem("Glyph of Shield of Righteousness", 45744, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_DIVINE_STORM = WoWItem("Glyph of Divine Storm", 45743, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_HAMMER_OF_THE_RIGHTEOUS = WoWItem("Glyph of Hammer of the Righteous", 45742, ItemClassification.useful)
# GLYPH_MAJOR_PALADIN_BEACON_OF_LIGHT = WoWItem("Glyph of Beacon of Light", 45741, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_SEAL_OF_WISDOM = WoWItem("Glyph of Seal of Wisdom", 41109, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_SEAL_OF_LIGHT = WoWItem("Glyph of Seal of Light", 41110, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_CLEANSING = WoWItem("Glyph of Cleansing", 41104, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_TURN_EVIL = WoWItem("Glyph of Turn Evil", 41102, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_FLASH_OF_LIGHT = WoWItem("Glyph of Flash of Light", 41105, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_EXORCISM = WoWItem("Glyph of Exorcism", 41103, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_CONSECRATION = WoWItem("Glyph of Consecration", 41099, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_CRUSADER_STRIKE = WoWItem("Glyph of Crusader Strike", 41098, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_SEAL_OF_COMMAND = WoWItem("Glyph of Seal of Command", 41094, ItemClassification.useful)
# GLYPH_MAJOR_PALADIN_RIGHTEOUS_DEFENSE = WoWItem("Glyph of Righteous Defense", 41100, ItemClassification.useful)
# GLYPH_MAJOR_PALADIN_SPIRITUAL_ATTUNEMENT = WoWItem("Glyph of Spiritual Attunement", 41096, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_DIVINITY = WoWItem("Glyph of Divinity", 41108, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_HAMMER_OF_JUSTICE = WoWItem("Glyph of Hammer of Justice", 41095, ItemClassification.useful)
GLYPH_MAJOR_PALADIN_JUDGEMENT = WoWItem("Glyph of Judgement", 41092, ItemClassification.useful)
# GLYPH_MAJOR_PALADIN_HOLY_LIGHT = WoWItem("Glyph of Holy Light", 41106, ItemClassification.useful)
GLYPH_MINOR_PALADIN_THE_WISE = WoWItem("Glyph of the Wise", 43369, ItemClassification.filler)
GLYPH_MINOR_PALADIN_BLESSING_OF_KINGS = WoWItem("Glyph of Blessing of Kings", 43365, ItemClassification.filler)
GLYPH_MINOR_PALADIN_SENSE_UNDEAD = WoWItem("Glyph of Sense Undead", 43368, ItemClassification.filler)
GLYPH_MINOR_PALADIN_BLESSING_OF_WISDOM = WoWItem("Glyph of Blessing of Wisdom", 43366, ItemClassification.filler)
GLYPH_MINOR_PALADIN_LAY_ON_HANDS = WoWItem("Glyph of Lay on Hands", 43367, ItemClassification.filler)
GLYPH_MINOR_PALADIN_BLESSING_OF_MIGHT = WoWItem("Glyph of Blessing of Might", 43340, ItemClassification.filler)
GLYPHS_PALADIN = [
    GLYPH_MAJOR_PALADIN_AVENGING_WRATH,
    GLYPH_MAJOR_PALADIN_AVENGERS_SHIELD,
    GLYPH_MAJOR_PALADIN_SEAL_OF_VENGEANCE,
    GLYPH_MAJOR_PALADIN_SEAL_OF_RIGHTEOUSNESS,
    GLYPH_MAJOR_PALADIN_HOLY_WRATH,
    GLYPH_MAJOR_PALADIN_HAMMER_OF_WRATH,
    GLYPH_MAJOR_PALADIN_SALVATION,
    GLYPH_MAJOR_PALADIN_HOLY_SHOCK,
    GLYPH_MAJOR_PALADIN_DIVINE_PLEA,
    GLYPH_MAJOR_PALADIN_SHIELD_OF_RIGHTEOUSNESS,
    GLYPH_MAJOR_PALADIN_DIVINE_STORM,
    GLYPH_MAJOR_PALADIN_HAMMER_OF_THE_RIGHTEOUS,
    # GLYPH_MAJOR_PALADIN_BEACON_OF_LIGHT,
    GLYPH_MAJOR_PALADIN_SEAL_OF_WISDOM,
    GLYPH_MAJOR_PALADIN_SEAL_OF_LIGHT,
    GLYPH_MAJOR_PALADIN_CLEANSING,
    GLYPH_MAJOR_PALADIN_TURN_EVIL,
    GLYPH_MAJOR_PALADIN_FLASH_OF_LIGHT,
    GLYPH_MAJOR_PALADIN_EXORCISM,
    GLYPH_MAJOR_PALADIN_CONSECRATION,
    GLYPH_MAJOR_PALADIN_CRUSADER_STRIKE,
    GLYPH_MAJOR_PALADIN_SEAL_OF_COMMAND,
    # GLYPH_MAJOR_PALADIN_RIGHTEOUS_DEFENSE,
    # GLYPH_MAJOR_PALADIN_SPIRITUAL_ATTUNEMENT,
    GLYPH_MAJOR_PALADIN_DIVINITY,
    GLYPH_MAJOR_PALADIN_HAMMER_OF_JUSTICE,
    GLYPH_MAJOR_PALADIN_JUDGEMENT,
    # GLYPH_MAJOR_PALADIN_HOLY_LIGHT,
    GLYPH_MINOR_PALADIN_THE_WISE,
    GLYPH_MINOR_PALADIN_BLESSING_OF_KINGS,
    GLYPH_MINOR_PALADIN_SENSE_UNDEAD,
    GLYPH_MINOR_PALADIN_BLESSING_OF_WISDOM,
    GLYPH_MINOR_PALADIN_LAY_ON_HANDS,
    GLYPH_MINOR_PALADIN_BLESSING_OF_MIGHT,
]
