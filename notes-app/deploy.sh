#!/usr/bin/env zsh

NAMESPACE="default"

helm delete my-notes --namespace $NAMESPACE
sleep 3
minikube kubectl -- delete secret pg-user-password --namespace $NAMESPACE
minikube kubectl -- create secret generic pg-user-password --from-literal=user-password="super_secret" --namespace $NAMESPACE
helm install my-notes . --namespace $NAMESPACE
