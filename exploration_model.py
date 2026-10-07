import json
import pkgutil
from dataclasses import dataclass

from .constants import DATA_PACKAGE


@dataclass(frozen=True)
class ExplorationModel:
    # Achievement_Criteria.dbc: the server module checks the location when the core credits this criterion
    id: int
    name: str
    # The zone the subzone lies in, which for a capital is the capital rather than the zone its achievement explores
    zone_id: int

    @staticmethod
    def from_dict(data: object) -> "ExplorationModel | None":
        if not isinstance(data, dict):
            return None

        criteria_id = data.get("id")
        name = data.get("name")
        zone_data = data.get("zone")
        zone_id = zone_data.get("id") if isinstance(zone_data, dict) else None
        if not isinstance(criteria_id, int) or not isinstance(name, str) or not isinstance(zone_id, int):
            return None

        return ExplorationModel(id=criteria_id, name=name, zone_id=zone_id)


def load_exploration_models(resource: str) -> list[ExplorationModel]:
    """Read a subzone table out of the data package.

    The failures here are raised rather than swallowed, so a packaging mistake cannot quietly
    generate a world with no subzones in it.
    """
    raw = pkgutil.get_data(DATA_PACKAGE, resource)
    if raw is None:
        raise FileNotFoundError(f'Could not read "{resource}" from "{DATA_PACKAGE}"')

    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        raise ValueError(f'Expected "{resource}" to hold a list of subzones, got {type(data).__name__}')

    return [exploration for exploration in map(ExplorationModel.from_dict, data) if exploration is not None]


EXPLORATION_MODELS = load_exploration_models("explorations.json")
