from asyncio import sleep
from typing import Optional

from aiohttp import ClientResponseError
from dependency_injector.wiring import Provide, inject
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from auth import Auth
from graphql import DocumentNode


@inject
class GraphQLRequest:
    def __init__(self, auth: Auth = Provide["auth"]) -> None:
        headers = {
            "Authorization": f"Bearer {auth.access_token}"
        }

        library_transport = AIOHTTPTransport(
            url='https://api.esound.app/library', headers=headers)
        song_transport = AIOHTTPTransport(
            url='https://api.esound.app/song', headers=headers)

        self._library_client = Client(transport=library_transport,
                                      fetch_schema_from_transport=True)
        self._song_client = Client(transport=song_transport,
                                   fetch_schema_from_transport=True)

    async def request(self, gql: DocumentNode, variables: Optional[dict] = None, is_library_endpoint: Optional[bool] = False):
        _client: Optional[Client] = None

        _client = self._song_client

        if is_library_endpoint:
            _client = self._library_client

        async with _client as client:
            try:
                response = await client.execute(gql, variables)

                return response
            except ClientResponseError as e:
                if e.code == 429:
                    await sleep(10_000)
