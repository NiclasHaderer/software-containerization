exec_cmd(){
  #  Print in green
  # shellcheck disable=SC2028
  echo "\n"
  echo "\e[32m$1\e[0m"
  eval "$1"
  sleep 3
}

namespace="default"

# Show current contexts
exec_cmd "kubectl config get-contexts"
# Show that the pods can be listed
exec_cmd "kubectl get pods -n $namespace"
# Show the rolebinding for the user "notes-admin"
exec_cmd "kubectl describe rolebinding notes-app-auditor-binding -n $namespace"
# Show the permissions the role has
exec_cmd "kubectl get role notes-app-auditor -n $namespace -ojson | jq -r '.rules'"
# Switch to the new user
exec_cmd "kubectl config use-context notes-auditor-context"
exec_cmd "kubectl config get-contexts"
# Show that the default ns cannot be accessed
exec_cmd "kubectl get pods -n kube-system"
# But in the notes ns the user has full access
exec_cmd "kubectl get pods -n $namespace"
# Show that the user can create delete a pod
# Get the pod name
pod_name=$(kubectl get pods -n $namespace -ojson -l tier=frontend | jq -r '.items[0].metadata.name')
exec_cmd "kubectl delete pod $pod_name -n $namespace"