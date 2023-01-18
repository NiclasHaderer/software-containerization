#!/bin/bash

NAMESPACE="default"

helm delete my-notes --namespace $NAMESPACE
sleep 3
minikube kubectl -- delete secret pg-user-password --namespace $NAMESPACE
minikube kubectl -- apply -f secrets.yaml --namespace $NAMESPACE
helm install my-notes . --namespace $NAMESPACE
