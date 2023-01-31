#!/bin/bash

# Recommended: notes-auditor, notes-admin, notes-cluster-admin

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
openssl req -new -key "$user_name".key -out "$user_name".csr -subj "/CN=$user_name"
openssl x509 -req -in "$user_name.csr" -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out "$user_name.crt" -days 500
kubectl config set-credentials "$user_name" --client-certificate="$user_name.crt" --client-key="$user_name.key"
kubectl config set-context "$user_name-context" --cluster=minikube --user="$user_name"
# shellcheck disable=SC2103
cd ..