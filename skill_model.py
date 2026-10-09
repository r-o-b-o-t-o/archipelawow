import json
import pkgutil
from dataclasses import dataclass

from .constants import DATA_PACKAGE


@dataclass(frozen=True)
class SkillModel:
    # SkillLine.dbc: the server module checks the locations when the skill rises
    id: int
    name: str
    # The weapon skill of spells.json a character not created holding the skill buys it with, 0 for Defense and Unarmed
    spell: int
    # The races of each class created holding the skill, keyed by class id
    starting_class_races: tuple[tuple[int, int], ...]

    @staticmethod
    def from_dict(data: object) -> "SkillModel | None":
        if not isinstance(data, dict):
            return None

        skill_id = data.get("id")
        name = data.get("name")
        if not isinstance(skill_id, int) or not isinstance(name, str):
            return None

        spell = data.get("spell")
        class_races = data.get("startingClassRaces")
        return SkillModel(
            id=skill_id,
            name=name,
            spell=spell if isinstance(spell, int) else 0,
            # JSON has no integer keys, so the class ids come back as strings
            starting_class_races=(
                tuple((int(key), races) for key, races in class_races.items() if str(key).isdecimal() and isinstance(races, int))
                if isinstance(class_races, dict)
                else ()
            ),
        )

    def is_starting_skill_of(self, class_id: int, race: int) -> bool:
        """Whether a character of this class and race is created holding the skill."""
        races = next((races for skill_class, races in self.starting_class_races if skill_class == class_id), 0)
        return bool(races & (1 << (race - 1)))


def load_skill_models(resource: str) -> list[SkillModel]:
    """Read a skill table out of the data package.

    The failures here are raised rather than swallowed, so a packaging mistake cannot quietly
    generate a world with no skills in it.
    """
    raw = pkgutil.get_data(DATA_PACKAGE, resource)
    if raw is None:
        raise FileNotFoundError(f'Could not read "{resource}" from "{DATA_PACKAGE}"')

    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        raise ValueError(f'Expected "{resource}" to hold a list of skills, got {type(data).__name__}')

    return [skill for skill in map(SkillModel.from_dict, data) if skill is not None]


SKILL_MODELS = load_skill_models("skills.json")
