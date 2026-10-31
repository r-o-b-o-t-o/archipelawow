from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .items.zones import Zone
    from .world import World

from rule_builder.rules import Has, HasAll, Or, Rule

from .items.levels import LEVEL_UP


def required_level(level: int) -> Rule:
    # Has resolves to True for a count below 1, which is the first level
    return Has(LEVEL_UP.name, level - 1)


def has_zone(zone: "Zone", world: "World") -> Rule:
    """A zone's item, and the level the zone opens at: a zone handed over early is not expected to be used early."""
    return Has(zone.name) & required_level(zone.level(world))


def has_zone_reached_through(zone: "Zone", reached_through: list["Zone"], zones_in_pool: "set[Zone]", world: "World") -> Rule:
    """`has_zone`, and one of `reached_through` on top of it for a spot that `zone` alone does not lead to. A zone out of
    the pool has no item and is left out."""
    through = [has_zone(z, world) for z in reached_through if z in zones_in_pool]
    return has_zone(zone, world) & Or(*through) if through else has_zone(zone, world)


def required_level_and_zones(level: int, alliance_zones: list["Zone"], horde_zones: list["Zone"], world: "World") -> Rule:
    zones = alliance_zones if world.is_alliance() else horde_zones
    return required_level(level) & HasAll(*[zone.name for zone in zones])
