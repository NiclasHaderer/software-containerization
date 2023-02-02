exec_cmd(){
  #  Print in green
  # shellcheck disable=SC2028
  echo "\n"
  printf "\e[32m$1\e[0m"
  echo "\n"
  eval "$1"
  sleep 3
}

kubectl config use-context gke_containerisation_europe-west4-a_containerization-cluster-v2 > /dev/null

# Show current contexts
exec_cmd "kubectl config get-contexts"
exec_cmd "kubectl config use-context notes-cluster-admin-context"
exec_cmd "kubectl get clusterroles notes-cluster-admin -ojson | jq -r '.rules'"

# Show that the user can create delete a pod
# Get the pod name
pod_name=$(kubectl get pods -n notes -ojson -l tier=frontend | jq -r '.items[0].metadata.name')
exec_cmd "kubectl delete pod $pod_name -n notes"
# Show that the user can list pods in the kube-system namespace
exec_cmd "kubectl get pods -n kube-system"