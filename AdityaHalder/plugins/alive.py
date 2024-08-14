from .. import bot, cdx
from ..modules.utilities import (
    add_served_chat, add_served_user
)
from pyrogram import enums, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.on_message(cdx(["start", "help"]) & filters.private)
async def start_message_private(client, message):
    chat_id = message.chat.id
    await add_served_user(chat_id)
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
                    url=f"https://t.me/{bot.username}?startgroup=true",
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
    await client.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=buttons,
        disable_web_page_preview=True,
    )



@bot.on_message(filters.new_chat_members, group=2)
async def welcome_self(client, message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)
    try:
        for member in message.new_chat_members:
            if member.id == bot.id:
                chat_type = message.chat.type
                if (
                    chat_type != enums.ChatType.SUPERGROUP
                    or chat_type != enums.ChatType.CHANNEL
                ):
                    await message.reply_text("This chat is not supergroup !")
                    return await bot.leave_chat(message.chat.id)
                return await message.reply_text(
                    "**🥀 𝗪𝗼𝘄, 𝗧𝗵𝗮𝗻𝗸 𝗬𝗼𝘂 🌿 ...**"
                )
    except Exception:
        pass
