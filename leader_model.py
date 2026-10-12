import json
import pkgutil
from dataclasses import dataclass

from .constants import DATA_PACKAGE


@dataclass(frozen=True)
class LeaderModel:
    # creature_template entry: the server module checks the location when the character greets this creature
    id: int
    name: str
    # The capital the leader stands in
    zone_id: int

    @staticmethod
    def from_dict(data: object) -> "LeaderModel | None":
        if not isinstance(data, dict):
            return None

        creature_id = data.get("id")
        name = data.get("name")
        zone_data = data.get("zone")
        zone_id = zone_data.get("id") if isinstance(zone_data, dict) else None
        if not isinstance(creature_id, int) or not isinstance(name, str) or not isinstance(zone_id, int):
            return None

        return LeaderModel(id=creature_id, name=name, zone_id=zone_id)


def load_leader_models(resource: str) -> list[LeaderModel]:
    """Read the faction leader table out of the data package.

    The failures here are raised rather than swallowed, so a packaging mistake cannot quietly
    generate a world with no leaders in it.
    """
    raw = pkgutil.get_data(DATA_PACKAGE, resource)
    if raw is None:
        raise FileNotFoundError(f'Could not read "{resource}" from "{DATA_PACKAGE}"')

    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        raise ValueError(f'Expected "{resource}" to hold a list of leaders, got {type(data).__name__}')

    return [leader for leader in map(LeaderModel.from_dict, data) if leader is not None]


LEADER_MODELS = load_leader_models("leaders.json")
