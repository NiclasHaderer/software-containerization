#!/bin/bash
minikube start --network-plugin=cni --cni=calico --kubernetes-version=v1.24.3 --extra-config=apiserver.Authorization.Mode=RBAC
minikube addons enable ingress
minikube addons enable dashboard
minikube addons enable metrics-server


