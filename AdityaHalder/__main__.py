import asyncio, os, pyrogram

from .console import (
    load_sudo_users, LOGGER as logs
)
from .modules import collect_all_variables
from .modules.clients import start_all_clients
from .plugins import import_all_plugins

loop = asyncio.get_event_loop()


async def main():
    logs.info("🔄 𝙋𝙧𝙤𝙘𝙚𝙨𝙨𝙞𝙣𝙜, 𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩❗...")
    if "cache" not in os.listdir():
        os.mkdir("cache")
    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    await collect_all_variables()
    await load_sudo_users()
    await start_all_clients()
    await import_all_plugins()
    logs.info("✅ 𝘽𝙂𝙏 𝙋𝙡𝙖𝙮𝙚𝙧 𝙞𝙨 𝙉𝙤𝙬 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 ‼️")
    await pyrogram.idle()


if __name__ == "__main__":
    loop.run_until_complete(main())
    logs.info("❎ 𝙂𝙤𝙤𝙙𝙗𝙮𝙚, 𝘽𝙤𝙩 𝙉𝙤𝙬 𝙎𝙩𝙤𝙥𝙥𝙚𝙙 ‼️")
