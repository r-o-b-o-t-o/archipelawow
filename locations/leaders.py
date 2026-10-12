from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from ..conditions import has_zone
from ..items import zones
from ..items.zones import ZONES_CONTAINER, Zone
from .location_container import LocationContainer
from .location_registry import Location


class Leader(Location):
    def __init__(self, title: str, name: str, creature_id: int, zone: Zone):
        super().__init__(f"{title}: say /hi to {name}")
        LEADERS_CONTAINER.add(self)
        self.creature_id = creature_id
        self.zone = zone


class LeadersContainer(LocationContainer[Leader]):
    def build_locations(self, world: "World"):
        # Capitals are sided, so the pool only holds the character's own faction's
        zones_in_pool = set(ZONES_CONTAINER.build_pool(world))
        return [loc for loc in LEADERS if loc.zone in zones_in_pool]

    def get_slot_data(self, world: "World"):
        return [[loc.creature_id, loc.id] for loc in self.build_locations(world)]

    def get_locations(self, world: "World") -> list[tuple[str, Location]]:
        return [(loc.zone.region(world), loc) for loc in self.build_locations(world)]

    def set_rules(self, world: "World"):
        for leader in self.build_locations(world):
            world.set_rule(world.get_location(leader.name), has_zone(leader.zone, world))


LEADERS_CONTAINER = LeadersContainer()

LEADERS = [
    Leader("Hungry Like the Wolf", "King Varian Wrynn", 29611, zones.STORMWIND_CITY),
    Leader("In the Hall of the Mountain King", "King Magni Bronzebeard", 2784, zones.IRONFORGE),
    Leader("Careless Whisper", "Tyrande Whisperwind", 7999, zones.DARNASSUS),
    Leader("Space Truckin'", "Prophet Velen", 17468, zones.THE_EXODAR),
    Leader("Riders on the Storm", "Thrall", 4949, zones.ORGRIMMAR),
    Leader("Buffalo Soldier", "Cairne Bloodhoof", 3057, zones.THUNDER_BLUFF),
    Leader("Bring Me to Life", "Lady Sylvanas Windrunner", 10181, zones.UNDERCITY),
    Leader("Eye of the Tiger", "Lor'themar Theron", 16802, zones.SILVERMOON_CITY),
]
