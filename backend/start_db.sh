docker run --rm \
  --name todo_posgres \
  -e POSTGRES_PASSWORD=super_secret \
  -e POSTGRES_USER=todo_user \
  -e POSTGRES_DB=todo \
  -p 5432:5432 \
  postgres:alpine