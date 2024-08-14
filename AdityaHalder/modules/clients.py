import os, sys

from .. import console
from pyrogram import Client
from pytgcalls import PyTgCalls
from motor.motor_asyncio import AsyncIOMotorClient


assistants = []
assistantids = []

async_client = AsyncIOMotorClient
mongobase = async_client(console.MONGO_DB_URL)
mongodb = mongobase.AdityaHalder


class App(Client):
    def __init__(self):
        self.one = Client(
            name="App_One",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=console.STRING1,
            no_updates=True,
        )
        self.two = Client(
            name="App_Two",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=console.STRING2,
            no_updates=True,
        )
        self.three = Client(
            name="App_Three",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=console.STRING3,
            no_updates=True,
        )
        self.four = Client(
            name="App_Four",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=console.STRING4,
            no_updates=True,
        )
        self.five = Client(
            name="App_Five",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=console.STRING5,
            no_updates=True,
        )
        
    async def start(self):
        console.LOGGER.info("🦋 𝙎𝙩𝙖𝙧𝙩𝙞𝙣𝙜 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝘾𝙡𝙞𝙚𝙣𝙩𝙨 ‼️")
        if console.STRING1:
            try:
                await self.one.start()
            except Exception as e:
                console.LOGGER.info(f"❎ 𝙁𝙖𝙞𝙡𝙚𝙙 𝙏𝙤 𝙎𝙩𝙖𝙧𝙩 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙊𝙣𝙚❗\n⚠️ 𝙍𝙚𝙖𝙨𝙤𝙣: {e}")
                sys.exit()
            assistants.append(1)
            try:
                await self.one.join_chat("BikashGadgetsTech")
                await self.one.join_chat("Bgt_chat")
            except:
                pass
            self.one.name = self.one.me.first_name + " " + (self.one.me.last_name or "")
            self.one.username = f"@{self.one.me.username}" if self.one.me.username else self.one.me.mention
            self.one.id = self.one.me.id
            if console.LOG_GROUP_ID != 0:
                try:
                    await self.one.send_message(
                        console.LOG_GROUP_ID,
                        "**✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙊𝙣𝙚 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 ‼️**"
                    )
                except:
                    pass
            console.LOGGER.info(f"✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙊𝙣𝙚 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 𝘼𝙨: {self.one.name}")
                
        if console.STRING2:
            try:
                await self.two.start()
            except Exception as e:
                console.LOGGER.info(f"❎ 𝙁𝙖𝙞𝙡𝙚𝙙 𝙏𝙤 𝙎𝙩𝙖𝙧𝙩 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙏𝙬𝙤❗\n⚠️ 𝙍𝙚𝙖𝙨𝙤𝙣: {e}")
                sys.exit()
            assistants.append(2)
            try:
                await self.two.join_chat("BikashGadgetsTech")
                await self.two.join_chat("Bgt_chat")
            except:
                pass
            self.two.name = self.two.me.first_name + " " + (self.two.me.last_name or "")
            self.two.username = f"@{self.two.me.username}" if self.two.me.username else self.two.me.mention
            self.two.id = self.two.me.id
            if console.LOG_GROUP_ID != 0:
                try:
                    await self.two.send_message(
                        console.LOG_GROUP_ID,
                        "**✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙏𝙬𝙤 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 ‼️**"
                    )
                except:
                    pass
            console.LOGGER.info(f"✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙏𝙬𝙤 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 𝘼𝙨: {self.two.name}")
                
        if console.STRING3:
            try:
                await self.three.start()
            except Exception as e:
                console.LOGGER.info(f"❎ 𝙁𝙖𝙞𝙡𝙚𝙙 𝙏𝙤 𝙎𝙩𝙖𝙧𝙩 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙏𝙝𝙧𝙚𝙚❗\n⚠️ 𝙍𝙚𝙖𝙨𝙤𝙣: {e}")
                sys.exit()
            assistants.append(3)
            try:
                await self.three.join_chat("BikashGadgetsTech")
                await self.three.join_chat("Bgt_chat")
            except:
                pass
            self.three.name = self.three.me.first_name + " " + (self.three.me.last_name or "")
            self.three.username = f"@{self.three.me.username}" if self.three.me.username else self.three.me.mention
            self.three.id = self.three.me.id
            if console.LOG_GROUP_ID != 0:
                try:
                    await self.three.send_message(
                        console.LOG_GROUP_ID,
                        "**✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙏𝙝𝙧𝙚𝙚 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 ‼️**"
                    )
                except:
                    pass
            console.LOGGER.info(f"✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙏𝙝𝙧𝙚𝙚 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 𝘼𝙨: {self.three.name}")
                
        if console.STRING4:
            try:
                await self.four.start()
            except Exception as e:
                console.LOGGER.info(f"❎ 𝙁𝙖𝙞𝙡𝙚𝙙 𝙏𝙤 𝙎𝙩𝙖𝙧𝙩 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙁𝙤𝙪𝙧❗\n⚠️ 𝙍𝙚𝙖𝙨𝙤𝙣: {e}")
                sys.exit()
            assistants.append(4)
            try:
                await self.four.join_chat("BikashGadgetsTech")
                await self.four.join_chat("Bgt_chat")
            except:
                pass
            self.four.name = self.four.me.first_name + " " + (self.four.me.last_name or "")
            self.four.username = f"@{self.four.me.username}" if self.four.me.username else self.four.me.mention
            self.four.id = self.four.me.id
            if console.LOG_GROUP_ID != 0:
                try:
                    await self.four.send_message(
                        console.LOG_GROUP_ID,
                        "**✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙁𝙤𝙪𝙧 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 ‼️**"
                    )
                except:
                    pass
            console.LOGGER.info(f"✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙁𝙤𝙪𝙧 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 𝘼𝙨: {self.four.name}")
                
        if console.STRING5:
            try:
                await self.five.start()
            except Exception as e:
                console.LOGGER.info(f"❎ 𝙁𝙖𝙞𝙡𝙚𝙙 𝙏𝙤 𝙎𝙩𝙖𝙧𝙩 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙁𝙞𝙫𝙚❗\n⚠️ 𝙍𝙚𝙖𝙨𝙤𝙣: {e}")
                sys.exit()
            assistants.append(5)
            try:
                await self.five.join_chat("BikashGadgetsTech")
                await self.five.join_chat("Bgt_chat")
            except:
                pass
            self.five.name = self.five.me.first_name + " " + (self.five.me.last_name or "")
            self.five.username = f"@{self.five.me.username}" if self.five.me.username else self.five.me.mention
            self.five.id = self.five.me.id
            if console.LOG_GROUP_ID != 0:
                try:
                    await self.five.send_message(
                        console.LOG_GROUP_ID,
                        "**✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙁𝙞𝙫𝙚 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 ‼️**"
                    )
                except:
                    pass
            console.LOGGER.info(f"✅ 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙁𝙞𝙫𝙚 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 𝘼𝙨: {self.five.name}")
                    

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Ro_Bot",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            bot_token=console.BOT_TOKEN,
        )
    async def start(self):
        try:
            await super().start()
        except Exception as e:
            console.LOGGER.info(f"❎ 𝙁𝙖𝙞𝙡𝙚𝙙 𝙏𝙤 𝙎𝙩𝙖𝙧𝙩 𝙍𝙤𝙗𝙤𝙩❗\n⚠️ 𝙍𝙚𝙖𝙨𝙤𝙣: {e}")
            sys.exit()
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = f"@{self.me.username}"
        self.id = self.me.id
        if console.LOG_GROUP_ID != 0:
            try:
                await self.send_message(
                    console.LOG_GROUP_ID,
                    "**✅ 𝙍𝙤𝙗𝙤𝙩 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 ‼️**"
                )
            except:
                pass
        console.LOGGER.info(f"✅ 𝙍𝙤𝙗𝙤𝙩 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 𝘼𝙨: {self.name}")


