# Ai-Userbot Version
__version__ = "v2.0"


# All Clients
from .modules.clients import (
    App, Bot, Call, mongodb
)
app = App()
bot = Bot()
call = Call()

# Database
adb = mongodb


# Command Handlers
from .modules.helpers import (
    cdx, cdz, rgx
)
cdx = cdx
cdz = cdz
rgx = rgx


# Edit Or Reply
from .modules.helpers import (
    check_errors
)
check_errors = check_errors


# Logger
from .console import LOGGER
logs = LOGGER


# Plugins
from .console import PLUGINS
plugs = PLUGINS


#Sudo Users
from .console import SUDOERS
SUDOERS = SUDOERS

# Variables
from . import console as config
vars = config

