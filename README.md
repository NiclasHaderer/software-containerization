# Software containerization

## Backend

Basic todo app with authentication which is not alt all secure and encodes the username and the password to a token ;)

## Frontend

Angular App which uses the backend to show some todo items

## Getting started
### Running
+ First run the backend (see backend [readme](backend/README.md))
+ Afterwards run the frontend (see frontend [readme](frontend/README.md))
+ Visit `http://127.0.0.1:4200` for the frontend
+ Visit `http://127.0.0.1:8000/docs` || `http://127.0.0.1:8000/redoc` for the openapi docs.

### Auth
+ If you want to enable a default user which allows you to user the api without auth, set `spoof_user` to true in the [settings.py](backend/todo_api/settings.py). This will still allow you to user other users, but you also have a default user for not authenticated requests.
+ To login a user make a request to the `http://127.0.0.1:8000/login` endpoint and get the user.  
    Returns: `{ username: string;  token: string;  id: number; }`
+ The received token has to be attached to the request as Authorization header `req.headers.set('Authorization', user.token)`. See [auth.interceptor](frontedn/../frontend/src/app/auth/auth.interceptor.ts) for an example.
