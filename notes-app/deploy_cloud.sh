#!/bin/bash

# Deploys the notes-app to a cloud kubernetes cluster hostet
# on Google Cloud Platform using helm.

# !! This will cost money, running the smallest cluster costs
# !! about 100$ per month.

# !! before running this script, make sure the glcoud cli is
# !! authenticated and the correct project is selected

# !! make sure kubectl is installed and configured to connect
# !! to the correct cluster

# !! also, make sure the docker images are built and pushed to
# !! the container registry.

# read therefore: https://www.notion.so/Google-Cloud-d1b0e69eb7434504b45256123ab51854

# 1) Install NGINX Ingress Controller on GKE according to:
# https://medium.com/@glen.yu/nginx-ingress-or-gke-ingress-d87dd9db504c

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx


NAMESPACE="default"

# 2) Apply the secrets.yaml file to the cluster using kubectl

kubectl delete secret pg-user-password --namespace $NAMESPACE
kubectl apply -f secrets.yaml --namespace $NAMESPACE

# 3) Install app using helm
helm delete my-notes --namespace $NAMESPACE
echo "Waiting for helm to delete the notes-app ..."
sleep 10
helm install my-notes . --namespace $NAMESPACE
