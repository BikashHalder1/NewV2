import aiohttp, aiofiles, asyncio, os, random, re, textwrap

from .. import (
    adb, app, bot, call,
    cdx, cdz, check_errors, console
)
from ..modules.helpers import stream_logger
from ..modules.utilities import add_served_chat, get_assistant, group_assistant
from ntgcalls import TelegramServerError
from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import filters as fl
from pytgcalls.exceptions import NoActiveGroupCall, NotInCallError
from pytgcalls.types import (
    Call, AudioQuality, VideoQuality, MediaStream,
    GroupCallConfig, StreamAudioEnded, ChatUpdate, Update
)
from typing import Dict, List, Union
from youtubesearchpython.__future__ import VideosSearch


call_config = GroupCallConfig(auto_start=False)
channeldb = adb.channeldb
queue = {}


def admins_command_only(function):
    async def wrapper(client, message):
        try:
            await message.delete()
        except:
            pass
        user_id = message.from_user.id if message.from_user else None
        if user_id:
            if console.OWNER_ID != 0:
                if user_id == console.OWNER_ID:
                    return await function(client, message)
        
            member = await bot.get_chat_member(
                message.chat.id, user_id
            )
            if (
                member.status == ChatMemberStatus.ADMINISTRATOR
                or member.status == ChatMemberStatus.OWNER
            ):
                return await function(client, message)
        
        return await message.reply_text(
            "**🤖 𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻𝘀 𝗮𝗻𝗱 𝗢𝘄𝗻𝗲𝗿\n𝗖𝗮𝗻 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱❗**"
        )
        
    return wrapper


async def get_youtube_info(query):
    if "https://" in query:
        base = r"(?:https?:)?(?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube(?:\-nocookie)?\.(?:[A-Za-z]{2,4}|[A-Za-z]{2,3}\.[A-Za-z]{2})\/)?(?:shorts\/|live\/)?(?:watch|embed\/|vi?\/)*(?:\?[\w=&]*vi?=)?([^#&\?\/]{11}).*$"
        resu = re.findall(base, query)
        vidid = resu[0] if resu[0] else None
    else:
        vidid = None
    url = (
        f"https://www.youtube.com/watch?v={vidid}"
        if vidid else None
    )
    search = url if url else query
    results = VideosSearch(search, limit=1)
    for result in (await results.next())["result"]:
        try:
            title = result["title"]
        except:
            title = "Unsupported Title"
        vidids = vidid if vidid else result["id"]
        vidurl = url if url else result["link"]
        try:
            duration = result.get("duration")
            if not duration:
                duration = "Live"
            elif len(duration) == 7:
                duration = f"0{duration}"
            elif len(duration) == 4:
                duration = f"0{duration}"
        except:
            duration = "Unknown Mins"
        try:
            views = result["viewCount"]["short"]
        except:
            views = "Unknown Views"
        try:
            channel = result["channel"]["name"]
        except:
            channel = "Unknown Channel"
            
    youtube_dictionary = {
        "title": title, "id": vidids,
        "link": vidurl, "duration": duration,
        "views": views, "channel": channel,
    }
    return youtube_dictionary


async def get_call_status(chat_id):
    aditya = await group_assistant(call, chat_id)
    calls = await aditya.calls
    chat_call = calls.get(chat_id)
    if chat_call:
        status = chat_call.status
        if status == Call.Status.IDLE:
            call_status = "IDLE"
        elif status == Call.Status.PLAYING:
            call_status = "PLAYING"
            
        elif status == Call.Status.PAUSED:
            call_status = "PAUSED"
    else:
        call_status = "NOTHING"

    return call_status
    

async def get_media_stream(file, type):
    if type == "Audio":
        stream = MediaStream(
            media_path=file,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
        )

    elif type == "Video":
        stream = MediaStream(
            media_path=file,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.HD_720p,
        )

    return stream



