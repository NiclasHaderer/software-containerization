FROM node:18 as builder
WORKDIR /app
COPY . .
RUN yarn install --forzen-lockfile
RUN yarn run build --configuration=production

FROM nginx:1.23-alpine-slim
COPY --from=builder /app/dist/todo-list /usr/share/nginx/html
COPY /nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
