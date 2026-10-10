import json
import pkgutil
from dataclasses import dataclass

from .constants import DATA_PACKAGE


@dataclass(frozen=True)
class GlyphModel:
    # item_template: the server module mails the item
    id: int
    name: str
    # ChrClasses.dbc, the same ids as the CharacterClass option
    class_id: int
    minor: bool
    required_level: int

    @staticmethod
    def from_dict(data: object) -> "GlyphModel | None":
        if not isinstance(data, dict):
            return None

        glyph_id = data.get("id")
        name = data.get("name")
        class_id = data.get("class")
        glyph_type = data.get("type")
        required_level = data.get("requiredLevel")
        if (
            not isinstance(glyph_id, int)
            or not isinstance(name, str)
            or not isinstance(class_id, int)
            or glyph_type not in ("major", "minor")
            or not isinstance(required_level, int)
        ):
            return None

        return GlyphModel(id=glyph_id, name=name, class_id=class_id, minor=glyph_type == "minor", required_level=required_level)


def load_glyph_models(resource: str) -> list[GlyphModel]:
    """Read a glyph table out of the data package.

    The failures here are raised rather than swallowed, so a packaging mistake cannot quietly
    generate a world with no glyphs in it.
    """
    raw = pkgutil.get_data(DATA_PACKAGE, resource)
    if raw is None:
        raise FileNotFoundError(f'Could not read "{resource}" from "{DATA_PACKAGE}"')

    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        raise ValueError(f'Expected "{resource}" to hold a list of glyphs, got {type(data).__name__}')

    return [glyph for glyph in map(GlyphModel.from_dict, data) if glyph is not None]


GLYPH_MODELS = load_glyph_models("glyphs.json")
