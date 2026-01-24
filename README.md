# Todo AI Chatbot - Kubernetes Deployment

This project demonstrates the deployment of the Todo AI Chatbot application to Kubernetes using AI-assisted tools.

## Overview

The Todo AI Chatbot application is containerized and deployed to Kubernetes with the following components:

- **Backend Service**: FastAPI application with AI integration
- **Frontend Service**: Next.js application with chat interface
- **External Dependencies**: Neon PostgreSQL database and OpenAI APIs
- **Deployment Method**: AI-generated Dockerfiles, Kubernetes manifests, and Helm charts

## Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Frontend      │────│   Backend        │
│   (Next.js)     │    │   (FastAPI)      │
└─────────────────┘    └──────────────────┘
         │                        │
         └────────────────────────┘
                     │
        ┌─────────────────────────┐
        │ External Dependencies   │
        │ - Neon PostgreSQL       │
        │ - OpenAI APIs           │
        └─────────────────────────┘
```

## Containerization

The application is containerized using AI-generated Dockerfiles:

- **Backend**: Multi-stage Dockerfile with security optimizations
- **Frontend**: Production-ready Dockerfile with proper signal handling

See the `docker/` directory for details.

## Kubernetes Deployment

The application is deployed to Kubernetes using:

- **Kubernetes Manifests**: AI-generated deployments, services, and secrets
- **Helm Charts**: AI-generated charts for simplified deployment

See the `k8s/` and `charts/` directories for details.

## Quick Start

### Prerequisites

- Docker
- Kubernetes cluster (Minikube, Kind, or cloud provider)
- Helm 3.x
- kubectl

### Deployment Steps

1. Build the Docker images:
   ```bash
   docker build -f docker/backend.Dockerfile -t todo-backend:v1 .
   docker build -f docker/frontend.Dockerfile -t todo-frontend:v1 .
   ```

2. Deploy using Helm:
   ```bash
   helm install todo-app charts/todo-app \
     --set database.url="your-neon-db-url" \
     --set openai.apiKey="your-openai-api-key"
   ```

3. Access the application:
   ```bash
   kubectl port-forward svc/todo-app-frontend 3000:3000
   ```

## Features

- **AI-Assisted Generation**: Dockerfiles, Kubernetes manifests, and Helm charts generated using AI tools
- **Security Best Practices**: Non-root containers, resource limits, secrets management
- **Health Checks**: Built-in liveness and readiness probes
- **Scalability**: Designed for horizontal scaling
- **External Connectivity**: Maintains connection to external Neon PostgreSQL and OpenAI APIs

## Directory Structure

```
├── docker/                 # AI-generated Dockerfiles
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── k8s/                  # AI-generated Kubernetes manifests
│   ├── deployments/
│   ├── services/
│   └── config/
└── charts/               # AI-generated Helm charts
    └── todo-app/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
```

## Configuration

The application can be configured via Helm values:

- `replicaCount`: Number of pod replicas
- `image.*`: Image repositories and tags
- `service.*`: Service configuration
- `database.url`: Neon PostgreSQL connection string
- `openai.apiKey`: OpenAI API key

## Security

- Containers run as non-root users
- Resource limits prevent resource exhaustion
- Secrets are stored securely in Kubernetes
- Network segmentation with services

## Troubleshooting

Check pod status:
```bash
kubectl get pods
```

View pod logs:
```bash
kubectl logs <pod-name>
```

Check service status:
```bash
kubectl get services
```

## Next Steps

- Implement CI/CD pipeline for automated deployments
- Add monitoring and observability
- Set up ingress controller for external access
- Implement auto-scaling based on demand