async def download_thumbnail(vidid: str):
    async with aiohttp.ClientSession() as session:
        links = [
            f"https://i.ytimg.com/vi/{vidid}/maxresdefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/sddefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/hqdefault.jpg",
            f"https://te.legra.ph/file/c6e1041c6c9a12913f57a.png",
        ]
        thumbnail = f"cache/temp_{vidid}.png"
        for url in links:
            async with session.get(url) as resp:
                if resp.status != 200:
                    continue
                else:
                    f = await aiofiles.open(thumbnail, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
                    return thumbnail


async def get_user_logo(user_id):
    try:
        user_chat = await bot.get_chat(user_id)
        userimage = user_chat.photo.big_file_id
        user_logo = await bot.download_media(
            userimage, f"cache/{user_id}.png"
        )
    except:
        user_chat = await bot.get_me()
        userimage = user_chat.photo.big_file_id
        user_logo = await bot.download_media(
            userimage, f"cache/{bot.id}.png"
        )
    return user_logo
    

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def circle_image(image, size):
    size = (size, size)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(
        image, mask.size, centering=(0.5, 0.5)
    )
    output.putalpha(mask)
    return output


def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


async def gen_thumb(results, user_id):
    if not results:
        return f"https://graph.org/file/d4bc06ada79821eb01025.jpg"
    title_a = results.get("title")
    title_b = re.sub("\W+", " ", title_a)
    title = title_b.title()
    vidid = results.get("id")
    duration = results.get("duration")
    views = results.get("views")
    channel = results.get("channel")
    image = await download_thumbnail(vidid)
    logo = await get_user_logo(user_id)
    try:
        image01 = Image.open(image)
        image02 = Image.open(logo)
        image03 = Image.open("AdityaHalder/resource/thumbnail.png")
        image04 = changeImageSize(1280, 720, image01)
        image05 = ImageEnhance.Brightness(image04)
        image06 = image05.enhance(1.3)
        image07 = ImageEnhance.Contrast(image06)
        image08 = image07.enhance(1.3)
        image09 = circle_image(image08, 365)
        image10 = circle_image(image02, 90)
        image11 = image08.filter(ImageFilter.GaussianBlur(15))
        image12 = ImageEnhance.Brightness(image11)
        image13 = image12.enhance(0.5)
        image13.paste(image09, (140, 180), mask=image09)
        image13.paste(image10, (410, 450), mask=image10)
        image13.paste(image03, (0, 0), mask=image03)
        
        font01 = ImageFont.truetype("AdityaHalder/resource/font_01.ttf", 45)
        font02 = ImageFont.truetype("AdityaHalder/resource/font_02.ttf", 30)
        draw = ImageDraw.Draw(image13)
        para = textwrap.wrap(title, width=28)
        para_size = len(para)
        if para_size == 1:
            title_height = 230
        else:
            title_height = 180
        j = 0
        for line in para:
            if j == 1:
                j += 1
                draw.text(
                    (565, 230), f"{line}",
                    fill="white", font=font01
                )
            if j == 0:
                j += 1
                draw.text(
                    (565, title_height), f"{line}",
                    fill="white", font=font01
                )
        draw.text(
            (565, 320),
            f"{channel}  |  {views[:23]}",
            (255, 255, 255), font=font02
        )
        
        line_length = 580  
        line_color = random_color_generator()
     
        if duration != "Live":
            color_line_percentage = random.uniform(0.15, 0.85)
            color_line_length = int(line_length * color_line_percentage)
            white_line_length = line_length - color_line_length
            start_point_color = (565, 380)
            end_point_color = (565 + color_line_length, 380)
            draw.line([start_point_color, end_point_color], fill=line_color, width=9)
            start_point_white = (565 + color_line_length, 380)
            end_point_white = (565 + line_length, 380)
            draw.line([start_point_white, end_point_white], fill="white", width=8)
            circle_radius = 10 
            circle_position = (end_point_color[0], end_point_color[1])
            draw.ellipse([circle_position[0] - circle_radius, circle_position[1] - circle_radius,
                      circle_position[0] + circle_radius, circle_position[1] + circle_radius], fill=line_color)
        else:
            line_color = (255, 0, 0)
            start_point_color = (565, 380)
            end_point_color = (565 + line_length, 380)
            draw.line([start_point_color, end_point_color], fill=line_color, width=9)
        
            circle_radius = 10 
            circle_position = (end_point_color[0], end_point_color[1])
            draw.ellipse([circle_position[0] - circle_radius, circle_position[1] - circle_radius,
                          circle_position[0] + circle_radius, circle_position[1] + circle_radius], fill=line_color)

        draw.text(
            (565, 400), "00:00",
            (255, 255, 255), font=font02
        )
        if len(duration) == 4:
            draw.text(
                (1090, 400), duration,
                (255, 255, 255), font=font02
            )
        elif len(duration) == 5:
            draw.text(
                (1055, 400), duration,
                (255, 255, 255), font=font02
            )
        elif len(duration) == 8:
            draw.text(
                (1015, 400), duration,
                (255, 255, 255), font=font02
            )
        
        image14 = ImageOps.expand(
            image13, border=10, fill=random_color_generator()
        )
        image15 = changeImageSize(1280, 720, image14)
        image15.save(f"cache/{vidid}_{user_id}.png")
        return f"cache/{vidid}_{user_id}.png"
    except Exception as e:
        return f"https://graph.org/file/d4bc06ada79821eb01025.jpg"


   

async def add_to_queue(
    chat_id, results, stream_type,
    stream, thumbnail, from_user,
    forceplay: Union[bool, str] = None
):
    put = {
        "chat_id": chat_id,
        "results": results,
        "stream_type": stream_type,
        "stream": stream,
        "thumbnail": thumbnail,
        "from_user": from_user,
    }
    check = queue.get(chat_id)
    if forceplay:
        if check:
            check.insert(0, put)
        else:
            queue[chat_id] = []
            queue[chat_id].append(put)
    else:
        if check:
            queue[chat_id].append(put)
        else:
            queue[chat_id] = []
            queue[chat_id].append(put)

    return len(queue[chat_id]) - 1


async def is_queue_not_empty(chat_id):
    my_queue = queue.get(chat_id)
    if (
        not my_queue
        or len(my_queue) == 0
    ):
        return False
    else:
        return my_queue


async def task_done(chat_id):
    check = await is_queue_not_empty(chat_id)
    if check:
        check.pop(0)


async def close_stream(chat_id):
    active_call = queue.get(chat_id)
    if active_call:
        try:
            queue.pop(chat_id)
        except:
            pass
    aditya = await group_assistant(call, chat_id)
    try:
        await aditya.leave_call(chat_id)
    except:
        pass


async def get_channel_id() -> int:
    check = await channeldb.find_one(
        {"chat_id": {"$lt": 0}}
    )
    if not check:
        return 0
    get_chat = check["chat_id"]
    return get_chat


async def set_channel_id(chat_id: int) -> bool:
    chatid = await get_channel_id()
    if chatid == chat_id:
        return False
    await channeldb.update_one(
        {"chat_id": chatid},
        {"$set": {"chat_id": chat_id}},
        upsert=True,
    )
    return True


@bot.on_message(cdx(["cset"]) & filters.me)
@check_errors
async def set_db_channel_id(client, message):
    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        try:
            chat_id = message.text.split(None, 1)[1]
            if "@" in chat_id:
                chat_id = chat_id.replace("@", "")
                chat = await bot.get_chat(chat_id)
                chat_id = chat.id
        except Exception as e:
            await message.reply_text(f"**🚫 Error:** `{e}`")
    if len(str(chat_id)) != 14:
        return await message.reply_text("**➡️ Give Me Correct Chat ID❗**")
    try:
        add_chat_id = await set_channel_id(
            int(chat_id)
        )
        if add_chat_id:
            return await message.reply_text("**✅ Chat ID Added As Channel ID.**")
        return await message.reply_text("**✅ Already Active As Channel ID❗")
    except Exception as e:
        await message.reply_text(f"**🚫 Error:** `{e}`")
        

@bot.on_message(
    cdz([
        "play", "vplay", "cplay", "cvplay", "fplay", "fvplay", "fcplay", "fcvplay"
    ]) & ~filters.private
)
@check_errors
async def stream_audio_or_video(client, message):
    try:
        await message.delete()
    except:
        pass
    stickers = [
        "🥀", "🌹", "🌺", "🎉", "🎃", "💥", "🦋", "🕊️",
        "❤️", "💖", "💝", "💗", "💓", "💘", "💞", "💋",
    ]
    aux = await message.reply_text(random.choice(stickers))
    if (
           str(message.command[0][0]) == "c"
           or str(message.command[0][1]) == "c"
    ):
        if chat_id != 0:
            chat_id = await get_channel_id()
        else:
            chat_id = message.chat.id
    else:
        chat_id = message.chat.id
    await add_served_chat(chat_id)
    from_user = message.from_user if message.from_user else bot.me
    user_id = from_user.id
    mention = from_user.mention
    aditya = await group_assistant(call, chat_id)
    call_status = await get_call_status(chat_id)
    replied = message.reply_to_message
    audio = (replied.audio or replied.voice) if replied else None
    video = (replied.video or replied.document) if replied else None
    try:
        if audio:
            results = None
            title = None
            file = await replied.download()
            vidid = f"{chat_id}_{message.id}"
            duration = None
            type = "Audio"
        elif video:
            results = None
            title = None
            file = await replied.download()
            vidid = f"{chat_id}_{message.id}"
            duration = None
            type = "Video"
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 𝗚𝗶𝘃𝗲 𝗠𝗲 𝗦𝗼𝗺𝗲 𝗤𝘂𝗲𝗿𝘆 𝗧𝗼\n𝗣𝗹𝗮𝘆 𝗠𝘂𝘀𝗶𝗰 𝗢𝗿 𝗩𝗶𝗱𝗲𝗼❗...**"
                )
            query = message.text.split(None, 1)[1]
            results = await get_youtube_info(query)
            vidid = results.get("id")
            file = results.get("link")
            title = results.get("title")[:18]
            title = f"[{title}]({file})"
            duration = results.get("duration")
            if duration == "Live":
                duration = duration + " Stream"
            else:
                duration = duration + " Mins"
            type = "Audio" if (
                str(message.command[0][0]) != "v"
                and str(message.command[0][1]) != "v"
                and str(message.command[0][2]) != "v"
            ) else "Video"
        stream = await get_media_stream(file, type)
        keyboards = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🗑️ 𝗖𝗹𝗼𝘀𝗲",
                        callback_data="force_close"
                    )
                ]
            ]
        )
        try:
            if (
                call_status == "IDLE"
                or call_status == "NOTHING"
            ):
                await aditya.play(chat_id, stream, config=call_config)
                await aditya.unmute_stream(chat_id)
                thumbnail = await gen_thumb(results, user_id)
                await add_to_queue(chat_id, results, type, stream, thumbnail, from_user)
                caption = f"""**❀≽ 𝗦𝘁𝗮𝗿𝘁𝗲𝗱 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗡𝗼𝘄 ♚**

**✭ 𝗧𝗶𝘁𝗹𝗲:** {title}
**✭ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻:** {duration}
**✭ 𝗦𝘁𝗿𝗲𝗮𝗺 𝗧𝘆𝗽𝗲:** {type}
**ツ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗕𝘆:** {mention}"""
                await client.send_photo(
                    chat_id, photo=thumbnail,
                    caption=caption,
                    reply_markup=keyboards,
                )
                try:
                    await aux.delete()
                except:
                    pass
                await stream_logger(client, message, thumbnail, type)
            elif (
                call_status == "PLAYING"
                or call_status == "PAUSED"
            ):
                if str(message.command[0][0]) == "f":
                    await aditya.play(chat_id, stream, config=call_config)
                    await aditya.unmute_stream(chat_id)
                    thumbnail = await gen_thumb(results, user_id)
                    await add_to_queue(chat_id, results, type, stream, thumbnail, from_user)
                    caption = f"""**❀≽ 𝗦𝘁𝗮𝗿𝘁𝗲𝗱 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗡𝗼𝘄 ♚**

**✭ 𝗧𝗶𝘁𝗹𝗲:** {title}
**✭ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻:** {duration}
**✭ 𝗦𝘁𝗿𝗲𝗮𝗺 𝗧𝘆𝗽𝗲:** {type}
**ツ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗕𝘆:** {mention}"""
                    await client.send_photo(
                        chat_id, photo=thumbnail,
                        caption=caption,
                        reply_markup=keyboards,
                    )
                    try:
                        await aux.delete()
                    except:
                        pass
                    await stream_logger(client, message, thumbnail, type)
                else:
                    thumbnail = await gen_thumb(results, user_id)
                    position = await add_to_queue(
                        chat_id, results, type, stream, thumbnail, from_user
                    )
                    caption = f"""**❀≽ 𝗔𝗱𝗱𝗲𝗱 𝗧𝗼 𝗤𝘂𝗲𝘂𝗲 ✭ 𝗔𝘁 #{position}**

**✭ 𝗧𝗶𝘁𝗹𝗲:** {title}
**✭ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻:** {duration}
**✭ 𝗦𝘁𝗿𝗲𝗮𝗺 𝗧𝘆𝗽𝗲:** {type}
**ツ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗕𝘆:** {mention}"""
                    await client.send_photo(
                        chat_id, photo=thumbnail,
                        caption=caption,
                        reply_markup=keyboards,
                    )
                    try:
                        await aux.delete()
                    except:
                        pass
                    await stream_logger(client, message, thumbnail, type)
        except NoActiveGroupCall:
            adi = await get_assistant(chat_id)
            try:
                try:
                    assistant = await bot.get_chat_member(chat_id, adi.me.id)
                except ChatAdminRequired:
                    return await aux.edit("**🤖 𝘼𝙩 𝙁𝙞𝙧𝙨𝙩, 𝙋𝙧𝙤𝙢𝙤𝙩𝙚 𝙈𝙚 𝙖𝙨 𝙖𝙣 𝘼𝙙𝙢𝙞𝙣❗**")
                if (
                    assistant.status == ChatMemberStatus.BANNED
                    or assistant.status == ChatMemberStatus.RESTRICTED
                ):
                    return await aux.edit(
                        f"**🤖 𝘼𝙩 𝙁𝙞𝙧𝙨𝙩, 𝙐𝙣𝙗𝙖𝙣 [𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙄𝘿](https://t.me/{adi.username}) 𝙏𝙤 𝙎𝙩𝙖𝙧𝙩 𝙎𝙩𝙧𝙚𝙖𝙢❗**"
                    )
            except UserNotParticipant:
                if message.chat.username:
                    invitelink = message.chat.username
                    try:
                        await app.resolve_peer(invitelink)
                    except:
                        pass
                else:
                    try:
                        invitelink = await bot.export_chat_invite_link(chat_id)
                    except ChatAdminRequired:
                        return await aux.edit(
                            "**🤖 𝙃𝙚𝙮, 𝙄 𝙉𝙚𝙚𝙙 𝙄𝙣𝙫𝙞𝙩𝙚 𝙐𝙨𝙚𝙧 𝙋𝙚𝙧𝙢𝙞𝙨𝙨𝙞𝙤𝙣 𝙏𝙤 𝘼𝙙𝙙 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙄𝘿❗**"
                        )
                    except Exception as e:
                        return await aux.edit(f"**🚫 𝙀𝙧𝙧𝙤𝙧:** `{e}`")
                try:
                    await asyncio.sleep(1)
                    await adi.join_chat(invitelink)
                except InviteRequestSent:
                    try:
                        await bot.approve_chat_join_request(chat_id, adi.me.id)
                    except Exception as e:
                        return await aux.edit(f"**🚫 𝙀𝙧𝙧𝙤𝙧:** `{e}`")
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await aux.edit(f"**🚫 𝙀𝙧𝙧𝙤𝙧:** `{e}`")
            try:
                await aditya.play(chat_id, stream, config=call_config)
                await aditya.unmute_stream(chat_id)
                thumbnail = await gen_thumb(results, user_id)
                await add_to_queue(chat_id, results, type, stream, thumbnail, from_user)
                caption = f"""**❀≽ 𝗦𝘁𝗮𝗿𝘁𝗲𝗱 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗡𝗼𝘄 ♚**

**✭ 𝗧𝗶𝘁𝗹𝗲:** {title}
**✭ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻:** {duration}
**✭ 𝗦𝘁𝗿𝗲𝗮𝗺 𝗧𝘆𝗽𝗲:** {type}
**ツ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗕𝘆:** {mention}"""
                await client.send_photo(
                    chat_id, photo=thumbnail,
                    caption=caption,
                    reply_markup=keyboards,
                )
                try:
                    await aux.delete()
                except:
                    pass
                await stream_logger(client, message, thumbnail, type)
            except NoActiveGroupCall:
                return await aux.edit("**🤖 𝙃𝙚𝙮, 𝘼𝙩 𝙁𝙞𝙧𝙨𝙩 𝙎𝙩𝙖𝙧𝙩 𝙑𝘾 𝙏𝙤 𝙎𝙩𝙧𝙚𝙖𝙢❗**")
        except TelegramServerError:
            return aux.edit(f"**❎ 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙄𝙨𝙨𝙪𝙚, 🚫 𝙍𝙚𝙖𝙨𝙤𝙣:** `{e}`")
    except Exception as e:
        await aux.edit(f"**🚫 𝙎𝙩𝙧𝙚𝙖𝙢 𝙀𝙧𝙧𝙤𝙧:** `{e}`")


