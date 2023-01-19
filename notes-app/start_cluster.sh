#!/bin/bash
minikube start --cni calico
minikube addons enable ingress
minikube addons enable dashboard


