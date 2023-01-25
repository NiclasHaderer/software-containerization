#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# The kubectl context
CONTEXT="gke_containerisation_europe-west4-a_containerization-cluster-v2"

# Default values
namespace="default"
upgrade=false
reinstall=false
install=false
delete=false

# Create a function called usage() that prints the usage message
usage() {
  echo "Usage: deploy_could.sh [--namespace=string] [--upgrade] [--reinstall] [--delete] [--install]"
}

TEMP=$(getopt -o '' --long namespace:,upgrade,reinstall,delete,install -n 'deploy_could.sh' -- "$@")
eval set -- "$TEMP"
while true; do
  case "$1" in
    --namespace)
      namespace="$2"
      shift 2;;
    --upgrade)
      upgrade=true
      shift;;
    --reinstall)
      reinstall=true
      shift;;
    --delete)
      delete=true
      shift;;
    --install)
      install=true
      shift;;
    -h|--help)
      usage
      exit 0;;
    --)
      shift
      break;;
    *)
      echo "Internal error!" >&2
      usage
      exit 1;;
  esac
done

if ! $upgrade && ! $reinstall && ! $install && ! $delete; then
    echo "Either install, upgrade, reinstall or delete must be specified." >&2
    usage
    exit 1
fi

if [[ "true" == $upgrade && "true" == $reinstall ]]; then
    echo "Only one of upgrade or reinstall can be specified." >&2
    usage
    exit 1
fi

if $upgrade; then
    # 3) Upgrade the app using helm
    helm upgrade my-notes . --namespace "$namespace" --kube-context $CONTEXT --set deployment.type=gce
fi

if $reinstall; then
    # 3) Reinstall the app using helm
    helm uninstall my-notes --namespace "$namespace" --kube-context $CONTEXT --wait
    helm install my-notes . --namespace "$namespace"  --kube-context $CONTEXT --set deployment.type=gce
fi

if $install; then
    # If namespace does not exist, create it
    if ! kubectl get namespace "$namespace" --context $CONTEXT; then
      echo "Namespace $namespace does not exist. Creating..."
      kubectl create namespace "$namespace" --context $CONTEXT
    fi
    # 3) Install the app using helm
    helm install my-notes . --namespace "$namespace"  --kube-context $CONTEXT --set deployment.type=gce
fi

if $delete; then
    # 2) Delete the app using helm
    helm uninstall my-notes --namespace "$namespace" --kube-context $CONTEXT --wait
fi