@bot.on_message(cdx(["pause", "cpause"]) & ~filters.private)
@admins_command_only
@check_errors
async def pause_and_mute(client, message):
    if str(message.command[0][0]) == "c":
        chat_id = await get_channel_id()
    else:
        chat_id = message.chat.id
    aditya = await group_assistant(call, chat_id)
    call_status = await get_call_status(chat_id)
    try:
        try:
            if call_status == "IDLE":
                is_mute = await aditya.mute_stream(chat_id)
                if is_mute:
                    await message.reply_text("**🔇 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗠𝘂𝘁𝗲𝗱 ‼️**")
                else:
                    await message.reply_text("**🔇 𝗔𝗹𝗿𝗲𝗮𝗱𝘆 𝗠𝘂𝘁𝗲𝗱 ‼️**")
            elif call_status == "PLAYING":
                await aditya.pause_stream(chat_id)
                await aditya.mute_stream(chat_id)
                await message.reply_text("**▶️ 𝗦𝘁𝗿𝗲𝗮𝗺 𝗣𝗮𝘂𝘀𝗲𝗱 ‼️**")
            elif call_status == "PAUSED":
                await message.reply_text("**▶️ 𝗔𝗹𝗿𝗲𝗮𝗱𝘆 𝗣𝗮𝘂𝘀𝗲𝗱❗**")
            elif call_status == "NOTHING":
                await message.reply_text("**🌺 𝗡𝗼𝘁𝗵𝗶𝗻𝗴 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴❗**")
            else:
                await message.reply_text("**✅ 𝗔𝗹𝗿𝗲𝗮𝗱𝘆 𝗶𝗻 𝗩𝗰 ‼️**")
        except NoActiveGroupCall:
            await message.reply_text("**❎ 𝗡𝗼 𝗔𝗰𝘁𝗶𝘃𝗲 𝗩𝗰 ‼️**")
    except Exception as e:
        await message.reply_text(f"**🚫 𝗣𝗮𝘂𝘀𝗲 𝗘𝗿𝗿𝗼𝗿:** `{e}`")


