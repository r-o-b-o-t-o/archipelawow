from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

from ..conditions import has_zone
from ..items.zones import ZONES_CONTAINER
from ..leader_model import LEADER_MODELS, LeaderModel
from .location_container import LocationContainer
from .location_registry import Location


class Leader(Location):
    def __init__(self, data: LeaderModel):
        super().__init__(f"{TITLES[data.name]}: say /hi to {data.name}")
        LEADERS_CONTAINER.add(self)
        self.creature_id = data.id
        self.zone = ZONES_CONTAINER.zones[data.zone_id]


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

# What each leader's location is titled, by the name the extract gives the leader
TITLES = {
    "King Varian Wrynn": "Hungry Like the Wolf",
    "King Magni Bronzebeard": "In the Hall of the Mountain King",
    "Tyrande Whisperwind": "Careless Whisper",
    "Prophet Velen": "Space Truckin'",
    "Thrall": "Riders on the Storm",
    "Cairne Bloodhoof": "Buffalo Soldier",
    "Lady Sylvanas Windrunner": "Bring Me to Life",
    "Lor'themar Theron": "Eye of the Tiger",
}

LEADERS = [Leader(data) for data in LEADER_MODELS]
