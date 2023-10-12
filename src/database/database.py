from typing import Optional

import aiosqlite

from filemanager import path_exists, read_file
from helpers import BASE_DIR, Message

db: Optional[aiosqlite.Connection] = None
DIR = BASE_DIR / "src" / "database" / "base.sql"


class Database:
    async def _import_base_table(self, db: aiosqlite.Connection):
        database_file = await read_file(DIR)

        try:
            Message.info("Importing base database..")
            await db.executescript(database_file)
            Message.ok("Database imported successfully..")
        except:
            Message.error("Could not import the database!")
            exit()

    async def init(self):
        is_first_start = False
        database_dir = BASE_DIR / "data.db"

        if not await path_exists(database_dir):
            is_first_start = True

        self.connection = await aiosqlite.connect(database_dir)

        if (is_first_start):
            await self._import_base_table(self.connection)