@bot.on_message(cdx(["resume", "cresume"]) & ~filters.private)
@admins_command_only
@check_errors
async def resume_and_unmute(client, message):
    if str(message.command[0][0]) == "c":
        chat_id = await get_channel_id()
    else:
        chat_id = message.chat.id
    aditya = await group_assistant(call, chat_id)
    call_status = await get_call_status(chat_id)
    try:
        try:
            if call_status == "IDLE":
                is_unmute = await aditya.unmute_stream(chat_id)
                if is_unmute:
                    await message.reply_text("**🔊 Successfully Unmuted ‼️**")
                else:
                    await message.reply_text("**🔊 Already Unmuted ‼️**")
            elif call_status == "PAUSED":
                await aditya.unmute_stream(chat_id)
                await aditya.resume_stream(chat_id)
                await message.reply_text("**✅ 𝗦𝘁𝗿𝗲𝗮𝗺 𝗥𝗲𝘀𝘂𝗺𝗲𝗱 ‼️**")
            elif call_status == "PLAYING":
                await message.reply_text("**⏸️ 𝗔𝗹𝗿𝗲𝗮𝗱𝘆 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 ‼️**")
            elif call_status == "NOTHING":
                await message.reply_text("**🌺 𝗡𝗼𝘁𝗵𝗶𝗻𝗴 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 ‼️**")
            else:
                await message.reply_text("**✅ 𝗔𝗹𝗿𝗲𝗮𝗱𝘆 𝗶𝗻 𝗩𝗰 ‼️**")
        except NoActiveGroupCall:
            await message.reply_text("**❎ 𝗡𝗼 𝗔𝗰𝘁𝗶𝘃𝗲 𝗩𝗰 ‼️**")
    except Exception as e:
        await message.reply_text(f"**🚫 𝗥𝗲𝘀𝘂𝗺𝗲 𝗘𝗿𝗿𝗼𝗿:** `{e}`")


