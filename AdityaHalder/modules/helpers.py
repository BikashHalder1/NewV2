from .. import console
from pyrogram import filters
from typing import Callable, Union, List, Pattern


def cdx(commands: Union[str, List[str]]):
    return filters.command(commands, ["/", "!", "."])

def cdz(commands: Union[str, List[str]]):
    return filters.command(commands, ["", "/", "!", "."])

def rgx(pattern: Union[str, Pattern]):
    return filters.regex(pattern)

def check_errors(func: Callable) -> Callable:
    async def decorator(client, message):
        try:
            return await func(client, message)
        except Exception as e:
            await message.reply_text(
                f"**{type(e).__name__}:** `{e}`"
            )

    return decorator


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time



async def stream_logger(client, message, thumbnail, type):
    if console.LOG_GROUP_ID:
        if message.chat.id != console.LOG_GROUP_ID:
            try:
                chat = message.chat
                chat_name = chat.title
                chat_id = chat.id
                try:
                    if chat.username:
                        chat_link = f"@{chat.username}"
                    else:
                        try:
                            chat_link = chat.invite_link
                            if chat_link is None:
                                chat_link = await client.export_chat_invite_link(chat_id)
                        except Exception:
                            chat_link = await client.export_chat_invite_link(chat_id)
                        except:
                            chat_link = "Private Chat"
                        chat_link = f"[Check Now]({chat_link})"
                except:
                    chat_link = "Private Chat"
    
                user = message.from_user
                firstname = user.mention
                username = f"@{user.username}" if user.username else user.mention
                user_id = user.id
                if len(message.command) < 2:
                    stream_query = "From Telegram ..."
                else:
                    stream_query = message.text.split(None, 1)[1]
                if type == "Audio":
                    stream_type = "Audio Streaming"
                elif type == "Video":
                    stream_type = "Video Streaming"
                else:
                    stream_type = "Unknown Streaming"
                caption = f"""
**━━━━━━━━━━━━━━━━━━━**
**💥 𝗖𝗵𝗮𝘁 𝗧𝗶𝘁𝗹𝗲:** {chat_name}
**🌐 𝗖𝗵𝗮𝘁 𝗟𝗶𝗻𝗸:** {chat_link}
**💯 𝗖𝗵𝗮𝘁 𝗜𝗗:** `{chat_id}`
**━━━━━━━━━━━━━━━━━━━**
**🤖 𝗨𝘀𝗲𝗿 𝗡𝗮𝗺𝗲:** {firstname}
**👾 𝗨𝘀𝗲𝗿 𝗟𝗶𝗻𝗸:** {username}
**🐬 𝗨𝘀𝗲𝗿 𝗜𝗗:** {user_id}
**━━━━━━━━━━━━━━━━━━━**
**🦋 𝗤𝘂𝗲𝗿𝘆:** {stream_query}
**🎸 𝗧𝘆𝗽𝗲:** {stream_type}
**━━━━━━━━━━━━━━━━━━━**"""
                return await client.send_photo(
                    chat_id=console.LOG_GROUP_ID,
                    photo=thumbnail, caption=caption,
                )
            except Exception as e:
                console.logs.info(f"𝗦𝘁𝗿𝗲𝗮𝗺 𝗟𝗼𝗴𝘀 𝗘𝗿𝗿𝗼𝗿:\n{e}")
                pass


