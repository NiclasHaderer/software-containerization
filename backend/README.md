# Backend

This is the backend of the software containerization project. It is a REST API that allows to create, start, stop and 
delete posts and persist them in a database. It is implemented in Python using the fastapi framework.

## Setup
The backend can be either run locally or in a docker container. The docker container is the recommended way to run the backend.

### Without Docker

1) Install poetry (see https://python-poetry.org/docs/)
2) Use poetry to install dependencies (using `poetry install`)
3) Start the database `start_db.sh`
4) Run the backend  `poetry run python3 cmd/run.py`
5) Visit `http://127.0.0.1:8000/docs` || `http://127.0.0.1:8000/redoc` for the openapi docs.

### With Docker
Build the image with `docker build -t backend .` and run it with `docker run -p 8000:8000 backend`.