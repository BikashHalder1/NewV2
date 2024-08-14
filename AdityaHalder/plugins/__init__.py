import glob, importlib

from .. import logs, plugs
from os.path import basename, dirname, isfile


def __list_all_plugins():
    plugin_paths = glob.glob(dirname(__file__) + "/*.py")
    
    all_plugins = [
        basename(f)[:-3]
        for f in plugin_paths
        if isfile(f) and f.endswith(".py")
        and not f.endswith("__init__.py")
    ]

    return all_plugins


ALL_PLUGINS = sorted(__list_all_plugins())
__all__ = ALL_PLUGINS + ["ALL_PLUGINS"]


async def import_all_plugins():
    logs.info("➡️ 𝙄𝙢𝙥𝙤𝙧𝙩𝙞𝙣𝙜 𝘼𝙡𝙡 𝙋𝙡𝙪𝙜𝙞𝙣𝙨 !!...")
    for all_plugin in ALL_PLUGINS:
        try:
            imported_plugin = importlib.import_module(
                "AdityaHalder.plugins." + all_plugin
            )
            logs.info(f"✅ 𝙄𝙢𝙥𝙤𝙧𝙩𝙚𝙙: {all_plugin}")
            if (hasattr
                (
                    imported_plugin, "__NAME__"
                ) and imported_plugin.__NAME__
            ):
                imported_plugin.__NAME__ = imported_plugin.__NAME__
                if (
                    hasattr(
                        imported_plugin, "__MENU__"
                    ) and imported_plugin.__MENU__
                ):
                    plugs[imported_plugin.__NAME__.lower()
                    ] = imported_plugin
        except Exception as e:
            logs.info(f"❎ 𝙁𝙖𝙞𝙡𝙚𝙙: {all_plugin}\n↪️ 𝙍𝙚𝙖𝙨𝙤𝙣: {e}")
            continue
    logs.info("✅ 𝘼𝙡𝙡 𝙋𝙡𝙪𝙜𝙞𝙣𝙨 𝘼𝙧𝙚 𝙄𝙢𝙥𝙤𝙧𝙩𝙚𝙙 ‼️")
    
