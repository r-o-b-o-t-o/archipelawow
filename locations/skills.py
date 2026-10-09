from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from rule_builder.rules import Has, Rule

from .. import regions
from ..conditions import required_level
from ..items.spells import SPELLS_CONTAINER as SPELL_ITEMS_CONTAINER
from ..options import CharacterClass
from ..skill_model import SKILL_MODELS, SkillModel
from ..spell_model import SpellKind
from .location_container import LocationContainer
from .location_registry import Location

# A skill's cap is five times the character's level
SKILL_PER_LEVEL = 5

# SkillLine.dbc
SKILL_DEFENSE = 95


class Skill(Location):
    """Raising a weapon skill or Defense to its cap at the last level of a bracket."""

    def __init__(self, data: SkillModel, level: int):
        super().__init__(f"Skill: {data.name} {level * SKILL_PER_LEVEL}")
        SKILLS_CONTAINER.add(self)
        self.data = data
        self.level = level
        self.region = regions.get_region_by_level(level)


class SkillsContainer(LocationContainer[Skill]):
    def __init__(self) -> None:
        super().__init__()
        self.all_skills: list[Skill] = []

    def add(self, location: Skill):
        super().add(location)
        self.all_skills.append(location)

    def skill_items(self, world: "World") -> dict[int, str | None]:
        """The skills this seed's character can raise, by id, each with the item teaching it or None for a starting one."""
        if world.options.character_class.value in CharacterClass.pure_casters:
            return {}

        character_class, race = world.options.character_class.value, world.options.character_race.value
        items = {item.data.id: item.name for item in SPELL_ITEMS_CONTAINER.build_pool(world) if item.data.kind == SpellKind.WEAPON}
        skills: dict[int, str | None] = {}
        for skill in SKILL_MODELS:
            # Bear and cat form raise Defense but no weapon skill
            if character_class == CharacterClass.option_druid and skill.id != SKILL_DEFENSE:
                continue

            if skill.is_starting_skill_of(character_class, race):
                skills[skill.id] = None
            elif skill.spell in items:
                skills[skill.id] = items[skill.spell]
        return skills

    def build_locations(self, world: "World") -> list[Skill]:
        skills = self.skill_items(world)
        return [loc for loc in self.all_skills if loc.data.id in skills and loc.level <= world.level_cap()]

    def get_slot_data(self, world: "World"):
        return [[loc.data.id, loc.level * SKILL_PER_LEVEL, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        return [(loc.region, loc) for loc in self.build_locations(world)]

    def set_rules(self, world: "World"):
        skills = self.skill_items(world)
        for loc in self.build_locations(world):
            rule: Rule = required_level(loc.level)
            item = skills[loc.data.id]
            if item is not None:
                rule &= Has(item)
            world.set_rule(world.get_location(loc.name), rule)


SKILLS_CONTAINER = SkillsContainer()

for skill in SKILL_MODELS:
    # The last level of each bracket
    for level in range(5, 81, 5):
        Skill(skill, level)
