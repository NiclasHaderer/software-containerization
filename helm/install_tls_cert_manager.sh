#!/bin/bash

# !!! This leads to a certificate that is not valid for the domain !!!
# -> Rate limit could get exceeded

# 1) Install cert-manager on GKE according to: https://cert-manager.io/docs/tutorials/getting-started-with-cert-manager-on-google-kubernetes-engine-using-lets-encrypt-for-ingress-ssl/
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.8.2/cert-manager.yaml
