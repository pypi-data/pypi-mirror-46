# coding: utf-8
# stdlib imports
import sys
import os
from pathlib import Path

# local imports
from ofxtools import utils

__all__ = ["CONFIGDIR", "USERCONFIGDIR"]


#  CONFIGDIR = utils.fixpath(os.path.dirname(__file__))
CONFIGDIR = Path(__file__).parent.resolve()


HOME = Path.home().resolve()


# Cross-platform specification of user configuration directory
system = sys.platform.lower()
environ = os.environ

if system.startswith("win"):  # Windows
    if "APPDATA" in environ:
        CONFIGHOME = Path(environ["APPDATA"]).resolve()
    else:
        CONFIGHOME = HOME / "AppData" / "Roaming"
elif system.startswith("darwin"):  # Mac
    CONFIGHOME = HOME / "Library" / "Preferences"
else:  # Linux
    if "XDG_CONFIG_HOME" in os.environ:
        CONFIGHOME = Path(environ["XDG_CONFIG_HOME"])
    else:
        CONFIGHOME = HOME / ".config"


USERCONFIGDIR = CONFIGHOME / "ofxtools"


USERCONFIGDIR.mkdir(parents=True, exist_ok=True)
