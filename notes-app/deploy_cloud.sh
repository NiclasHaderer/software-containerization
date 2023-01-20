#!/bin/bash

# Deploys the notes-app to a cloud kubernetes cluster hostet
# on Google Cloud Platform using helm.

# !! This will cost money, running the smallest cluster costs
# !! about 200$ per month.

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
# todo: delete the ingress controller before installing it again to avoid errors
helm install nginx-ingress ingress-nginx/ingress-nginx --set controller.service.loadBalancerIP=34.160.138.104

NAMESPACE="default"
CONTEXT="gke_containerisation_europe-west4-a_containerization-cluster-v2"

# 2) Apply the db.secret.yaml file to the cluster using kubectl

kubectl delete secret pg-user-password --namespace $NAMESPACE --context $CONTEXT
kubectl apply -f db.secret.yaml --namespace $NAMESPACE --context $CONTEXT

# 3) Install app using helm
helm uninstall my-notes --namespace $NAMESPACE --kube-context $CONTEXT --wait
echo "Waiting for helm to delete the notes-app ..."
sleep 10
helm install my-notes . --namespace $NAMESPACE  --kube-context $CONTEXT
