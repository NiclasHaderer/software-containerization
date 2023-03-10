exec_cmd(){
  #  Print in green
  echo ""
  printf "\e[32m$1\e[0m"
  echo ""
  eval "$1"
  sleep 3
}

kubectl config use-context gke_containerisation_europe-west4-a_containerization-cluster-v2 > /dev/null

# Show current contexts
exec_cmd "kubectl config get-contexts"
# Show that the pods can be listed
exec_cmd "kubectl get pods -n notes"
# Show the rolebinding for the user "notes-admin"
exec_cmd "kubectl describe rolebinding notes-app-admin-binding -n notes"
# Show the permissions the role has
exec_cmd "kubectl get role notes-app-admin -n notes -ojson | jq -r '.rules'"
# Switch to the new user
exec_cmd "kubectl config use-context notes-admin-context"
exec_cmd "kubectl config get-contexts"
# Show that the default ns cannot be accessed
exec_cmd "kubectl get pods -n kube-system"
# But in the notes ns the user has full access
exec_cmd "kubectl get pods -n notes"
# Show that the user can create delete a pod
# Get the pod name
pod_name=$(kubectl get pods -n notes -ojson -l tier=frontend | jq -r '.items[0].metadata.name')
exec_cmd "kubectl delete pod $pod_name -n notes"