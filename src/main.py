import argparse
import asyncio
from sys import exit

import colorama
from dependency_injector.wiring import Provide, inject
from ytmusicapi import setup_oauth

from auth import Auth
from config import CONFIG_FILE, Config, ConfigSections
from database.database import Database
from database.models.song import Song
from di import Container
from filemanager import path_exists
from helpers import BASE_DIR, Message
from migrate import Migrate
from services.esound import EsoundApi
from services.graphql import GraphQLRequest

colorama.init(autoreset=True)

parser = argparse.ArgumentParser(
    prog='YTEsound',
    description='Migrate from Youtube Music to Esound')


parser.add_argument('-o', '--oauth', action="store_true",
                    help='Login with OAuth.')
args = parser.parse_args()


async def is_first_start() -> bool:
    if await path_exists(CONFIG_FILE):
        return False
    return True


async def check_youtube_auth():
    if not await path_exists(BASE_DIR / "oauth.json") and not await path_exists(BASE_DIR / "headers.json"):
        print(BASE_DIR)
        Message.error(
            "Neither oauth.json or headers.json could be found. Please run python src/main.py -o.")
        exit(0)


@inject
async def initialize(auth: Auth = Provide[Container.auth], config: Config = Provide[Container.config], database: Database = Provide[Container.database]):
    await config.initialize()
    await database.init()
    await auth.initialize(email=config.config[ConfigSections.Esound.name]["email"], password=config.config[ConfigSections.Esound.name]["password"])
    await check_youtube_auth()


async def main():
    if await is_first_start():
        await Config().initialize()
        setup_oauth('oauth.json')
        Message.ok(
            f"{colorama.Fore.CYAN} Please fill in settings.yml and re-run the script.")
        exit(0)

    await initialize()
    migrate = Migrate()

    await migrate.run()


@inject
async def dispose(database: Database = Provide[Container.database]):
    await database.connection.close()

if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__, GraphQLRequest, EsoundApi, Song])

    if args.oauth:
        setup_oauth('oauth.json')
        exit()

    asyncio.run(main())
