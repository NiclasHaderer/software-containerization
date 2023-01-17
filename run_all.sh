docker image rm containerization-frontend
docker build frontend -t containerization-frontend

docker image rm gcr.io/containerisation/containerization-backend:latest
docker build backend -t gcr.io/containerisation/containerization-backend:latest
docker push gcr.io/containerisation/containerization-backend:latest

docker compose up

# See project in gcloud console: https://console.cloud.google.com/gcr/images/containerisation