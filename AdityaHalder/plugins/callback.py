import time

from .. import bot, rgx, console, logs
from ..modules.helpers import get_readable_time
from ..modules.utilities import (
    get_served_chats, get_served_users
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.on_callback_query(rgx("force_close"))
async def close_menu(client, query):
    try:
        return await query.message.delete()
    except:
        pass



@bot.on_callback_query(rgx("help_menu"))
async def help_menu(client, query):
    try:
        text = f"""**👽 𝗔𝗹𝗹 𝗠𝗲𝗺𝗯𝗲𝗿𝘀 𝗖𝗮𝗻 𝗨𝘀𝗲:
/play songname - Play Audio
/vplay song name - Play Video

👾 𝗢𝗻𝗹𝘆 𝗙𝗼𝗿 𝗖𝗵𝗮𝘁 𝗔𝗱𝗺𝗶𝗻𝘀:
/pause - Pause Current Stream
/resume - Resume Streaming
/skip - Play Next Audio/Video
/end - Leave VC & Clear Queue

𝗡𝗼𝘁𝗲: All Commands Will Work
Only in Channels/Groups.**"""
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🤖 𝗢𝘄𝗻𝗲𝗿 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀",
                        callback_data="help_command"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙 𝗕𝗮𝗰𝗸",
                        callback_data="home_menu"
                    )
                ],
            ]
        )
        return await query.message.edit(
            text=text,
            reply_markup=buttons,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"🚫 𝗛𝗠 𝗘𝗿𝗿𝗼𝗿: {e}")
        pass



@bot.on_callback_query(rgx("home_menu"))
async def home_menu(client, query):
    try:
        text = f"""**🥀 𝗛𝗲𝘆, 𝗜 𝗮𝗺 ❥︎ 𝗔𝗻 📀 𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱
𝗔𝗻𝗱 𝗦𝘂𝗽𝗲𝗿𝗳𝗮𝘀𝘁 ❥︎ 𝗩𝗖 𝗣𝗹𝗮𝘆𝗲𝗿 𝗙𝗼𝗿
𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗖𝗵𝗮𝘁𝘀 ✨ ...

💐 𝗙𝗲𝗲𝗹 𝗙𝗿𝗲𝗲 𝗧𝗼 🕊️𝗔𝗱𝗱 𝗠𝗲 ❥︎ 𝗜𝗻
𝗬𝗼𝘂𝗿 𝗖𝗵𝗮𝘁𝘀, 🌺 𝗔𝗻𝗱 𝗘𝗻𝗷𝗼𝘆 ❥︎ 𝗡𝗼
𝗟𝗮𝗴 𝗔𝘂𝗱𝗶𝗼 𝗔𝗻𝗱 𝗩𝗶𝗱𝗲𝗼 🌷...

📡 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 ❥ [𝘽𝙂𝙏](https://t.me/BikashGadgetsTech)**"""
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🥀 𝗔𝗱𝗱 𝗠𝗲 𝗜𝗻 𝗬𝗼𝘂𝗿 𝗖𝗵𝗮𝘁 ✨",
                        url=f"https://t.me/{bot.me.username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🌺 𝗢𝗽𝗲𝗻 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗟𝗶𝘀𝘁 🌿",
                        callback_data="help_menu",
                    )
                ]
            ]
        )
        return await query.message.edit(
            text=text,
            reply_markup=buttons,
            disable_web_page_preview=True
        )
    except Exception as e:
        logs.info(f"🚫 𝗛𝗠 𝗘𝗿𝗿𝗼𝗿: {e}")
        pass



@bot.on_callback_query(rgx("help_command"))
async def help_menu_owner(client, query):
    try:
        user_id = query.from_user.id
        if console.OWNER_ID != 0:
            if user_id != console.OWNER_ID:
                return await query.answer(
                    "⚠️ 𝗢𝗻𝗹𝘆 𝗙𝗼𝗿 𝗕𝗼𝘁 𝗢𝘄𝗻𝗲𝗿❗",
                    show_alert=True
                )
            return await query.answer(
                "✅ 𝗖𝗼𝗺𝗶𝗻𝗴 𝗦𝗼𝗼𝗻❗...",
                show_alert=True
            )
        return await query.answer(
            "❌ 𝗡𝗼𝘁 𝗣𝗿𝗼𝗴𝗿𝗮𝗺𝗺𝗲𝗱 𝗬𝗲𝘁 ‼️",
            show_alert=True
        )
    except Exception as e:
        print(f"🚫 𝗢𝗠 𝗘𝗿𝗿𝗼𝗿: {e}")
        pass



@bot.on_callback_query(rgx("check_stats"))
async def check_total_stats(client, query):
    try:
        user_id = query.from_user.id
        runtime = console.runtime
        boot_time = int(time.time() - runtime)
        uptime = get_readable_time((boot_time))
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        return await query.answer(
            f"""
⏱️ 𝗥𝘂𝗻𝘁𝗶𝗺𝗲 [𝗕𝗼𝗼𝘁]:
☛ {uptime}

🔴 𝗧𝗼𝘁𝗮𝗹 𝗖𝗵𝗮𝘁𝘀: {served_chats}
🔵 𝗧𝗼𝘁𝗮𝗹 𝗨𝘀𝗲𝗿𝘀: {served_users}
            """,
            show_alert=True
        )
    except Exception as e:
        logs.info(f"🚫 𝗢𝗠 𝗘𝗿𝗿𝗼𝗿: {e}")
        pass
