#!/bin/bash

# Recommended: notes-auditor, notes-admin, notes-cluster-admin

CURRENT_CONTEXT=$(kubectl config current-context)
CLUSTER_CONTEXT=$CURRENT_CONTEXT

if [ $# -eq 0 ]; then
  echo "Pass username as argument"
  exit 1
fi

# get username from arg
user_name=$1
echo "Creating user $user_name"
# check if folder exists and if no create it
if [ ! -d "certs" ]; then
  mkdir certs
fi
# shellcheck disable=SC2164
cd certs
openssl genrsa -out "$user_name.key" 2048
openssl req -new -key "$user_name".key -out "$user_name".csr -subj "/CN=$user_name/O=acg"
ENCODED=$(cat "$user_name".csr | base64 | tr -d "\n")

cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: $user_name-csr
spec:
  request: $ENCODED
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
EOF

kubectl certificate approve "$user_name"-csr

# Get the Certificate
kubectl get csr "$user_name"-csr -o jsonpath='{.status.certificate}' \
  | base64 --decode > "$user_name".crt

#openssl x509 -req -in "$user_name.csr" -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out "$user_name.crt" -days 500
kubectl config set-credentials "$user_name" --client-certificate="$user_name.crt" --client-key="$user_name.key" --embed-certs=true
kubectl config set-context "$user_name-context" --cluster=$CLUSTER_CONTEXT --namespace=default --user="$user_name"
# shellcheck disable=SC2103
cd ..

# https://medium.com/@mattgillard/creating-a-kubernetes-rbac-user-in-google-kubernetes-engine-gke-fa930217a052