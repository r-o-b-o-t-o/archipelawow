from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

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

# How many weapon skills a seed picks among those its character can raise, on top of Defense. Each is a grind to its
# cap, and all of them would come to well over a hundred checks for most classes.
PICKED_WEAPON_SKILLS = 3


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
        # The container is a singleton shared by every player, and the roll must not be re-rolled per caller
        self.__skills_cache: "WeakKeyDictionary[World, dict[int, str | None]]" = WeakKeyDictionary()

    def add(self, location: Skill):
        super().add(location)
        self.all_skills.append(location)

    def skill_items(self, world: "World") -> dict[int, str | None]:
        """The skills that are locations for this world, by id, each with the item teaching it or None for a starting one.

        Rolled once so that every caller sees the same set.
        """
        skills = self.__skills_cache.get(world)
        if skills is None:
            skills = self.pick_skills(world)
            self.__skills_cache[world] = skills

        return skills

    def pick_skills(self, world: "World") -> dict[int, str | None]:
        if world.options.character_class.value in CharacterClass.pure_casters:
            return {}

        character_class, race = world.options.character_class.value, world.options.character_race.value
        items = {item.data.id: item.name for item in SPELL_ITEMS_CONTAINER.build_pool(world) if item.data.kind == SpellKind.WEAPON}
        available: dict[int, str | None] = {}
        for skill in SKILL_MODELS:
            if skill.is_starting_skill_of(character_class, race):
                available[skill.id] = None
            elif skill.spell in items:
                available[skill.id] = items[skill.spell]

        # Bear and cat form raise Defense but no weapon skill
        count = 0 if character_class == CharacterClass.option_druid else PICKED_WEAPON_SKILLS
        weapons = [skill_id for skill_id in available if skill_id != SKILL_DEFENSE]
        picked = set(world.random.sample(weapons, min(count, len(weapons))))
        return {skill_id: item for skill_id, item in available.items() if skill_id == SKILL_DEFENSE or skill_id in picked}

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
