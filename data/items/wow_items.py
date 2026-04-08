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

GLYPH_MAJOR_SHAMAN_FIRE_ELEMENTAL_TOTEM = WoWItem("Glyph of Fire Elemental Totem", 41529, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_LAVA = WoWItem("Glyph of Lava", 41524, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_ELEMENTAL_MASTERY = WoWItem("Glyph of Elemental Mastery", 41552, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_MANA_TIDE_TOTEM = WoWItem("Glyph of Mana Tide Totem", 41538, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_STONECLAW_TOTEM = WoWItem("Glyph of Stoneclaw Totem", 45778, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_HEX = WoWItem("Glyph of Hex", 45777, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_TOTEM_OF_WRATH = WoWItem("Glyph of Totem of Wrath", 45776, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_EARTH_SHIELD = WoWItem("Glyph of Earth Shield", 45775, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_RIPTIDE = WoWItem("Glyph of Riptide", 45772, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_FERAL_SPIRIT = WoWItem("Glyph of Feral Spirit", 45771, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_THUNDER = WoWItem("Glyph of Thunder", 45770, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_STORMSTRIKE = WoWItem("Glyph of Stormstrike", 41539, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_CHAIN_HEAL = WoWItem("Glyph of Chain Heal", 41517, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_CHAIN_LIGHTNING = WoWItem("Glyph of Chain Lightning", 41518, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_WINDFURY_WEAPON = WoWItem("Glyph of Windfury Weapon", 41542, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_EARTHLIVING_WEAPON = WoWItem("Glyph of Earthliving Weapon", 41527, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_LESSER_HEALING_WAVE = WoWItem("Glyph of Lesser Healing Wave", 41535, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_WATER_MASTERY = WoWItem("Glyph of Water Mastery", 41541, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_FROST_SHOCK = WoWItem("Glyph of Frost Shock", 41547, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_HEALING_STREAM_TOTEM = WoWItem("Glyph of Healing Stream Totem", 41533, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_FIRE_NOVA = WoWItem("Glyph of Fire Nova", 41530, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_LAVA_LASH = WoWItem("Glyph of Lava Lash", 41540, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_FLAMETONGUE_WEAPON = WoWItem("Glyph of Flametongue Weapon", 41532, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_FLAME_SHOCK = WoWItem("Glyph of Flame Shock", 41531, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_LIGHTNING_SHIELD = WoWItem("Glyph of Lightning Shield", 41537, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_SHOCKING = WoWItem("Glyph of Shocking", 41526, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_LIGHTNING_BOLT = WoWItem("Glyph of Lightning Bolt", 41536, ItemClassification.useful)
GLYPH_MAJOR_SHAMAN_HEALING_WAVE = WoWItem("Glyph of Healing Wave", 41534, ItemClassification.useful)
GLYPH_MINOR_SHAMAN_THUNDERSTORM = WoWItem("Glyph of Thunderstorm", 44923, ItemClassification.filler)
GLYPH_MINOR_SHAMAN_ASTRAL_RECALL = WoWItem("Glyph of Astral Recall", 43381, ItemClassification.filler)
GLYPH_MINOR_SHAMAN_RENEWED_LIFE = WoWItem("Glyph of Renewed Life", 43385, ItemClassification.filler)
GLYPH_MINOR_SHAMAN_WATER_WALKING = WoWItem("Glyph of Water Walking", 43388, ItemClassification.filler)
GLYPH_MINOR_SHAMAN_WATER_BREATHING = WoWItem("Glyph of Water Breathing", 43344, ItemClassification.filler)
GLYPH_MINOR_SHAMAN_WATER_SHIELD = WoWItem("Glyph of Water Shield", 43386, ItemClassification.filler)
GLYPH_MINOR_SHAMAN_GHOST_WOLF = WoWItem("Glyph of Ghost Wolf", 43725, ItemClassification.filler)
GLYPHS_SHAMAN = [
    GLYPH_MAJOR_SHAMAN_FIRE_ELEMENTAL_TOTEM,
    GLYPH_MAJOR_SHAMAN_LAVA,
    GLYPH_MAJOR_SHAMAN_ELEMENTAL_MASTERY,
    GLYPH_MAJOR_SHAMAN_MANA_TIDE_TOTEM,
    GLYPH_MAJOR_SHAMAN_STONECLAW_TOTEM,
    GLYPH_MAJOR_SHAMAN_HEX,
    GLYPH_MAJOR_SHAMAN_TOTEM_OF_WRATH,
    GLYPH_MAJOR_SHAMAN_EARTH_SHIELD,
    GLYPH_MAJOR_SHAMAN_RIPTIDE,
    GLYPH_MAJOR_SHAMAN_FERAL_SPIRIT,
    GLYPH_MAJOR_SHAMAN_THUNDER,
    GLYPH_MAJOR_SHAMAN_STORMSTRIKE,
    GLYPH_MAJOR_SHAMAN_CHAIN_HEAL,
    GLYPH_MAJOR_SHAMAN_CHAIN_LIGHTNING,
    GLYPH_MAJOR_SHAMAN_WINDFURY_WEAPON,
    GLYPH_MAJOR_SHAMAN_EARTHLIVING_WEAPON,
    GLYPH_MAJOR_SHAMAN_LESSER_HEALING_WAVE,
    GLYPH_MAJOR_SHAMAN_WATER_MASTERY,
    GLYPH_MAJOR_SHAMAN_FROST_SHOCK,
    GLYPH_MAJOR_SHAMAN_HEALING_STREAM_TOTEM,
    GLYPH_MAJOR_SHAMAN_FIRE_NOVA,
    GLYPH_MAJOR_SHAMAN_LAVA_LASH,
    GLYPH_MAJOR_SHAMAN_FLAMETONGUE_WEAPON,
    GLYPH_MAJOR_SHAMAN_FLAME_SHOCK,
    GLYPH_MAJOR_SHAMAN_LIGHTNING_SHIELD,
    GLYPH_MAJOR_SHAMAN_SHOCKING,
    GLYPH_MAJOR_SHAMAN_LIGHTNING_BOLT,
    GLYPH_MAJOR_SHAMAN_HEALING_WAVE,
    GLYPH_MINOR_SHAMAN_THUNDERSTORM,
    GLYPH_MINOR_SHAMAN_ASTRAL_RECALL,
    GLYPH_MINOR_SHAMAN_RENEWED_LIFE,
    GLYPH_MINOR_SHAMAN_WATER_WALKING,
    GLYPH_MINOR_SHAMAN_WATER_BREATHING,
    GLYPH_MINOR_SHAMAN_WATER_SHIELD,
    GLYPH_MINOR_SHAMAN_GHOST_WOLF,
]

GLYPH_MAJOR_ROGUE_VIGOR = WoWItem("Glyph of Vigor", 42971, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_DEADLY_THROW = WoWItem("Glyph of Deadly Throw", 42959, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_CLOAK_OF_SHADOWS = WoWItem("Glyph of Cloak of Shadows", 45769, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_MUTILATE = WoWItem("Glyph of Mutilate", 45768, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_TRICKS_OF_THE_TRADE = WoWItem("Glyph of Tricks of the Trade", 45767, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_FAN_OF_KNIVES = WoWItem("Glyph of Fan of Knives", 45766, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_SHADOW_DANCE = WoWItem("Glyph of Shadow Dance", 45764, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_KILLING_SPREE = WoWItem("Glyph of Killing Spree", 45762, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_HUNGER_FOR_BLOOD = WoWItem("Glyph of Hunger for Blood", 45761, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_ADRENALINE_RUSH = WoWItem("Glyph of Adrenaline Rush", 42954, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_PREPARATION = WoWItem("Glyph of Preparation", 42968, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_HEMORRHAGE = WoWItem("Glyph of Hemorrhage", 42967, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_BLADE_FLURRY = WoWItem("Glyph of Blade Flurry", 42957, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_GHOSTLY_STRIKE = WoWItem("Glyph of Ghostly Strike", 42965, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_RUPTURE = WoWItem("Glyph of Rupture", 42969, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_CRIPPLING_POISON = WoWItem("Glyph of Crippling Poison", 42958, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_AMBUSH = WoWItem("Glyph of Ambush", 42955, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_FEINT = WoWItem("Glyph of Feint", 42963, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_GARROTE = WoWItem("Glyph of Garrote", 42964, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_EXPOSE_ARMOR = WoWItem("Glyph of Expose Armor", 42962, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_SAP = WoWItem("Glyph of Sap", 42970, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_SLICE_AND_DICE = WoWItem("Glyph of Slice and Dice", 42973, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_SPRINT = WoWItem("Glyph of Sprint", 42974, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_EVASION = WoWItem("Glyph of Evasion", 42960, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_GOUGE = WoWItem("Glyph of Gouge", 42966, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_BACKSTAB = WoWItem("Glyph of Backstab", 42956, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_SINISTER_STRIKE = WoWItem("Glyph of Sinister Strike", 42972, ItemClassification.useful)
GLYPH_MAJOR_ROGUE_EVISCERATE = WoWItem("Glyph of Eviscerate", 42961, ItemClassification.useful)
GLYPH_MINOR_ROGUE_SAFE_FALL = WoWItem("Glyph of Safe Fall", 43378, ItemClassification.filler)
GLYPH_MINOR_ROGUE_DISTRACT = WoWItem("Glyph of Distract", 43376, ItemClassification.filler)
GLYPH_MINOR_ROGUE_VANISH = WoWItem("Glyph of Vanish", 43380, ItemClassification.filler)
GLYPH_MINOR_ROGUE_PICK_LOCK = WoWItem("Glyph of Pick Lock", 43377, ItemClassification.filler)
GLYPH_MINOR_ROGUE_BLURRED_SPEED = WoWItem("Glyph of Blurred Speed", 43379, ItemClassification.filler)
GLYPH_MINOR_ROGUE_PICK_POCKET = WoWItem("Glyph of Pick Pocket", 43343, ItemClassification.filler)
GLYPHS_ROGUE = [
    GLYPH_MAJOR_ROGUE_VIGOR,
    GLYPH_MAJOR_ROGUE_DEADLY_THROW,
    GLYPH_MAJOR_ROGUE_CLOAK_OF_SHADOWS,
    GLYPH_MAJOR_ROGUE_MUTILATE,
    GLYPH_MAJOR_ROGUE_TRICKS_OF_THE_TRADE,
    GLYPH_MAJOR_ROGUE_FAN_OF_KNIVES,
    GLYPH_MAJOR_ROGUE_SHADOW_DANCE,
    GLYPH_MAJOR_ROGUE_KILLING_SPREE,
    GLYPH_MAJOR_ROGUE_HUNGER_FOR_BLOOD,
    GLYPH_MAJOR_ROGUE_ADRENALINE_RUSH,
    GLYPH_MAJOR_ROGUE_PREPARATION,
    GLYPH_MAJOR_ROGUE_HEMORRHAGE,
    GLYPH_MAJOR_ROGUE_BLADE_FLURRY,
    GLYPH_MAJOR_ROGUE_GHOSTLY_STRIKE,
    GLYPH_MAJOR_ROGUE_RUPTURE,
    GLYPH_MAJOR_ROGUE_CRIPPLING_POISON,
    GLYPH_MAJOR_ROGUE_AMBUSH,
    GLYPH_MAJOR_ROGUE_FEINT,
    GLYPH_MAJOR_ROGUE_GARROTE,
    GLYPH_MAJOR_ROGUE_EXPOSE_ARMOR,
    GLYPH_MAJOR_ROGUE_SAP,
    GLYPH_MAJOR_ROGUE_SLICE_AND_DICE,
    GLYPH_MAJOR_ROGUE_SPRINT,
    GLYPH_MAJOR_ROGUE_EVASION,
    GLYPH_MAJOR_ROGUE_GOUGE,
    GLYPH_MAJOR_ROGUE_BACKSTAB,
    GLYPH_MAJOR_ROGUE_SINISTER_STRIKE,
    GLYPH_MAJOR_ROGUE_EVISCERATE,
    GLYPH_MINOR_ROGUE_SAFE_FALL,
    GLYPH_MINOR_ROGUE_DISTRACT,
    GLYPH_MINOR_ROGUE_VANISH,
    GLYPH_MINOR_ROGUE_PICK_LOCK,
    GLYPH_MINOR_ROGUE_BLURRED_SPEED,
    GLYPH_MINOR_ROGUE_PICK_POCKET,
]
