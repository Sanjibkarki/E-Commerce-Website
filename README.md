A full-stack E-Commerce web application built with **Django**, containerized using **Docker**, and deployed on **Kubernetes (kind)** with **Nginx** as reverse proxy and SSL support.

---

## Tech Stack

- Backend: Django (Python 3.11)
- Frontend: Django Templates
- Database: PostgreSQL
- Web Server: Nginx
- Containerization: Docker
- Orchestration: Kubernetes (kind)
- SSL: Self-signed certificates

##  Deployment Workflow

### Step 1 — Build Docker Image

Build the Django application image:

```bash
docker build -t sanjeev/ecommerce:latest .

### Step 2 — Create Cluster using Kind
kind create cluster --config kubernetes/kind-config.yaml

##  Step 3 - Then create a PVC for the pods
kubectl apply -f kubernetes/static.yaml
kubectl apply -f kubernetes/media.yaml

##  Step 4 -  Create PODS
kubectl apply -f kubenetes/