@bot.on_message(cdx(["skip", "cskip"]) & ~filters.private)
@admins_command_only
@check_errors
async def skip_current_song(client, message):
    if str(message.command[0][0]) == "c":
        chat_id = await get_channel_id()
    else:
        chat_id = message.chat.id
    aditya = await group_assistant(call, chat_id)
    aux = await message.reply_text("**🌺 𝗦𝗸𝗶𝗽𝗽𝗲𝗱 🌷...**")
    try:
        status = await get_call_status(chat_id)
        if (
            status == "NOTHING" or status == "IDLE"
        ):
            await close_stream(chat_id)
            return await aux.edit("**🌺 𝗡𝗼𝘁𝗵𝗶𝗻𝗴 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴❗**")
        elif (
            status == "PLAYING" or status == "PAUSED"
        ):
            await task_done(chat_id)
            if not await is_queue_not_empty(chat_id):
                await close_stream(chat_id)
                return await aux.edit(
                    "**🥀 𝗡𝗼 𝗦𝗼𝗻𝗴 𝗜𝗻 𝗤𝘂𝗲𝘂𝗲 𝗟𝗶𝘀𝘁\n𝗦𝗼, 𝗟𝗲𝗮𝘃𝗶𝗻𝗴 𝗩𝗖❗**"
                )
        my_queue = queue.get(chat_id)
        results = my_queue[0]["results"]
        file = results.get("link")
        title = results.get("title")[:18]
        title = f"[{title}]({file})"
        duration = results.get("duration")
        if duration == "Live":
            duration = duration + " Stream"
        else:
            duration = duration + " Mins"
        type = my_queue[0]["stream_type"]
        from_user = my_queue[0]["from_user"]
        user_id = from_user.id
        mention = from_user.mention
        thumbnail = my_queue[0]["thumbnail"]
        # stream = await get_media_stream(file, type)
        stream = my_queue[0]["stream"]
        keyboards = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🗑️ 𝗖𝗹𝗼𝘀𝗲",
                        callback_data="force_close"
                    )
                ]
            ]
        )
        await aditya.play(chat_id, stream, config=call_config)
        caption = f"""**❀≽ 𝗦𝘁𝗮𝗿𝘁𝗲𝗱 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗡𝗼𝘄 ♚**

**✭ 𝗧𝗶𝘁𝗹𝗲:** {title}
**✭ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻:** {duration}
**✭ 𝗦𝘁𝗿𝗲𝗮𝗺 𝗧𝘆𝗽𝗲:** {type}
**ツ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗕𝘆:** {mention}"""
        await client.send_photo(
            chat_id, photo=thumbnail,
            caption=caption,
            reply_markup=keyboards,
        )
        try:
            return await aux.delete()
        except:
            pass
    except Exception as e:
        await aux.edit(f"🚫 𝗦𝗸𝗶𝗽 𝗘𝗿𝗿𝗼𝗿: `{e}`")
            

