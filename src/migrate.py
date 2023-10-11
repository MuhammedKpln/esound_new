from datetime import date

from dependency_injector.wiring import Provide, inject

from database.database import Song, db
from di import Container
from helpers import Message
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
        pass

    def save_local_copy(self, song_id: int, song_title: str) -> None:
        Song.create(esound_song_id=song_id, song_title=song_title,
                    created_at=date.today())

    def _if_already_in_library(self, song_id: int) -> bool:
        return Song.select().where(Song.esound_song_id == song_id).exists()

    async def run(self):
        ytMusicSongs = self._ytMusicApi.fetch_liked_songs()

        if not ytMusicSongs:
            Message.info(
                "Could not fetch liked song, did you liked any songs?")
            exit(0)

        for song in ytMusicSongs:
            esound_song = await self._esound_api.save_song(song)

            if not esound_song:
                break

            is_already_in_library = self._if_already_in_library(
                esound_song["esound_song_id"])

            if (is_already_in_library):
                Message.info("Already in library, contiuning...")
                continue

            await self._esound_api.save_to_library(esound_song["esound_song_id"])
            self.save_local_copy(
                esound_song["esound_song_id"], esound_song["song_title"])

            Message.ok(f"Saved {song['title']}")
