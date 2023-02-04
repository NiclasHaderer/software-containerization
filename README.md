# Software containerization
This is the project for the Software Containerization of 2023 course at VU Amsterdam by group 42. We didn't 
find "the answer to life, the universe and everything", but we did find a way to containerize software and deploy
it to a Kubernetes cluster. 

The repository is publicly available on [GitHub](https://github.com/NiclasHaderer/software-containerization).
For questions, please contact us via email. Unfortunately, we are not able to let the cluster run as it is 
quite expensive, so we cannot provide a public URL for a live demo.

##  Components
The software containerization project consists of two components: 
the backend and the frontend. The backend is a REST API that 
allows to create, start, stop and delete posts and persist 
them in a database. The frontend is a web application that 
allows to interact with the backend.

Furthermore, a helm chart of a postgres database is provided to which 
the backend can connect to.

### Backend

See [Backend ReadMe](./backend/README.md) for more information on how to build and run the backend.

### Frontend

See the [Frontend ReadMe](./frontend/README.md) for more information on how to build and run the frontend.

## Deployment
The application can be deployed using kubernetes and helm. While developing the application, 
we used minikube to deploy the application locally as well as the Google Kubernetes Engine (GKE) 
to deploy the application on a cloud provider. This lead to the problem of two different 
configuration possibilities as not all features of kubernetes are available on minikube/GKE.


### Helm Chart
To deploy the whole application, a helm chart is provided. It is located in the `helm` folder. 
To define whether to deploy the application to minikube or GKE, the `values.yaml` file can be
edited. The `values.yaml` file contains the following values:

```yaml
deployment:
  type: minikube # minikube or gke
```
This has f. e. effects on the type of ingress that is used. For minikube, the nginx ingress is used, 
while for GKE, the GKE ingress is used.

To make the deployment as easy as possible, we created two scripts within the `helm` folder that can be used to deploy the
application to minikube or GKE. They are located in the `scripts` folder. To deploy the application
to minikube, the `deploy_local.sh` script can be used. To deploy the application to GKE, the
`deploy_cloud.sh` script can be used. Both scripts require the `helm` command to be installed.

#### GKE
In order to deploy the application to GKE, you have to configure your kubectl to use the GKE cluster using the `gcloud` command.
```bash
./deploy_cloud.sh --install    # installs the application
./deploy_cloud.sh --delete     # uninstalls the application
./deploy_cloud.sh --upgrade    # upgrades the application
./deploy_cloud.sh --reinstall  # deletes and installs the application
```

#### Minikube
The minikube script offers fewer options, by running it, if an existing deployment is found, it will be deleted and a new one will be installed.
```bash
./deploy_local.sh
```
### TLS
The application can be deployed with TLS enabled. The necessary resources are created by executing the
`init_tls_staging.sh` or `init_tls_production.sh` script. Both will apply an Issuer and a Secret for the TLS certificate 
to the cluster. The `init_tls_production.sh` script will use the production Let's Encrypt server, while the `init_tls_staging.sh`
script will use the staging server. The staging server is used for testing purposes and does not have a rate limit, while the production
server has a rate limit of 5 certificates per domain per week.

The application is currently configured to use the production certificate. TLS is only enabled when deploying to GKE.

### Network Policies
We used network policies to restrict the communication between the different components of the application. 
The network policies are located in the `templates` folder of the helm chart and are applied when the application is deployed.

Depending on whether the application is deployed to minikube or GKE, the network policies are different as not all features 
of kubernetes are available on minikube/GKE.

### RBAC
The application uses RBAC to restrict the access to the different components of the application. The scripts to create users 
are located in the `rbac` folder in the root directory of the project and have to be applied manually.
RoleBindings and Roles resources are located in the `templates` folder of the helm chart and are applied when the application is deployed.

To create the users as shown in the presentation, navigate in the `rbac` folder and to use the following scripts:
```bash
./create-user.sh "notes-auditor"
./create-user.sh "notes-admin"
./create-user.sh "notes-cluster-admin"
```

Showcase the permissions of the different users

```bash
./showcase-admin.sh
./showcase-auditor.sh
./showcase-cluster-admin.sh
```
The RBAC configuration is tested and showcased using the GKE cluster. 

