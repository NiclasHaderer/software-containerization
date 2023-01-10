import os
from pathlib import Path

from settings import SETTINGS
from tinydb import TinyDB

path = Path(os.path.realpath(SETTINGS.db_folder))
full_path = f"{path.absolute()}/database.json"

if not os.path.isdir(path.absolute()):
    print(f"Could not find db folder {path}")
    print(f"Creating database folder at {path}")
    py_path = Path(path)
    py_path.mkdir(exist_ok=True, parents=True)

if not os.path.isfile(full_path):
    open(full_path, 'a').close()

db = TinyDB(full_path)

USER_TABLE = db.table("user", cache_size=0)
TODO_TABLE = db.table("todo", cache_size=0)
