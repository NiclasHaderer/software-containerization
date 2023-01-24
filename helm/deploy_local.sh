#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

NAMESPACE="default"
CONTEXT="minikube"

# check if my-notes is already installed
if helm list --namespace $NAMESPACE | grep my-notes; then
  echo "my-notes is already installed. Uninstalling..."
  helm uninstall my-notes --namespace $NAMESPACE --wait --kube-context $CONTEXT
fi

# check if the namespace exists
if ! kubectl get namespace $NAMESPACE --context $CONTEXT; then
  echo "Namespace $NAMESPACE does not exist. Creating..."
  kubectl create namespace $NAMESPACE --context $CONTEXT
fi

helm install my-notes . --namespace $NAMESPACE --kube-context $CONTEXT