# This script is to create and apply a certificate to the cluster using cert-manager and letsencrypt.
# As letsencrypt is rate limited, this script should only be run once if a new cluster is created to set up the
# certificate.
# The certificate is then stored in a secret in the cluster and can be used by the ingress controller to
# encrypt the traffic to the cluster.
# So don't delete the secret!!

namespace="notes"

# 2) Create an empty secret to store the certificate
# kubectl delete -f cert-manager/k8-omes-app-tls-production.secret.yaml --namespace "$namespace"
kubectl apply -f cert-manager/k8-omes-app-tls-production.secret.yaml --namespace "$namespace"

# 3) Create a certificate issuer
# kubectl delete -f cert-manager/lets-encrypt-production.issuer.yaml --namespace "$namespace"
kubectl apply -f cert-manager/lets-encrypt-production.issuer.yaml --namespace "$namespace"


# 4) Check if the certificate is ready
kubectl get certificate --namespace "$namespace" -o wide
kubectl get certificaterequest --namespace "$namespace" # describe the certificate request to see if it was successful
# kubectl describe certificaterequest k8-omes-app-tls-staging-hrnql --namespace "$namespace"


# everything according to
# https://cert-manager.io/docs/tutorials/getting-started-with-cert-manager-on-google-kubernetes-engine-using-lets-encrypt-for-ingress-ssl/