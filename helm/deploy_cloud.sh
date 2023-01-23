#!/bin/bash

# The kubectl context
CONTEXT="gke_containerisation_europe-west4-a_containerization-cluster-v2"

# Default values
first_time=false
namespace=default
upgrade=false
reinstall=false

TEMP=$(getopt -o '' --long first_time:,namespace:,upgrade,reinstall -n 'deploy_could.sh' -- "$@")
eval set -- "$TEMP"

while true; do
  case "$1" in
    --first_time)
      first_time=true
      shift 1;;
    --namespace)
      namespace="$2"
      shift 2;;
    --upgrade)
      upgrade=true
      shift;;
    --reinstall)
      reinstall=true
      shift;;
    -h|--help)
      echo "Usage: deploy_could.sh [--first_time] [--namespace=string] [--upgrade] [--reinstall]"
      exit 0;;
    --)
      shift
      break;;
    *)
      echo "Internal error!" >&2
      exit 1;;
  esac
done

if ! $upgrade && ! $reinstall; then
    echo "Either upgrade or reinstall must be specified." >&2
    exit 1
fi

if $upgrade && $reinstall; then
    echo "Only one of upgrade or reinstall can be specified." >&2
    exit 1
fi

if $first_time; then
    # 1) Install the ingress controller
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm install nginx-ingress ingress-nginx/ingress-nginx --set controller.service.loadBalancerIP=34.160.138.104
fi

if $upgrade; then
    # 2) Update the database secret
    kubectl delete secret pg-user-password --namespace "$namespace" --context $CONTEXT
    kubectl apply -f db.secret.yaml --namespace "$namespace" --context $CONTEXT

    # 3) Upgrade the app using helm
    helm upgrade my-notes . --namespace "$namespace" --kube-context $CONTEXT
fi

if $reinstall; then
    # 2) Update the database secret
    kubectl delete secret pg-user-password --namespace "$namespace" --context $CONTEXT
    kubectl apply -f db.secret.yaml --namespace "$namespace" --context $CONTEXT

    # 3) Reinstall the app using helm
    helm uninstall my-notes --namespace "$namespace" --kube-context $CONTEXT --wait
    echo "Waiting for helm to delete the notes-app ..."
    sleep 10
    helm install my-notes . --namespace "$namespace"  --kube-context $CONTEXT
fi
