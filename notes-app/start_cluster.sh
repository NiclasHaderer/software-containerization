#!/bin/bash
minikube start --network-plugin=cni --cni=calico
minikube addons enable ingress
minikube addons enable dashboard


