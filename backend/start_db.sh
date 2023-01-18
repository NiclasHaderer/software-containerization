docker run --rm \
  --name todo_postgres \
  -e POSTGRES_PASSWORD=super_secret \
  -e POSTGRES_USER=todo_user \
  -e POSTGRES_DB=notes \
  -p 5432:5432 \
  postgres:alpine