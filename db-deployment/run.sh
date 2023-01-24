#!/bin/bash

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        --install)
            echo "Installing PostgreSQL..."
            kubectl apply -f configs/secret.yaml
            kubectl apply -f configs/configmap.yaml
            kubectl apply -f configs/pvc.yaml
            kubectl apply -f configs/deployment.yaml
            kubectl apply -f configs/service.yaml
            echo "PostgreSQL installation complete."
            shift
            ;;
        --delete)
            echo "Deleting PostgreSQL..."
            kubectl delete -f configs/service.yaml
            kubectl delete -f configs/deployment.yaml
            kubectl delete -f configs/pvc.yaml
            kubectl delete -f configs/configmap.yaml
            kubectl delete -f configs/secret.yaml
            echo "PostgreSQL deletion complete."
            shift
            ;;
        --fill)
            db_name=$(kubectl get pods -l "app=postgres" -o jsonpath="{.items[0].metadata.name}")
            echo "Filling PostgreSQL with data..."
            kubectl exec --stdin --tty "$db_name" -- psql -d some-db -U fancy-user -c 'CREATE TABLE IF NOT EXISTS fancy_table (id SERIAL PRIMARY KEY, fancy_column VARCHAR(255) NOT NULL);'
            kubectl exec --stdin --tty "$db_name" -- psql -d some-db -U fancy-user -c 'INSERT INTO fancy_table (fancy_column) VALUES ('"'"'fancy_value'"'"');'
            echo "PostgreSQL data filling complete."
            shift
            ;;
        --restart-deployment)
            echo "Restarting PostgreSQL deployment..."
            kubectl rollout restart deployment/postgres
            echo "PostgreSQL deployment restart complete."
            shift
            ;;
        --test)
            db_name=$(kubectl get pods -l app=postgres -o jsonpath="{.items[0].metadata.name}")
            echo "Testing PostgreSQL connection..."
            kubectl exec --stdin --tty "$db_name" -- psql -d some-db -U fancy-user -c '\dt'
            kubectl exec --stdin --tty "$db_name" -- psql -d some-db -U fancy-user -c 'SELECT * from fancy_table;'
            echo "PostgreSQL connection test complete."
            shift
            ;;
        *)
            echo "Invalid option: $key"
            shift
            ;;
    esac
done
