from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from todo_api.database.migrate import run_migrations
from todo_api.settings import SETTINGS
from todo_api.views import router


async def run_migrations_if_single_node():
    if SETTINGS.single_node:
        await run_migrations()


middleware = []
if not SETTINGS.production:
    middleware.append(Middleware(
        CORSMiddleware,
        allow_origin_regex="(https?:\/\/)?(localhost|127\.0\.0\.1)(:[0-9]{2,5})?",
        allow_headers=["*"],
        allow_credentials=True,
        allow_methods=["*"],
    ))

app = FastAPI(middleware=middleware, on_startup=[run_migrations_if_single_node])

app.include_router(router)
