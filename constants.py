GAME_NAME = "World of Warcraft"

# Where the extracts the data extractor writes are shipped. They sit in a package of their own,
# apart from the code that reads them, and are reached through pkgutil rather than the filesystem
# because an installed .apworld is a zip: the path a module reports lives inside the archive, so
# opening it, or asking whether it exists, fails.
DATA_PACKAGE = f"{__package__}.data"
