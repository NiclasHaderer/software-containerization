docker image rm gcr.io/containerisation/containerization-frontend
docker build frontend -t gcr.io/containerisation/containerization-frontend:latest
docker push gcr.io/containerisation/containerization-frontend:latest

docker image rm gcr.io/containerisation/containerization-backend:latest
docker build backend -t gcr.io/containerisation/containerization-backend:latest
docker push gcr.io/containerisation/containerization-backend:latest


# See project in gcloud console: https://console.cloud.google.com/gcr/images/containerisation