@bot.on_message(cdx(["end", "stop", "cend", "cstop"]) & ~filters.private)
@admins_command_only
@check_errors
async def stop_or_end_stream(client, message):
    if str(message.command[0][0]) == "c":
        chat_id = await get_channel_id()
    else:
        chat_id = message.chat.id
    aditya = await group_assistant(call, chat_id)
    try:
        status = await get_call_status(chat_id)
        if status == "NOTHING":
            await close_stream(chat_id)
            return await message.reply_text("**🌺 𝗡𝗼𝘁𝗵𝗶𝗻𝗴 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴❗**")
        elif (
            status == "IDLE"
            or status == "PLAYING"
            or status == "PAUSED"
        ):
            await close_stream(chat_id)
            return await message.reply_text("**❎ 𝗦𝘁𝗼𝗽𝗽𝗲𝗱 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴❗**")
    except Exception as e:
        await message.reply_text(f"**🚫 𝗘𝗻𝗱 𝗘𝗿𝗿𝗼𝗿:** `{e}`")



@call.one.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
@call.two.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
@call.three.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
@call.four.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
@call.five.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
@call.one.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
@call.two.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
@call.three.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
@call.four.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
@call.five.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
@call.one.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
@call.two.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
@call.three.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
@call.four.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
@call.five.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
async def stream_services_handler(_, update: Update):
    return await close_stream(update.chat_id)
    
    
