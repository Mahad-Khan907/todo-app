# Kubernetes Configuration for Todo AI Chatbot

This directory contains Kubernetes manifests for deploying the Todo AI Chatbot application.

## Overview

The Todo AI Chatbot is deployed as a microservices application with:

- **Backend Service**: FastAPI application
- **Frontend Service**: Next.js application
- **External Dependencies**: Neon PostgreSQL database and OpenAI APIs

## Directory Structure

```
k8s/
├── deployments/
│   ├── backend-deployment.yaml
│   └── frontend-deployment.yaml
├── services/
│   ├── backend-service.yaml
│   └── frontend-service.yaml
├── config/
│   └── configmaps-secrets.yaml
└── ingress/
    └── ingress.yaml
```

## Components

### Deployments

- `backend-deployment.yaml`: Deploys the backend FastAPI application
- `frontend-deployment.yaml`: Deploys the frontend Next.js application

Both deployments include:
- Resource limits and requests
- Health checks (liveness and readiness probes)
- Environment variable configuration
- Proper security context

### Services

- `backend-service.yaml`: Internal service for backend access
- `frontend-service.yaml`: External service for frontend access

### Config

- `configmaps-secrets.yaml`: Contains secrets for database URL and OpenAI API key

## Deployment

To deploy the application to a Kubernetes cluster:

```bash
# Apply all manifests
kubectl apply -f k8s/

# Or apply individual components
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/config/
```

## Configuration

The application expects the following secrets to be configured:

- `db-secret`: Contains `database-url` key with Neon PostgreSQL connection string
- `openai-secret`: Contains `api-key` key with OpenAI API key

## Security Features

- Non-root container execution
- Resource limits to prevent resource exhaustion
- Proper network segmentation with services
- Secure handling of sensitive information via secrets

## Scaling

Deployments are configured with 1 replica by default but can be scaled:

```bash
kubectl scale deployment backend-deployment --replicas=3
kubectl scale deployment frontend-deployment --replicas=3
```