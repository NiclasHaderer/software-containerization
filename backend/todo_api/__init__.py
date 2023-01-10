from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from todo_api.middleware import AuthenticationMiddleware
from views import views

middleware = [
    Middleware(CORSMiddleware,
               allow_origin_regex='(https?:\/\/)?(localhost|127\.0\.0\.1)(:[0-9]{2,5})?',
               allow_headers=["*"],
               allow_credentials=True,
               allow_methods=["*"]
               ),
    Middleware(AuthenticationMiddleware)
]

app = FastAPI(middleware=middleware)

app.include_router(views.router)
