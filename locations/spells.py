from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from worlds.generic.Rules import set_rule

from .. import regions
from ..conditions import combine_rules, required_level
from ..items.progressive import PROGRESSIVE_RIDING
from ..spell_model import SPELL_DISPLAY_NAMES, SPELL_MODELS, SpellKind, SpellModel
from .location_container import LocationContainer
from .location_registry import Location


class Spell(Location):
    """Training one spell at a trainer.

    The trainer keeps offering the spell until the check is sent, and hands over nothing when it is
    bought: the ability itself comes back through the multiworld as an item.
    """

    def __init__(self, data: SpellModel):
        super().__init__(f"Train: {SPELL_DISPLAY_NAMES[(data.class_id, data.id)]}")
        SPELLS_CONTAINER.add(self)
        self.data = data
        self.region = regions.get_region_by_level(data.req_level)


class SpellsContainer(LocationContainer[Spell]):
    def __init__(self) -> None:
        super().__init__()
        self.all_spells: list[Spell] = []

    def add(self, location: Spell):
        super().add(location)
        self.all_spells.append(location)

    def build_locations(self, world: "World") -> list[Spell]:
        return [loc for loc in self.all_spells if loc.data.is_learnable_by(world)]

    def get_slot_data(self, world: "World"):
        return [[loc.data.id, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        return [(loc.region, loc) for loc in self.build_locations(world)]

    def set_rules(self, world: "World"):
        # What the riding skill stands at after each rung of the ladder, so anything sold against a
        # riding requirement can ask for however many rungs it takes to get there
        riding_ranks = [rank.req_skill_rank for rank in PROGRESSIVE_RIDING.ranks_for(world)]

        for loc in self.build_locations(world):
            # The region only gates the bracket floor, while a trainer refuses to teach a spell one
            # level early, so the exact level is a rule of its own. A weapon master asks for no level
            # at all for most of what it sells, which leaves nothing to say.
            level_rule = required_level(loc.data.req_level, world) if loc.data.req_level > 1 else None

            # Anything a mount trainer sells is priced in riding skill: a rank is only sold to a
            # character holding the one below it, and Cold Weather Flying only to one that has
            # reached Expert. Both come out as a number of ladder items to hold first.
            riding_rule = None
            if loc.data.kind in (SpellKind.RIDING, SpellKind.MOUNT):
                needed = sum(1 for rank in riding_ranks if rank < loc.data.req_skill_rank)
                if needed:
                    riding_rule = lambda state, needed=needed: state.has(PROGRESSIVE_RIDING.name, world.player, needed)

            if level_rule or riding_rule:
                set_rule(world.get_location(loc.name), combine_rules(level_rule, riding_rule))


SPELLS_CONTAINER = SpellsContainer()

for spell in SPELL_MODELS:
    Spell(spell)
