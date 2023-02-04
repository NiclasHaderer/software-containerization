# Frontend

## Information
The frontend is implemented using Angular. It is a single page 
application that communicates with the backend using REST API calls.

## Build and run

### Without Docker

Run `yarn install` to install the depenencies
Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`.
The app will automatically reload if you change any of the source files.

### With Docker
Run `docker build -t frontend .` to build the image. To run the image use 
`docker run -p 80:80 frontend` and navigate to `http://localhost:80/`.

