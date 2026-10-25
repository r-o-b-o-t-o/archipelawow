import json
import pkgutil
from dataclasses import dataclass
from enum import IntEnum

from .constants import DATA_PACKAGE


class BossFaction(IntEnum):
    """The one team that can fight a boss, the other being friendly with it."""

    ANY = 0
    ALLIANCE = 1
    HORDE = 2


@dataclass(frozen=True)
class BossModel:
    # DungeonEncounter.dbc, normal difficulty: the server module checks the location when the core credits this encounter.
    # Past the DBC's ids, an encounter the module credits itself, such as Sergeant Bly's or the Obsidian Sentinel's.
    id: int
    name: str
    map_id: int
    faction: BossFaction

    @staticmethod
    def from_dict(data: object) -> "BossModel | None":
        if not isinstance(data, dict):
            return None

        boss_id = data.get("id")
        name = data.get("name")
        map_data = data.get("map")
        map_id = map_data.get("id") if isinstance(map_data, dict) else None
        if not isinstance(boss_id, int) or not isinstance(name, str) or not isinstance(map_id, int):
            return None

        factions = data.get("factions")
        return BossModel(id=boss_id, name=name, map_id=map_id, faction=BossFaction(factions if isinstance(factions, int) else 0))


def load_boss_models(resource: str) -> list[BossModel]:
    """Read a boss table out of the data package.

    The failures here are raised rather than swallowed, so a packaging mistake cannot quietly
    generate a world with no bosses in it.
    """
    raw = pkgutil.get_data(DATA_PACKAGE, resource)
    if raw is None:
        raise FileNotFoundError(f'Could not read "{resource}" from "{DATA_PACKAGE}"')

    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        raise ValueError(f'Expected "{resource}" to hold a list of bosses, got {type(data).__name__}')

    return [boss for boss in map(BossModel.from_dict, data) if boss is not None]


BOSS_MODELS = load_boss_models("bosses.json")
