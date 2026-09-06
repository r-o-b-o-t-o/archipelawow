import json
import pkgutil
from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from .constants import DATA_PACKAGE

if TYPE_CHECKING:
    from .world import World


class SpellKind(IntEnum):
    """What a spell entry is, which decides whether the seed puts it in the pool at all."""

    CLASS = 1
    RIDING = 2
    STARTER = 3
    WEAPON = 4
    MOUNT = 5


class SpellFaction(IntEnum):
    """Which team's trainers teach a spell. A handful of paladin spells come in one copy per side."""

    ANY = 0
    ALLIANCE = 1
    HORDE = 2


class SpellExpansion(IntEnum):
    """The furthest a seed has to go for the trainer that teaches a spell to be reachable."""

    CLASSIC = 0
    BURNING_CRUSADE = 1
    WRATH = 2


KIND_NAMES = {
    "class": SpellKind.CLASS,
    "riding": SpellKind.RIDING,
    "starter": SpellKind.STARTER,
    "weapon": SpellKind.WEAPON,
    "mount": SpellKind.MOUNT,
}

CLASS_NAMES = {
    1: "Warrior",
    2: "Paladin",
    3: "Hunter",
    4: "Rogue",
    5: "Priest",
    6: "Death Knight",
    7: "Shaman",
    8: "Mage",
    9: "Warlock",
    11: "Druid",
}

FACTION_NAMES = {
    SpellFaction.ALLIANCE: "Alliance",
    SpellFaction.HORDE: "Horde",
}


@dataclass(frozen=True)
class SpellModel:
    id: int
    name: str
    class_id: int
    class_races: tuple[tuple[int, int], ...]
    req_level: int
    req_skill_rank: int
    taught_spells: tuple[int, ...]
    race_mask: int
    faction: SpellFaction
    expansion: SpellExpansion
    kind: SpellKind

    @staticmethod
    def from_dict(data: object) -> "SpellModel | None":
        if not isinstance(data, dict):
            return None

        spell_id = data.get("id")
        name = data.get("name")
        raw_kind = data.get("kind")
        kind = KIND_NAMES.get(raw_kind) if isinstance(raw_kind, str) else None
        if not isinstance(spell_id, int) or not isinstance(name, str) or kind is None:
            return None

        return SpellModel(
            id=spell_id,
            name=name,
            class_id=SpellModel._to_int(data.get("classId")),
            class_races=SpellModel._to_class_races(data.get("classRaces")),
            req_level=SpellModel._to_int(data.get("reqLevel")),
            req_skill_rank=SpellModel._to_int(data.get("reqSkillRank")),
            taught_spells=tuple(SpellModel._to_int_list(data.get("taughtSpells"))),
            race_mask=SpellModel._to_int(data.get("raceMask")),
            faction=SpellFaction(SpellModel._to_int(data.get("factions"))),
            expansion=SpellExpansion(SpellModel._to_int(data.get("expansion"))),
            kind=kind,
        )

    @staticmethod
    def _to_int(value: object) -> int:
        return value if isinstance(value, int) else 0

    @staticmethod
    def _to_int_list(value: object) -> list[int]:
        if not isinstance(value, list):
            return []
        return [item for item in value if isinstance(item, int)]

    @staticmethod
    def _to_class_races(value: object) -> tuple[tuple[int, int], ...]:
        """The races of each class a weapon skill is sold to, keyed by class id.

        Only the weapon skills carry this, and only as an object: JSON has no integer keys, so the
        class ids come back as strings.
        """
        if not isinstance(value, dict):
            return ()

        return tuple((int(class_id), race_mask) for class_id, race_mask in value.items()
                     if str(class_id).isdecimal() and isinstance(race_mask, int))

    def races_of_class(self, class_id: int) -> int:
        """The races of one class a weapon skill is still sold to, or no race at all."""
        return next((races for spell_class, races in self.class_races if spell_class == class_id), 0)

    def is_learnable_by(self, world: "World") -> bool:
        """Whether this seed's character could ever train this spell.

        Filters out the other classes, the other faction, the races a spell is closed to, and
        anything a trainer would only offer past the level the seed stops at, or from a continent it
        never opens -- the flying ranks of riding are sold in Outland and nowhere else. A spell whose
        first rank is out of reach can never be trained, so putting it in the pool would spend a
        progression item on a check nobody can reach.
        """
        if self.req_level > world.level_cap():
            return False

        if self.expansion >= SpellExpansion.WRATH and not world.has_wotlk_content():
            return False

        if self.expansion >= SpellExpansion.BURNING_CRUSADE and not world.has_tbc_content():
            return False

        if self.kind == SpellKind.STARTER and not world.options.spells_randomize_starter_abilities:
            return False

        character_class = world.options.character_class.value
        if self.kind == SpellKind.WEAPON:
            # A weapon skill is one entry for every race and class that can buy it, so the entry
            # answers here where a class spell answers with the class it belongs to. Race counts for
            # as much as class: a weapon master sells nothing a character was created holding, and
            # which weapon that is comes down to race -- a troll hunter starts with Bows, a draenei
            # one with Crossbows, and each can buy what the other started with.
            races = self.races_of_class(character_class)
            if not races & (1 << (world.options.character_race.value - 1)):
                return False

        if self.kind in (SpellKind.CLASS, SpellKind.STARTER) and self.class_id != character_class:
            return False

        if self.race_mask and not self.race_mask & (1 << (world.options.character_race.value - 1)):
            return False

        if self.faction == SpellFaction.ALLIANCE and not world.is_alliance():
            return False

        if self.faction == SpellFaction.HORDE and not world.is_horde():
            return False

        return True


