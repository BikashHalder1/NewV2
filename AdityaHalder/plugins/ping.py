from .. import (
   bot, cdx, check_errors
)

from datetime import datetime
from pyrogram import filters


@bot.on_message(cdx("ping"))
@check_errors
async def check_ping(client, message):
    start = datetime.now()
    m = await message.reply_text("**🤖 Ping !**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await m.edit(f"**🤖 Pinged !\nLatency:** `{ms}` ms")



__NAME__ = "Pɪɴɢ"
__MENU__ = """
`.ping` - **Check Ping Latency !!**
"""
