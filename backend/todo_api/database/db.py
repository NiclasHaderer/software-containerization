import asyncio

import psycopg2
from databases import Database

from todo_api.settings import SETTINGS

_db: Database | None = None


async def get_db(retry_nr=0, max_retries=10) -> Database:
    global _db
    if _db is None:
        try:
            _db = Database(SETTINGS.db_connection)
            await _db.connect()
        except psycopg2.OperationalError as e:
            if retry_nr <= max_retries:
                await asyncio.sleep(1000)
                return await get_db(retry_nr, max_retries)
            else:
                raise e

    return _db
