import collections
from pathlib import Path

root_dir = Path(__file__).parent.parent

ConfigOption = collections.namedtuple("ConfigOption", ("name", "default", "help"))

CONFIG_OPTIONS = (
    ConfigOption("force-https", False, "Always use https:// URLs"),
    ConfigOption("page-size", 500, "Maximum number of things shown on a page"),
    ConfigOption("page-size-max", 1000, "Maximum value accepted for page-size"),
    ConfigOption("root-dir", root_dir, "Path of root directory"),
)

DEFAULT_CONFIG = {option.name: option.default for option in CONFIG_OPTIONS}
