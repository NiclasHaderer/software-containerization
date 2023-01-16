#!/usr/bin/env zsh

NAMESPACE="default"

minikube kubectl -- delete secret pg-user-password --namespace $NAMESPACE
minikube kubectl -- create secret generic pg-user-password --from-literal=user-password="mysecretpassword" --namespace $NAMESPACE
helm install my-notes . --namespace $NAMESPACE
sleep 10
minikube kubectl -- port-forward my-notes-postgresql-0 5432:5432
# Run the following command to check if we can access the container
# psql -h 127.0.0.1 -p 5432 -d notes -U u_notes -W
