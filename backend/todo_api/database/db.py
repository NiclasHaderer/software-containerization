import asyncio

import psycopg2
from databases import Database

from todo_api.settings import SETTINGS

_db: Database | None = None


async def get_db(retry_nr=0, max_retries=10) -> Database:
    global _db
    if _db is None:
        try:
            db = Database(SETTINGS.db_connection)
            await db.connect()
            _db = db
        except (AssertionError, psycopg2.OperationalError) as e:
            print(e)
            if retry_nr <= max_retries:
                await asyncio.sleep(1)
                return await get_db(retry_nr + 1, max_retries)
            else:
                raise e

    return _db


if __name__ == "__main__":
    asyncio.run(get_db())