@call.one.on_update(fl.stream_end)
@call.two.on_update(fl.stream_end)
@call.three.on_update(fl.stream_end)
@call.four.on_update(fl.stream_end)
@call.five.on_update(fl.stream_end)
async def stream_end_handler(_, update: Update):
    chat_id = update.chat_id
    await task_done(chat_id)
    if not await is_queue_not_empty(chat_id):
        return await close_stream(chat_id)
    
    aditya = await group_assistant(call, chat_id)
    my_queue = queue.get(chat_id)
    results = my_queue[0]["results"]
    file = results.get("link")
    title = results.get("title")[:18]
    title = f"[{title}]({file})"
    duration = results.get("duration")
    if duration == "Live":
        duration = duration + " Stream"
    else:
        duration = duration + " Mins"
    type = my_queue[0]["stream_type"]
    from_user = my_queue[0]["from_user"]
    user_id = from_user.id
    mention = from_user.mention
    thumbnail = my_queue[0]["thumbnail"]
    # stream = await get_media_stream(file, type)
    stream = my_queue[0]["stream"]
    keyboards = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🗑️ 𝗖𝗹𝗼𝘀𝗲",
                    callback_data="force_close"
                )
            ]
        ]
    )
    await aditya.play(chat_id, stream, config=call_config)
    caption = f"""**❀≽ 𝗦𝘁𝗮𝗿𝘁𝗲𝗱 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗡𝗼𝘄 ♚**

**✭ 𝗧𝗶𝘁𝗹𝗲:** {title}
**✭ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻:** {duration}
**✭ 𝗦𝘁𝗿𝗲𝗮𝗺 𝗧𝘆𝗽𝗲:** {type}
**ツ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗕𝘆:** {mention}"""
    await bot.send_photo(
        chat_id, photo=thumbnail,
        caption=caption,
        reply_markup=keyboards,
    )
