import dataclasses
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .world import World

from BaseClasses import CollectionRule, Entrance, Location
from rule_builder.rules import Rule, True_

# The rules the launcher's tracker evaluates (ui/src/tracker/types.ts there): it would take any other for one
# that always holds, so building one fails generation instead
TRACKER_RULES = {"True_", "False_", "Has", "HasAll", "HasAny", "HasAllCounts", "HasAnyCount", "And", "Or"}


def export_logic(world: "World") -> dict[str, Any]:
    """The world's resolved rules, for a tracker to tell which locations are in logic without running the world.

    Rules are deduplicated into a table and referenced by index: most quests share theirs with others of the same
    zones and level. A location is in logic when its region is reachable from the origin through the entrances,
    and its own rule holds.
    """
    rules: dict[Rule.Resolved, int] = {}
    table: list[dict[str, Any]] = []

    def rule_index(spot: str, rule: CollectionRule) -> int:
        if rule is Location.access_rule or rule is Entrance.access_rule:
            rule = True_().resolve(world)
        if not isinstance(rule, Rule.Resolved):
            raise TypeError(f'The rule of "{spot}" was not built with the rule builder, so a tracker cannot read it')
        if rule not in rules:
            rules[rule] = len(table)
            table.append(serialize(spot, rule))
        return rules[rule]

    regions = [region.name for region in world.get_regions()]
    region_index = {name: index for index, name in enumerate(regions)}
    entrances = [
        [region_index[region.name], region_index[entrance.connected_region.name], rule_index(entrance.name, entrance.access_rule)]
        for region in world.get_regions()
        for entrance in region.exits
        if entrance.connected_region
    ]
    locations = [
        [location.address, region_index[location.parent_region.name], rule_index(location.name, location.access_rule)]
        for location in world.get_locations()
        if location.address is not None and location.parent_region
    ]

    return {
        "rules": table,
        "regions": regions,
        "origin": region_index[world.origin_region_name],
        "entrances": entrances,
        "locations": locations,
        "goal": rule_index("the goal", world.multiworld.completion_condition[world.player]),
    }


def serialize(spot: str, rule: Rule.Resolved) -> dict[str, Any]:
    """A resolved rule's fields, named after the rule it was resolved from (Has, And...)."""
    name = type(rule).__qualname__.removesuffix(".Resolved")
    if name not in TRACKER_RULES:
        raise TypeError(f'The rule of "{spot}" uses {name}, which trackers cannot read')
    data: dict[str, Any] = {"rule": name}
    for field in dataclasses.fields(rule):
        if field.name in ("player", "caching_enabled"):
            continue
        value = getattr(rule, field.name)
        data[field.name] = [serialize(spot, child) for child in value] if field.name == "children" else value
    return data
