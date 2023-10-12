from pathlib import Path
from typing import Generator, List

import aiofiles
from colorama import Fore
from gql import gql

from graphql import DocumentNode
from models.ytmusic_song import YoutubeLikedSongModel

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


def divide_chunks(l: list, n: int) -> Generator:
    for i in range(0, len(l), n):
        yield l[i:i + n]


def split_list_by_title(l: List[YoutubeLikedSongModel], song_title: str) -> List[YoutubeLikedSongModel]:
    new_list = []

    for key, i in enumerate(l):
        if i["title"] == song_title:
            new_list = l[key:]
            break

    return new_list
