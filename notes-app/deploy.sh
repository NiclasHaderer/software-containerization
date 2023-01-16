
kubectl create secret generic pg-user-password --from-literal=password=mysecretpassword
helm install my_notes .