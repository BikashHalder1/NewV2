import sys
from .. import console


async def collect_all_variables():
    console.LOGGER.info("♾️ 𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝘼𝙡𝙡 𝙑𝙖𝙧𝙞𝙖𝙗𝙡𝙚𝙨 ...")
    if console.API_ID == 0:
        console.LOGGER.info("'𝘼𝙋𝙄_𝙄𝘿' - 𝙉𝙤𝙩 𝙁𝙤𝙪𝙣𝙙 !!")
        sys.exit()
        
    if not console.API_HASH:
        console.LOGGER.info("'𝘼𝙋𝙄_𝙃𝘼𝙎𝙃' - 𝙉𝙤𝙩 𝙁𝙤𝙪𝙣𝙙 !!")
        sys.exit()
        
    if not console.BOT_TOKEN:
        console.LOGGER.info("'𝘽𝙊𝙏_𝙏𝙊𝙆𝙀𝙉' - 𝙉𝙤𝙩 𝙁𝙤𝙪𝙣𝙙 !!")
        sys.exit()
        
    if (
        not console.STRING1
        and not console.STRING2
        and not console.STRING3
        and not console.STRING4
        and not console.STRING5
    ):
        console.LOGGER.info("'𝙎𝙏𝙍𝙄𝙉𝙂_𝙊𝙉𝙀' - 𝙉𝙤𝙩 𝙁𝙤𝙪𝙣𝙙 !!")
        sys.exit()
        
    if not console.MONGO_DB_URL:
        console.LOGGER.info("'𝙈𝙊𝙉𝙂𝙊_𝘿𝘽_𝙐𝙍𝙇' - 𝙉𝙤𝙩 𝙁𝙤𝙪𝙣𝙙 !!")
        sys.exit()

    if console.OWNER_ID == 0:
        console.LOGGER.info("'𝙊𝙒𝙉𝙀𝙍_𝙄𝘿' - 𝙉𝙤𝙩 𝙁𝙤𝙪𝙣𝙙 !!")
        sys.exit()

    if console.LOG_GROUP_ID == 0:
        console.LOGGER.info("'𝙇𝙊𝙂_𝙂𝙍𝙊𝙐𝙋_𝙄𝘿' - 𝙉𝙤𝙩 𝙁𝙤𝙪𝙣𝙙 !!")
        
    console.LOGGER.info("✅ 𝘼𝙡𝙡 𝙑𝙖𝙧𝙞𝙖𝙗𝙡𝙚𝙨 𝘼𝙧𝙚 𝘾𝙤𝙡𝙡𝙚𝙘𝙩𝙚𝙙 ‼️")
    
    
