from pathlib import Path

import aiofiles
from colorama import Fore
from gql import gql

from graphql import DocumentNode

BASE_DIR = Path(__file__).resolve().parent.parent


async def load_query(path: Path) -> DocumentNode:
    async with aiofiles.open(path) as f:
        return gql(await f.read())


class Message:
    @staticmethod
    def error(message: str):
        print(f"{Fore.RED} " + message)

    @staticmethod
    def info(message: str):
        print(f"{Fore.CYAN} " + message)

    @staticmethod
    def ok(message: str):
        print(f"{Fore.GREEN} " + message)
