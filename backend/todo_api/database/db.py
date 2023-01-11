from databases import Database

from todo_api.settings import SETTINGS

_db: Database | None = None


async def get_db() -> Database:
    global _db
    if _db is None:
        _db = Database(SETTINGS.db_connection)
        await _db.connect()
    return _db
