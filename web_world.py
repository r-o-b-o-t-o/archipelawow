from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld as BaseWebWorld

from . import constants
from .options import option_groups, option_presets


class WebWorld(BaseWebWorld):
    game = constants.GAME_NAME
    theme = "ice"  # dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, stone

    setup_en = Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to setting up World of Warcraft with AzerothCore and ArchipelaWoW.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Roboto"],
    )

    # We add these tutorials to our WebWorld by overriding the "tutorials" field
    tutorials = [setup_en]

    # If we have option groups and/or option presets, we need to specify these here as well
    option_groups = option_groups
    options_presets = option_presets
