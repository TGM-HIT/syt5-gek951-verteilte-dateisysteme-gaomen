<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Verteilte Dateisysteme "Network Storage und Dateisysteme"</h3>

  <p align="center">
    This repository is for a task for systems technology.
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

In dieser Aufgabe soll MinIO mit Kubernetes deployed werden.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


# 1. Introduction

In this project, the task is to deploy MinIO, a high-performance distributed object storage system, on a Kubernetes cluster. MinIO can be used as an S3-compatible object storage solution, and this project aims to demonstrate how to set up and use it in a Kubernetes environment.

To achieve this, a simple Flask application, which interacts with MinIO, is also deployed on Kubernetes. This repository includes all the necessary scripts and configurations for deploying MinIO and the Flask application, enabling easy setup and management of the services within the cluster.

The setup process involves creating Kubernetes resources such as secrets, persistent volume claims (PVC), and deploying both the MinIO service and the Flask application service. Additionally, it covers how to expose these services using Kubernetes and how to test the deployed applications.


# 2. Architecture Overview

The architecture of this project revolves around deploying MinIO as an object storage service within a Kubernetes cluster, alongside a Flask application that interacts with MinIO. The architecture consists of the following key components:

  **Kubernetes Cluster**:
      The deployment is hosted on a Kubernetes cluster, either locally using tools like Minikube or on a cloud-based Kubernetes service.

  **MinIO Deployment**:
      MinIO is deployed as a stateful service that provides object storage in a distributed manner. It is configured to use persistent storage via Persistent Volume Claims (PVCs) for data durability.
      A Secret is created to store sensitive credentials for MinIO, which are used for secure access to the storage.

  **Flask Deployment**:
      A Flask application is deployed as a web service that interacts with MinIO via its S3-compatible API. This application can be used for tasks like uploading, downloading, and managing objects in the MinIO storage.
      The Flask service is exposed to external traffic using a LoadBalancer service, allowing users to access the application.

  **Networking and Exposure**:
      Both services (MinIO and Flask) are exposed through Kubernetes services. The Flask application is available to the outside world via a load balancer, while MinIO is exposed within the internal Kubernetes network.
      If using Minikube, the services are exposed to the host machine using minikube tunnel, enabling easy access to the services via their internal cluster IPs.

This architecture provides a scalable, highly available object storage solution (MinIO) integrated with a simple web application (Flask) to interact with the storage, all managed within Kubernetes.

### 2.2 Start the Application

To deploy the **Flask-MinIO** application on your Kubernetes cluster, follow the steps below:

#### 1. Start the Kubernetes Cluster

First, ensure your Kubernetes cluster is running. If you're using **Minikube**, start it with the following command:

```bash
minikube start  # If you're using Minikube
```

#### 2. Navigate to the Kubernetes Config Directory

Change to the directory where the Kubernetes configuration files are located:

```bash
cd python/kubernetes-config
```

#### 3. Grant Execution Permissions to Scripts

Before running the deployment scripts, make sure they are executable:

```bash
chmod +x apply.sh generate-secrets.sh unapply.sh
```

#### 4. Generate MinIO Secrets

Generate the MinIO secret by running the script:

```bash
./generate-secrets.sh  # Creates minio-secret.yaml
```

This will create the necessary secrets file (`minio-secret.yaml`) required for secure access to the MinIO service.

#### 5. Apply the Kubernetes Configuration

Now, apply the Kubernetes configurations to deploy MinIO and the Flask application:

```bash
./apply.sh
```

This will create the following Kubernetes resources:

```bash
secret/minio-secret created
persistentvolumeclaim/minio-pvc created
deployment.apps/minio created
service/minio-service created
deployment.apps/flask-minio-app created
service/flask-minio-service created
```

Your services are now deployed on the Kubernetes cluster.

---

### 2.2 View the Services

Once the application is deployed, you can check the status of the services by running:

```bash
kubectl get svc
```

The output should look like this:

```bash
NAME                  TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
flask-minio-service   LoadBalancer   10.105.27.152   <pending>     8080:32587/TCP   2m54s
kubernetes            ClusterIP      10.96.0.1       <none>        443/TCP          3m4s
minio-service         ClusterIP      10.111.80.241   <none>        9000/TCP         2m54s
```

Here, you can see that both the `flask-minio-service` and `minio-service` have been created. However, the `flask-minio-service` is behind a **LoadBalancer**, and its external IP is still pending.

#### 1. Expose the Services (Minikube only)

##### Tunnel
If you're using **Minikube**, you'll need to tunnel the service to your local machine to access it. Run the following command:

```bash
minikube tunnel
```

This will set up a tunnel to expose the `flask-minio-service` to your local machine. You should see an output similar to this:

```bash
Status:
        machine: minikube
        pid: 30280
        route: 10.96.0.0/12 -> 192.168.49.2
        minikube: Running
        services: [flask-minio-service]
    errors:
                minikube: no errors
                router: no errors
                loadbalancer emulator: no error
```

##### Port Forward

```bash
kubectl port-forward svc/flask-minio-service 8080:8080
```

##### Expose it to the internet

Using a reverse proxy you can expose the service to the internet

```bash
sudo dnf install nginx
sudo vi /etc/nginx/sites-available/default

```

```
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://${CLUSTER_IP}:${PORT};

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Now restart test the configuration and restart the service

```bash
sudo nginx -t
sudo systemctl restart nginx
```

#### 2. Test the Flask-MinIO Service

Now, you can connect to the Flask application using the `CLUSTER-IP` of the `flask-minio-service` and port `8080`. For example:

```bash
curl 10.105.27.152:8080
```

This should return a response from the Flask application.

---

### 2.3 Delete the Services

To clean up and delete the entire deployment, run the **unapply** script:

```bash
./unapply.sh
```

This will remove all resources created by the `apply.sh` script, including the deployments, services, and secrets.