def load_spell_models(resource: str) -> list[SpellModel]:
    """Read a spell table out of the data package.

    The failures here are raised rather than swallowed, so a packaging mistake cannot quietly
    generate a world with no spells in it.
    """
    raw = pkgutil.get_data(DATA_PACKAGE, resource)
    if raw is None:
        raise FileNotFoundError(f'Could not read "{resource}" from "{DATA_PACKAGE}"')

    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        raise ValueError(f'Expected "{resource}" to hold a list of spells, got {type(data).__name__}')

    return [spell for spell in map(SpellModel.from_dict, data) if spell is not None]


def build_display_names(spells: list[SpellModel]) -> dict[tuple[int, int], str]:
    """A unique label per spell, keyed by class and spell id.

    Archipelago keys items and locations by name across every seed a registry holds, while WoW hands
    the same name to spells of different classes -- a mage and a druid both have a Remove Curse --
    and, for a few paladin spells, to one copy per faction. Only the names that actually clash are
    qualified, so the common case stays the plain spell name.
    """
    by_name: dict[str, list[SpellModel]] = {}
    for spell in spells:
        by_name.setdefault(spell.name, []).append(spell)

    names: dict[tuple[int, int], str] = {}
    for name, sharing in by_name.items():
        for spell in sharing:
            names[(spell.class_id, spell.id)] = name if len(sharing) == 1 else _qualified_name(spell, sharing)

    return names


def _qualified_name(spell: SpellModel, sharing: list[SpellModel]) -> str:
    """`spell`'s name with just enough after it to tell it apart from the others sharing it."""
    if len({other.class_id for other in sharing}) > 1:
        return f"{spell.name} ({CLASS_NAMES.get(spell.class_id, spell.class_id)})"

    if len({other.faction for other in sharing}) > 1:
        return f"{spell.name} ({FACTION_NAMES.get(spell.faction, spell.faction)})"

    return f"{spell.name} ({spell.id})"


SPELL_MODELS = load_spell_models("spells.json")
SPELL_DISPLAY_NAMES = build_display_names(SPELL_MODELS)
