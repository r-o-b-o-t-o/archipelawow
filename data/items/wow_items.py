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
            case CharacterClass.option_hunter:
                items += GLYPHS_HUNTER

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

GLYPH_MAJOR_HUNTER_SNAKE_TRAP = WoWItem("Glyph of Snake Trap", 42913, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_STEADY_SHOT = WoWItem("Glyph of Steady Shot", 42914, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_KILL_SHOT = WoWItem("Glyph of Kill Shot", 45732, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_VOLLEY = WoWItem("Glyph of Volley", 42916, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_TRUESHOT_AURA = WoWItem("Glyph of Trueshot Aura", 42915, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_WYVERN_STING = WoWItem("Glyph of Wyvern Sting", 42917, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_CHIMERA_SHOT = WoWItem("Glyph of Chimera Shot", 45625, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_EXPLOSIVE_SHOT = WoWItem("Glyph of Explosive Shot", 45731, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_BESTIAL_WRATH = WoWItem("Glyph of Bestial Wrath", 42902, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_EXPLOSIVE_TRAP = WoWItem("Glyph of Explosive Trap", 45733, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_SCATTER_SHOT = WoWItem("Glyph of Scatter Shot", 45734, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_RAPTOR_STRIKE = WoWItem("Glyph of Raptor Strike", 45735, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_THE_BEAST = WoWItem("Glyph of the Beast", 42899, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_FROST_TRAP = WoWItem("Glyph of Frost Trap", 42906, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_RAPID_FIRE = WoWItem("Glyph of Rapid Fire", 42911, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_FREEZING_TRAP = WoWItem("Glyph of Freezing Trap", 42905, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_DISENGAGE = WoWItem("Glyph of Disengage", 42904, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_DETERRENCE = WoWItem("Glyph of Deterrence", 42903, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_AIMED_SHOT = WoWItem("Glyph of Aimed Shot", 42897, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_MULTISHOT = WoWItem("Glyph of Multi-Shot", 42910, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_IMMOLATION_TRAP = WoWItem("Glyph of Immolation Trap", 42908, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_ASPECT_OF_THE_VIPER = WoWItem("Glyph of Aspect of the Viper", 42901, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_THE_HAWK = WoWItem("Glyph of the Hawk", 42909, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_HUNTERS_MARK = WoWItem("Glyph of Hunter's Mark", 42907, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_ARCANE_SHOT = WoWItem("Glyph of Arcane Shot", 42898, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_SERPENT_STING = WoWItem("Glyph of Serpent Sting", 42912, ItemClassification.useful)
GLYPH_MAJOR_HUNTER_MENDING = WoWItem("Glyph of Mending", 42900, ItemClassification.useful)
GLYPH_MINOR_HUNTER_THE_PACK = WoWItem("Glyph of the Pack", 43355, ItemClassification.filler)
GLYPH_MINOR_HUNTER_FEIGN_DEATH = WoWItem("Glyph of Feign Death", 43351, ItemClassification.filler)
GLYPH_MINOR_HUNTER_REVIVE_PET = WoWItem("Glyph of Revive Pet", 43338, ItemClassification.filler)
GLYPH_MINOR_HUNTER_POSSESSED_STRENGTH = WoWItem("Glyph of Possessed Strength", 43354, ItemClassification.filler)
GLYPH_MINOR_HUNTER_SCARE_BEAST = WoWItem("Glyph of Scare Beast", 43356, ItemClassification.filler)
GLYPH_MINOR_HUNTER_MEND_PET = WoWItem("Glyph of Mend Pet", 43350, ItemClassification.filler)
GLYPHS_HUNTER = [
    GLYPH_MAJOR_HUNTER_SNAKE_TRAP,
    GLYPH_MAJOR_HUNTER_STEADY_SHOT,
    GLYPH_MAJOR_HUNTER_KILL_SHOT,
    GLYPH_MAJOR_HUNTER_VOLLEY,
    GLYPH_MAJOR_HUNTER_TRUESHOT_AURA,
    GLYPH_MAJOR_HUNTER_WYVERN_STING,
    GLYPH_MAJOR_HUNTER_CHIMERA_SHOT,
    GLYPH_MAJOR_HUNTER_EXPLOSIVE_SHOT,
    GLYPH_MAJOR_HUNTER_BESTIAL_WRATH,
    GLYPH_MAJOR_HUNTER_EXPLOSIVE_TRAP,
    GLYPH_MAJOR_HUNTER_SCATTER_SHOT,
    GLYPH_MAJOR_HUNTER_RAPTOR_STRIKE,
    GLYPH_MAJOR_HUNTER_THE_BEAST,
    GLYPH_MAJOR_HUNTER_FROST_TRAP,
    GLYPH_MAJOR_HUNTER_RAPID_FIRE,
    GLYPH_MAJOR_HUNTER_FREEZING_TRAP,
    GLYPH_MAJOR_HUNTER_DISENGAGE,
    GLYPH_MAJOR_HUNTER_DETERRENCE,
    GLYPH_MAJOR_HUNTER_AIMED_SHOT,
    GLYPH_MAJOR_HUNTER_MULTISHOT,
    GLYPH_MAJOR_HUNTER_IMMOLATION_TRAP,
    GLYPH_MAJOR_HUNTER_ASPECT_OF_THE_VIPER,
    GLYPH_MAJOR_HUNTER_THE_HAWK,
    GLYPH_MAJOR_HUNTER_HUNTERS_MARK,
    GLYPH_MAJOR_HUNTER_ARCANE_SHOT,
    GLYPH_MAJOR_HUNTER_SERPENT_STING,
    GLYPH_MAJOR_HUNTER_MENDING,
    GLYPH_MINOR_HUNTER_THE_PACK,
    GLYPH_MINOR_HUNTER_FEIGN_DEATH,
    GLYPH_MINOR_HUNTER_REVIVE_PET,
    GLYPH_MINOR_HUNTER_POSSESSED_STRENGTH,
    GLYPH_MINOR_HUNTER_SCARE_BEAST,
    GLYPH_MINOR_HUNTER_MEND_PET,
]
