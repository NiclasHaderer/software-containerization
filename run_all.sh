docker image rm containerization-frontend
docker build frontend -t containerization-frontend

docker image rm containerization-backend
docker build backend -t containerization-backend

docker compose up