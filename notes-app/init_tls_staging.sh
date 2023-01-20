
# This script is to create and apply a certificate to the cluster using cert-manager and letsencrypt.
# As letsencrypt is rate limited, this script should only be run once if a new cluster is created to set up the
# certificate.
# The certificate is then stored in a secret in the cluster and can be used by the ingress controller to
# encrypt the traffic to the cluster.
# So don't delete the secret!!


# 1) Install cert-manager on GKE according to: https://cert-manager.io/docs/tutorials/getting-started-with-cert-manager-on-google-kubernetes-engine-using-lets-encrypt-for-ingress-ssl/
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.8.2/cert-manager.yaml

# 2) Create an empty secret to store the certificate
kubectl delete -f cert-manager/k8-omes-app-tls-staging.secret.yaml --namespace default
kubectl apply -f cert-manager/k8-omes-app-tls-staging.secret.yaml --namespace default

# 3) Create a certificate issuer
kubectl delete -f cert-manager/lets-encrypt-staging.issuer.yaml --namespace default
kubectl apply -f cert-manager/lets-encrypt-staging.issuer.yaml --namespace default

# 4) Check if the certificate is ready
kubectl get certificate --namespace default -o wide
kubectl get certificaterequest --namespace default # describe the certificate request to see if it was successful
# kubectl describe certificaterequest k8-omes-app-tls-staging-hrnql


# everything according to
# https://cert-manager.io/docs/tutorials/getting-started-with-cert-manager-on-google-kubernetes-engine-using-lets-encrypt-for-ingress-ssl/