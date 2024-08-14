import random
from .. import app
from .clients import mongodb
from typing import Dict, List, Union


assistantdb = mongodb.assistants
sudoersdb = mongodb.sudoers
chatsdb = mongodb.tgchats
usersdb = mongodb.tgusers

    
assistantdict = {}


async def get_client(assistant: int):
    if int(assistant) == 1:
        return app.one
    elif int(assistant) == 2:
        return app.two
    elif int(assistant) == 3:
        return app.three
    elif int(assistant) == 4:
        return app.four
    elif int(assistant) == 5:
        return app.five


async def set_assistant(chat_id):
    from .clients import assistants

    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant
    await assistantdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    app = await get_client(ran_assistant)
    return app


async def get_assistant(chat_id: int) -> str:
    from .clients import assistants

    assistant = assistantdict.get(chat_id)
    if not assistant:
        dbassistant = await assistantdb.find_one({"chat_id": chat_id})
        if not dbassistant:
            app = await set_assistant(chat_id)
            return app
        else:
            got_assis = dbassistant["assistant"]
            if got_assis in assistants:
                assistantdict[chat_id] = got_assis
                app = await get_client(got_assis)
                return app
            else:
                app = await set_assistant(chat_id)
                return app
    else:
        if assistant in assistants:
            app = await get_client(assistant)
            return app
        else:
            app = await set_assistant(chat_id)
            return app


async def set_calls_assistant(chat_id):
    from .clients import assistants

    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant
    await assistantdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    return ran_assistant


async def group_assistant(self, chat_id: int) -> int:
    from .clients import assistants

    assistant = assistantdict.get(chat_id)
    if not assistant:
        dbassistant = await assistantdb.find_one({"chat_id": chat_id})
        if not dbassistant:
            assis = await set_calls_assistant(chat_id)
        else:
            assis = dbassistant["assistant"]
            if assis in assistants:
                assistantdict[chat_id] = assis
                assis = assis
            else:
                assis = await set_calls_assistant(chat_id)
    else:
        if assistant in assistants:
            assis = assistant
        else:
            assis = await set_calls_assistant(chat_id)
    if int(assis) == 1:
        return self.one
    elif int(assis) == 2:
        return self.two
    elif int(assis) == 3:
        return self.three
    elif int(assis) == 4:
        return self.four
    elif int(assis) == 5:
        return self.five


# Get a list of sudo users
async def get_sudoers() -> list:
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    if not sudoers:
        return []
    return sudoers["sudoers"]


# Add an user in sudolist
async def add_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.append(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True


# Remove an user from sudolist
async def del_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.remove(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True


# Served Chats

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list




# served users

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