class Call(PyTgCalls):
    def __init__(self):
        self.assistant_one = Client(
            name="Assistant_One",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING1),
        )
        self.one = PyTgCalls(
            self.assistant_one,
            cache_duration=100,
        )
        self.assistant_two = Client(
            name="Assistant_Two",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING2),
        )
        self.two = PyTgCalls(
            self.assistant_two,
            cache_duration=100,
        )
        self.assistant_three = Client(
            name="Assistant_Three",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING3),
        )
        self.three = PyTgCalls(
            self.assistant_three,
            cache_duration=100,
        )
        self.assistant_four = Client(
            name="Assistant_Four",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING4),
        )
        self.four = PyTgCalls(
            self.assistant_four,
            cache_duration=100,
        )
        self.assistant_five = Client(
            name="Assistant_Five",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING5),
        )
        self.five = PyTgCalls(
            self.assistant_five,
            cache_duration=100,
        )

    async def start(self):
        console.LOGGER.info("♻️ 𝙎𝙩𝙖𝙧𝙩𝙞𝙣𝙜 𝙋𝙮𝙏𝙜𝘾𝙖𝙡𝙡𝙨 𝘾𝙡𝙞𝙚𝙣𝙩❗\n")
        if console.STRING1:
            await self.one.start()
        if console.STRING2:
            await self.two.start()
        if console.STRING3:
            await self.three.start()
        if console.STRING4:
            await self.four.start()
        if console.STRING5:
            await self.five.start()
        console.LOGGER.info("♻️ 𝙋𝙮𝙏𝙜𝘾𝙖𝙡𝙡𝙨 𝘾𝙡𝙞𝙚𝙣𝙩 𝙎𝙩𝙖𝙧𝙩𝙚𝙙❗\n")

        
async def start_all_clients():
    from AdityaHalder import app, bot, call
    for file in os.listdir():
        if file.endswith(".session"):
            os.remove(file)
    for file in os.listdir():
        if file.endswith(".session-journal"):
            os.remove(file)
    console.LOGGER.info("🥀 𝙋𝙧𝙤𝙘𝙚𝙨𝙨𝙞𝙣𝙜 𝘼𝙡𝙡 𝘾𝙡𝙞𝙚𝙣𝙩𝙨 ‼️")
    await bot.start()
    await app.start()
    await call.start()
    console.LOGGER.info("🥀 𝘼𝙡𝙡 𝘾𝙡𝙞𝙚𝙣𝙩𝙨 𝙉𝙤𝙬 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 ‼️")


