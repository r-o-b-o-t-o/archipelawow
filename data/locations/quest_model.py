import json
import pkgutil
from dataclasses import dataclass


@dataclass(frozen=True)
class QuestZoneModel:
    id: int
    name: str

    @staticmethod
    def from_dict(data: object) -> "QuestZoneModel | None":
        if not isinstance(data, dict):
            return None

        zone_id = data.get("id")
        zone_name = data.get("name")
        if not isinstance(zone_id, int) or not isinstance(zone_name, str):
            return None

        return QuestZoneModel(id=zone_id, name=zone_name)


@dataclass(frozen=True)
class QuestModel:
    id: int
    title: str
    display_title: str
    min_level: int | None
    recommended_level: int | None
    suggested_group_size: int | None
    races: list[int] | None
    classes: list[int] | None
    quest_sort_area: QuestZoneModel | None
    is_breadcrumb: bool
    is_dungeon: bool
    requires_any: list[int]
    requires_all: list[int]
    start_zones: list[QuestZoneModel]
    end_zones: list[QuestZoneModel]
    objective_zones: list[QuestZoneModel]

    @staticmethod
    def from_dict(data: object) -> "QuestModel | None":
        if not isinstance(data, dict):
            return None

        quest_id = data.get("id")
        title = data.get("title")
        if not isinstance(quest_id, int) or not isinstance(title, str):
            return None

        # The display title carries into permanent location names, so fall back to the validated title
        display_title = data.get("displayTitle")
        if not isinstance(display_title, str):
            display_title = title

        start_zones = QuestModel._parse_zones(data.get("startZones"))
        end_zones = QuestModel._parse_zones(data.get("endZones"))
        objective_zones = QuestModel._parse_zones(data.get("objectiveZones"))

        return QuestModel(
            id=quest_id,
            title=title,
            display_title=display_title,
            min_level=QuestModel._to_int_or_none(data.get("minLevel")),
            recommended_level=QuestModel._to_int_or_none(data.get("recommendedLevel")),
            suggested_group_size=QuestModel._to_int_or_none(data.get("suggestedGroupSize")),
            races=QuestModel._to_int_list_or_none(data.get("races")),
            classes=QuestModel._to_int_list_or_none(data.get("classes")),
            quest_sort_area=QuestZoneModel.from_dict(data.get("questSortArea")),
            is_breadcrumb=QuestModel._to_bool(data.get("isBreadcrumb")),
            is_dungeon=QuestModel._to_bool(data.get("isDungeon")),
            requires_any=QuestModel._to_int_list(data.get("requiresAny")),
            requires_all=QuestModel._to_int_list(data.get("requiresAll")),
            start_zones=start_zones,
            end_zones=end_zones,
            objective_zones=objective_zones,
        )

    @staticmethod
    def _to_int_or_none(value: object) -> int | None:
        return value if isinstance(value, int) else None

    @staticmethod
    def _to_bool(value: object) -> bool:
        return value if isinstance(value, bool) else False

    @staticmethod
    def _to_int_list(value: object) -> list[int]:
        if not isinstance(value, list):
            return []
        return [item for item in value if isinstance(item, int)]

    @staticmethod
    def _to_int_list_or_none(value: object) -> list[int] | None:
        if value is None:
            return None
        return QuestModel._to_int_list(value)

    @staticmethod
    def _parse_zones(value: object) -> list[QuestZoneModel]:
        if not isinstance(value, list):
            return []

        zones: list[QuestZoneModel] = []
        for zone_data in value:
            zone = QuestZoneModel.from_dict(zone_data)
            if zone is not None:
                zones.append(zone)
        return zones


def load_quest_models_by_id(package: str, resource: str) -> dict[int, QuestModel]:
    """Read the quest table shipped alongside `package`.

    Goes through pkgutil rather than the filesystem because an installed .apworld is a zip: the path
    a module reports lives inside the archive, so opening it, or asking whether it exists, fails. The
    failures here are raised rather than swallowed, so a packaging mistake cannot quietly generate a
    world with no quests in it.
    """
    raw = pkgutil.get_data(package, resource)
    if raw is None:
        raise FileNotFoundError(f'Could not read "{resource}" from "{package}"')

    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        raise ValueError(f'Expected "{resource}" to hold a list of quests, got {type(data).__name__}')

    quests_by_id: dict[int, QuestModel] = {}
    for quest_data in data:
        quest = QuestModel.from_dict(quest_data)
        if quest is not None:
            quests_by_id[quest.id] = quest

    return quests_by_id
