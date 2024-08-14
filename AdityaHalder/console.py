import logging, os, time

from os import getenv
from pyrogram import filters
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    format="[%(levelname)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "logs.txt", maxBytes=(1024 * 1024 * 5), backupCount=10
        ),
        logging.StreamHandler(),
    ],
)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)


if os.path.exists("Internal"):
   load_dotenv("Internal")


# REQUIRED VARIABLES
API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
MONGO_DB_URL = getenv("MONGO_DB_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 0))

# OPTIONAL VARIABLES
START_IMAGE = getenv(
    "START_IMAGE",
    "https://graph.org/file/d4bc06ada79821eb01025.jpg"
)
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0))


# ASSISTANT SESSION STRINGS
STRING1 = getenv("STRING1", None)
STRING2 = getenv("STRING2", None)
STRING3 = getenv("STRING3", None)
STRING4 = getenv("STRING4", None)
STRING5 = getenv("STRING5", None)



# Don't Edit This Codes From This Line

runtime = time.time()
PLUGINS = {}
LOGGER = logging.getLogger("Bikash")
SUDOERS = filters.user()


async def load_sudo_users():
    from .modules.clients import mongodb
    global SUDOERS
    SUDOERS.add(OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if OWNER_ID not in sudoers:
        sudoers.append(OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)
    LOGGER.info("🤖 𝙎𝙪𝙙𝙤 𝙐𝙨𝙚𝙧𝙨 𝙇𝙤𝙖𝙙𝙚𝙙.")

