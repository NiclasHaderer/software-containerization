import re
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from settings import SETTINGS
from views.helpers import decode_user_dict, generate_token, get_user_from_db, crate_user

DEFAULT_USER = {
    "username": "default",
    "password": "1234"
}


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:

        if SETTINGS.spoof_user and not AuthenticationMiddleware._is_whitelisted_url(request):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                token = generate_token(DEFAULT_USER["username"], DEFAULT_USER["password"])
                request.headers._list.append((b"authorization", bytes(token, encoding="UTF_8")))

                auth_header = request.headers.get("Authorization")

        if not AuthenticationMiddleware._is_whitelisted_url(request):
            is_authorized, error = AuthenticationMiddleware._validate_header(request)

            if not is_authorized:
                return error

        return await call_next(request)

    @staticmethod
    def _validate_header(request: Request) -> (bool, Optional[Response]):
        auth = request.headers.get("Authorization")
        if not auth:
            return False, AuthenticationMiddleware._auth_error("No auth header was found")

        try:
            auth_header = decode_user_dict(request)
        except Exception:
            return False, AuthenticationMiddleware._auth_error("Could not decode auth header")

        if "username" not in auth_header or "password" not in auth_header:
            return False, AuthenticationMiddleware._auth_error("`username` or `password` field not in header")

        user = get_user_from_db(auth_header["username"])

        if not user:
            if SETTINGS.spoof_user:
                user = crate_user(DEFAULT_USER["username"], DEFAULT_USER["password"])
            else:
                return False, AuthenticationMiddleware._auth_error("User token has no associated user")

        if not user.password_valid(auth_header["password"]):
            return False, AuthenticationMiddleware._auth_error("Token password invalid")

        return True, None

    @staticmethod
    def _auth_error(body) -> Response:
        response = {"detail": body}
        return JSONResponse(response, status_code=403)

    @staticmethod
    def _is_whitelisted_url(request: Request) -> bool:
        return bool(re.fullmatch("/login/?", request.url.path)) or \
               bool(re.fullmatch("/docs/?", request.url.path)) or \
               bool(re.fullmatch("/redoc/?", request.url.path)) or \
               bool(re.fullmatch("/create-account/?", request.url.path))
