from typing import TypedDict

from dependency_injector.wiring import Provide, inject

from di import Container
from helpers import BASE_DIR, Message, load_query
from models.esound_library import EsoundLibraryModel
from models.ytmusic_song import YoutubeLikedSongModel
from services.graphql import GraphQLRequest


class SavedSongPayload(TypedDict):
    esound_song_id: int
    song_title: str


@inject
class EsoundApi:
    def __init__(self, graphql: GraphQLRequest = Provide[Container.graphql_request]) -> None:
        self._client = graphql
        pass

    async def save_to_library(self, song_id: int) -> None:
        query = await load_query(BASE_DIR / "src" / "graphql" / "save_to_library.gql")

        variables = {
            "songId": song_id
        }

        await self._client.request(query, variables, is_library_endpoint=True)

    async def save_song(self, song: YoutubeLikedSongModel) -> SavedSongPayload | None:
        query = await load_query(BASE_DIR / "src" / "graphql" / "save_song.gql")

        variables = {
            "authorId": song["artists"][0]["id"] or "0",
            "authorImageUrl": "",
            "authorName":  song["artists"][0]["name"] or "Unknown Artist",
            "originalAuthorName":  song["artists"][0]["name"] or "Unknown Artist",
            "songTitle":  song["title"],
            "originalSongTitle": song["title"],
            "originalTitle": song["title"],
            "songImageUrl": song["thumbnails"][0]["url"],
            "sourceId": song["videoId"],
            "thirdPartyTrackId": None,
            "type": "YOUTUBE",
            "ytMusic": 1
        }

        try:
            response = await self._client.request(query, variables)
            if response:
                return {
                    "esound_song_id": response["SaveSong"]["songId"],
                    "song_title": song["title"]
                }
            else:
                Message.info("Too many requests, sleeping for 10 seconds..")
        except Exception as e:
            Message.error(f"Could not save song: {e}")

    async def get_esound_library(self) -> EsoundLibraryModel | None:
        query = await load_query(BASE_DIR / "src" / "graphql" / "get_library.gql")

        request = await self._client.request(query, is_library_endpoint=True)

        if (request):
            response = EsoundLibraryModel(**request)

            return response
