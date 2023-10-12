import asyncio
import concurrent.futures as cf
import threading
from datetime import date
from threading import Thread
from typing import List, Optional

from dependency_injector.wiring import Provide, inject

from database.models.song import CreateSongInput, Song
from di import Container
from helpers import Message, divide_chunks, split_list_by_title
from models.ytmusic_song import YoutubeLikedSongModel
from services.esound import EsoundApi
from services.graphql import GraphQLRequest
from services.ytmusicapi import YoutubeMusicApi


@inject
class Migrate:
    def __init__(self, gql: GraphQLRequest = Provide[Container.graphql_request]) -> None:
        self._esound_api = EsoundApi()
        self._ytMusicApi = YoutubeMusicApi()
        self._library = None
        self._song_db = Song()
        self._database_last_item_title = None
        pass

    async def save_local_copy(self, song_id: int, song_title: str) -> None:
        var = CreateSongInput(
            created_at=date.today(), esound_song_id=song_id, song_title=song_title)

        await self._song_db.create(var)

    async def _if_already_in_library(self, song_id: Optional[int] = None, song_title: Optional[str] = None) -> bool:
        if song_id:
            return await self._song_db.if_song_exists_by_id(song_id=song_id)

        if song_title:
            return await self._song_db.if_song_exists_by_title(song_title=song_title)

        return False

    async def _fetch_last_item(self) -> None:
        last_item = await self._song_db.get_last_item()

        if last_item:
            self._database_last_item_title = last_item[2]

    def filter_list(self, x: YoutubeLikedSongModel):
        if x["title"] != self._database_last_item_title:
            return True
        return False

    async def dispose(self):
        await self._song_db._database.connection.close()
        for task in asyncio.tasks.all_tasks():
            task.cancel()

    async def run(self):
        ytMusicSongs = self._ytMusicApi.fetch_liked_songs()

        if not ytMusicSongs:
            Message.info(
                "Could not fetch liked song, did you liked any songs?")
            exit(0)

        await self._fetch_last_item()

        if self._database_last_item_title:
            Message.info("Filtering list to restore where you leaved.")
            ytMusicSongs = split_list_by_title(
                ytMusicSongs, self._database_last_item_title)
            ytMusicSongs.pop(0)
            Message.ok("Filtering succeedeed.")

        if (len(ytMusicSongs) < 1):
            Message.ok("No new music found, aborting..")
            await self.dispose()
            exit(0)

        chunkedSongList: List[List[YoutubeLikedSongModel]] = list(
            divide_chunks(ytMusicSongs, 20))

        for key, i in enumerate(chunkedSongList):
            await self._run(i)

            if key == len(chunkedSongList) - 1:
                if not await self._if_already_in_library(song_title=i[len(i)-1]["title"]):
                    Message.ok(
                        "Sleeping for 10 seconds to not hitting Too Max Requests.")
                    await asyncio.sleep(10)

        Message.info("Finished migration, bye...")
        await self.dispose()
        exit()

    async def _run(self, list: List[YoutubeLikedSongModel]):
        for song in list:
            esound_song = await self._esound_api.save_song(song)

            if not esound_song:
                break

            is_already_in_library = await self._if_already_in_library(song_id=esound_song["esound_song_id"])

            if (is_already_in_library):
                Message.info(
                    f"'{song['title']}' is already in library, contiuning...")
                continue

            await self._esound_api.save_to_library(esound_song["esound_song_id"])
            await self.save_local_copy(
                esound_song["esound_song_id"], esound_song["song_title"])

            Message.ok(f"Saved {song['title']}")
