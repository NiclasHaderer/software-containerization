#!/bin/bash

# Deploys the notes-app to a local kubernetes cluster using
# minikube and helm.

NAMESPACE="default"

helm delete my-notes --namespace $NAMESPACE
sleep 3
minikube kubectl -- delete secret pg-user-password --namespace $NAMESPACE
minikube kubectl -- apply -f db.secret.yaml --namespace $NAMESPACE
helm install my-notes . --namespace $NAMESPACE
