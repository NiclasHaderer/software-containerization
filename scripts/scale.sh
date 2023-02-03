#!/bin/bash

exec_cmd(){
  #  Print in green
  echo ""
  printf "\e[32m$1\e[0m"
  echo ""
  eval "$1"
}

printf "Scaling the notes-app-frontend deployment to 5 replicas"
exec_cmd "kubectl get deployments"
sleep 1
exec_cmd "kubectl scale deployment notes-app-frontend --replicas=5"
sleep 1
exec_cmd "kubectl get deployments"
sleep 3

printf "Scale the notes-app-backend deployment to 5 replicas"
sleep 1
exec_cmd "kubectl get deployments"
sleep 1
exec_cmd "kubectl scale deployment notes-app-backend --replicas=5"
sleep 1
exec_cmd "kubectl get deployments"

printf "Scaling down the deployments to 3"

exec_cmd "kubectl scale deployment notes-app-frontend --replicas=3"
exec_cmd "kubectl scale deployment notes-app-backend --replicas=3"