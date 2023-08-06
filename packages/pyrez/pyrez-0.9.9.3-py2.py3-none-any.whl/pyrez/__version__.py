
from datetime import datetime
__author__ = "Luis (Lugg) Gustavo"
__author_email__ = "luis.silva.1044894@gmail.com"
__copyright__ = "Copyright (c) 2018-{} {}".format(datetime.utcnow().year, __author__)
__build__ = 0x000909
__description__ = "An open-source wrapper for Hi-Rez Studios API (Paladins, Realm Royale, and Smite), written in Python"
__license__ = "MIT"
__package_name__ = "pyrez"
__url__ = "https://luissilva1044894.github.io/Pyrez/"
__version__ = "0.9.9.3"
__title__ = "{}-{}".format(__package_name__.capitalize(), __version__)
version = __version__

from collections import namedtuple
version_info = namedtuple("VersionInfo", "major minor micro releaselevel serial")(major=0, minor=9, micro=9, releaselevel="beta", serial=0)

__all__ = (
    "__title__",
    "__description__",
    "__url__",
    "__version__",
    "__author__",
    #"__email__",
    "__license__",
    "__copyright__",
)
