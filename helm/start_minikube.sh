#!/bin/bash
minikube start --network-plugin=cni --cni=calico --kubernetes-version=v1.24.3
minikube addons enable ingress
minikube addons enable dashboard


