from datetime import datetime
from sqlite3 import Date, Row
from typing import Optional, TypedDict

from dependency_injector.wiring import Provide, inject

from database.database import Database
from di import Container
from helpers import Message


class CreateSongInput(TypedDict):
    esound_song_id: int
    song_title: str
    created_at: Date


@inject
class Song:
    def __init__(self, database: Database = Provide[Container.database]):
        self._database = database

    async def create(self, input: CreateSongInput) -> None:
        try:
            await self._database.connection.execute(
                "INSERT INTO song (esound_song_id,song_title,created_at) VALUES(?,?,?);", (input["esound_song_id"], input["song_title"], input["created_at"]))
            await self._database.connection.commit()

        except Exception as e:
            Message.error(f"Database: Could not create new entry {input}")
            pass

    async def if_song_exists_by_id(self, song_id: int):
        row = await self._database.connection.execute('SELECT EXISTS(SELECT 1 FROM song WHERE esound_song_id=?);', (song_id,))

        row = await row.fetchone()

        if row is not None:
            if row[0] > 0:
                return True

        return False

    async def if_song_exists_by_title(self, song_title: str):
        row = await self._database.connection.execute('SELECT EXISTS(SELECT 1 FROM song WHERE song_title=?);', (song_title,))

        row = await row.fetchone()

        if row is not None:
            if row[0] > 0:
                return True

        return False

    async def get_last_item(self) -> Optional[Row]:
        request = await self._database.connection.execute("SELECT * FROM song ORDER BY id DESC LIMIT 1;")
        row = await request.fetchone()

        return row
