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
        mention = query.from_user.mention
        text = f"""**➻ 𝗛𝗲𝗹𝗹𝗼, {mention}

🥀 𝗜 𝗮𝗺 𝗔𝗻 𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱 » 𝗛𝗶𝗴𝗵 𝗤𝘂𝗮𝗹𝗶𝘁𝘆
𝗥𝗼𝗯𝗼𝘁, 𝗜 𝗰𝗮𝗻 𝗛𝗲𝗹𝗽 🌿 𝗬𝗼𝘂 𝘁𝗼 𝗠𝗮𝗻𝗮𝗴𝗲
𝗬𝗼𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗢𝗿 𝗚𝗿𝗼𝘂𝗽𝘀.

🐬 𝗠𝘂𝘀𝘁 𝗛𝗶𝘁 ❥ 𝗛𝗲𝗹𝗽 𝗔𝗻𝗱 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀
𝗕𝘂𝘁𝘁𝗼𝗻 ⋟ 𝗧𝗼 𝗚𝗲𝘁 𝗠𝗼𝗿𝗲 𝗜𝗻𝗳𝗼 🦋 𝗢𝗳 𝗠𝘆
𝗠𝗼𝗱𝘂𝗹𝗲𝘀 𝗔𝗻𝗱 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀.

💐 𝗙𝗲𝗲𝗹 𝗙𝗿𝗲𝗲 𝗧𝗼 𝗨𝘀𝗲 › 𝗠𝗲 𝗔𝗻𝗱 𝗦𝗵𝗮𝗿𝗲
𝗪𝗶𝘁𝗵 𝗬𝗼𝘂𝗿 𝗢𝘁𝗵𝗲𝗿 𝗙𝗿𝗶𝗲𝗻𝗱𝘀.**"""
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
