from typing import TYPE_CHECKING, Literal, Optional

if TYPE_CHECKING:
    from .data.items.zones import Zone
    from .world import World

from BaseClasses import CollectionRule, CollectionState
from worlds.generic.Rules import set_rule

from .data.items.levels import LEVEL_UP


def set_location_rule(location: str, item: str, world: "World"):
    set_rule(world.get_location(location), lambda state: state.has(item, world.player))


def combine_rules(*args: Optional[CollectionRule], operator: Literal["and", "or"] = "and") -> CollectionRule:
    def f(state: CollectionState) -> bool:
        for rule in args:
            if not rule:
                continue
            result = rule(state)
            if operator == "and" and result is False:
                return False
            if operator == "or" and result is True:
                return True
        return operator == "and"

    return f


def required_level(level: int, world: "World") -> CollectionRule:
    return lambda state: state.has(LEVEL_UP.name, world.player, level - 1)


def has_item(item: str, world: "World") -> CollectionRule:
    return lambda state: state.has(item, world.player)


def has_all(items: list[str], world: "World") -> CollectionRule:
    return lambda state: state.has_all([item for item in items], world.player)


def has_any(items: list[str], world: "World") -> CollectionRule:
    return lambda state: state.has_any([item for item in items], world.player)


def required_level_and_items(level: int, alliance_items: list[str], horde_items: list[str], world: "World") -> CollectionRule:
    level_condition = required_level(level, world)

    if world.is_alliance():
        return combine_rules(level_condition, has_all(alliance_items, world))
    return combine_rules(level_condition, has_all(horde_items, world))


def required_level_and_zones(level: int, alliance_zones: list["Zone"], horde_zones: list["Zone"], world: "World"):
    return required_level_and_items(level, [i.name for i in alliance_zones], [i.name for i in horde_zones], world)
