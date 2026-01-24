# Quickstart Guide: Kubernetes Deployment

**Feature**: Kubernetes Deployment
**Date**: 2026-01-18
**Author**: Claude Code

## Overview

This guide explains how to deploy the Todo AI Chatbot application to a local Kubernetes cluster using Minikube and AI-generated configuration files. This deployment follows cloud-native principles with containerized services.

## Prerequisites

Before starting, ensure you have the following tools installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Kubernetes enabled OR [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- [kubectl-ai](https://github.com/itaysk/kubectl-ai) (for AI-assisted Kubernetes operations)
- [Docker AI Agent (Gordon)](https://docs.docker.com/desktop/ai/) (for AI-assisted Docker operations)

## Setup Instructions

### 1. Clone and Navigate to Repository

```bash
git clone <repository-url>
cd <repository-directory>
git checkout 003-k8s-deployment
```

### 2. Start Minikube Cluster

```bash
minikube start --driver=docker
minikube status
```

### 3. Generate Docker Images

Using Docker AI Agent (Gordon) to generate multi-stage Dockerfiles:

```bash
# Generate backend Dockerfile
docker ai "Create a multi-stage Dockerfile for a Python FastAPI application with uv package manager in the todo-hack/phases 4/backend directory"

# Generate frontend Dockerfile
docker ai "Create a multi-stage Dockerfile for a Next.js 16+ application with TypeScript in the todo-hack/phases 4/frontend directory"

# Build backend image
cd backend
docker build -t todo-backend:v1.0.0 .
cd ..

# Build frontend image
cd frontend
docker build -t todo-frontend:v1.0.0 .
cd ..
```

### 4. Generate Kubernetes Manifests with AI

Using kubectl-ai to generate Kubernetes deployment files:

```bash
# Generate backend deployment
kubectl ai "generate a k8s deployment yaml for a Python FastAPI app named todo-backend using the todo-backend:v1.0.0 image, save to k8s/backend-deployment.yaml"

# Generate frontend deployment
kubectl ai "generate a k8s deployment yaml for a Next.js app named todo-frontend using the todo-frontend:v1.0.0 image, save to k8s/frontend-deployment.yaml"

# Generate backend service
kubectl ai "generate a k8s service yaml to expose the todo-backend deployment on port 8000, save to k8s/backend-service.yaml"

# Generate frontend service
kubectl ai "generate a k8s service yaml to expose the todo-frontend deployment on port 3000 as a NodePort service, save to k8s/frontend-service.yaml"
```

### 5. Create Kubernetes Secrets

Create secrets for API keys and database connection:

```bash
# Create a namespace for the application
kubectl create namespace todo-app

# Create secrets (replace with your actual values)
kubectl create secret generic todo-secrets \
  --from-literal=OPENAI_API_KEY=<your-openai-api-key> \
  --from-literal=DATABASE_URL=<your-neon-db-url> \
  --namespace=todo-app
```

### 6. Generate Helm Chart

Using kubectl-ai or kagent to generate a Helm chart:

```bash
# Generate Helm chart
kubectl ai "generate a Helm chart named todo-app with templates for deployments and services, save to charts/todo-app/"

# Verify chart structure
tree charts/todo-app/
```

### 7. Deploy Application with Helm

```bash
# Install the Helm chart
helm install todo-chatbot ./charts/todo-app --namespace todo-app --create-namespace

# Verify deployment
kubectl get pods -n todo-app
kubectl get services -n todo-app
```

### 8. Access the Application

```bash
# Get the frontend service URL
minikube service todo-frontend-service -n todo-app --url

# Alternatively, use port forwarding
kubectl port-forward svc/todo-frontend-service 3000:3000 -n todo-app
```

## Verification Steps

1. Check that all pods are running:
   ```bash
   kubectl get pods -n todo-app
   ```

2. Check that services are available:
   ```bash
   kubectl get services -n todo-app
   ```

3. Access the frontend in your browser using the Minikube service URL

4. Verify that the AI Chatbot functionality works as expected

5. Test that task management features work correctly

## Troubleshooting

### Common Issues

1. **Pods stuck in Pending state**: Check resource requests/limits and node capacity
2. **Service unavailable**: Verify service configuration and selector labels
3. **Secrets not mounting**: Check secret names and volume mounts in deployment
4. **External API access failing**: Verify API keys in secrets and network policies

### Useful Commands

```bash
# Check pod logs
kubectl logs <pod-name> -n todo-app

# Get detailed pod information
kubectl describe pod <pod-name> -n todo-app

# Port forward for local testing
kubectl port-forward -n todo-app deployment/todo-frontend-deployment 3000:3000

# Check Helm release status
helm status todo-chatbot -n todo-app

# Rollback to previous version if needed
helm rollback todo-chatbot -n todo-app
```

## Cleanup

To remove the deployment:

```bash
# Uninstall Helm release
helm uninstall todo-chatbot -n todo-app

# Delete namespace
kubectl delete namespace todo-app

# Stop Minikube
minikube stop
```

## Next Steps

1. Set up monitoring with Prometheus and Grafana
2. Configure horizontal pod autoscaling
3. Implement CI/CD pipeline for automated deployments
4. Add network policies for enhanced security