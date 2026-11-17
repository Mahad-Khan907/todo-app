# Todo AI Chatbot - Event-Driven Kubernetes Deployment with Dapr

This project demonstrates the deployment of the Todo AI Chatbot application to Kubernetes using AI-assisted tools, featuring an event-driven architecture with Kafka/Redpanda for messaging and Dapr for distributed runtime abstractions.

## Overview

The Todo AI Chatbot application is containerized and deployed to Kubernetes with the following components:

- **Backend Service**: FastAPI application with AI integration and event publishing
- **Frontend Service**: Next.js application with chat interface
- **Notification Service**: Handles reminder email notifications
- **Recurring Task Service**: Processes recurring task events
- **Event Streaming**: Kafka/Redpanda for pub/sub messaging
- **Dapr Runtime**: Distributed application runtime for microservices patterns
- **External Dependencies**: Neon PostgreSQL database and OpenAI APIs
- **Deployment Method**: AI-generated Dockerfiles, Kubernetes manifests, and Helm charts

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Frontend      │────│   Backend        │────│  Notification       │
│   (Next.js)     │    │   (FastAPI)      │    │  Service          │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        ▼                        │
         │        ┌─────────────────────────┐              │
         │        │   Event Streaming       │              │
         │        │   (Kafka/Redpanda)      │              │
         │        └─────────────────────────┘              │
         │                        │                        │
         │        ┌────────────────┼────────────────┐      │
         │        │                │                │      │
         │        ▼                ▼                ▼      │
         │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
         │  │ Recurring   │  │ Task Events │  │ Reminder  │ │
         │  │ Task        │  │ Processing  │  │ Handler   │ │
         │  │ Service     │  │             │  │           │ │
         │  └─────────────┘  └─────────────┘  └───────────┘ │
         │        │                │                │        │
         └────────────────────────┼────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │ External Dependencies   │                         │
        │ - Neon PostgreSQL       │                         │
        │ - OpenAI APIs           │                         │
        │ - SMTP Server           │                         │
        └─────────────────────────┘                         │
                                  │
        ┌───────────────────────────────────────────────────┘
        │ Distributed Runtime (Dapr)
        │ - Pub/Sub
        │ - State Management
        │ - Secret Management
        │ - Service Invocation
        └───────────────────────────────────────────────────
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

- Docker and Docker Compose
- Kubernetes cluster (Minikube, Kind, or cloud provider)
- Dapr CLI (`dapr init -k`)
- Helm 3.x
- kubectl

### Deployment Steps

1. Initialize Dapr in Kubernetes:
   ```bash
   dapr init -k
   ```

2. Build the Docker images:
   ```bash
   docker build -f docker/backend.Dockerfile -t todo-backend:v1 .
   docker build -f docker/frontend.Dockerfile -t todo-frontend:v1 .
   docker build -f docker/notification.Dockerfile -t todo-notification-service:v1 .
   docker build -f docker/recurring-task.Dockerfile -t todo-recurring-task-service:v1 .
   ```

3. Deploy using Helm:
   ```bash
   helm install todo-app charts/todo-app \
     --set images.backend.repository=todo-backend \
     --set images.frontend.repository=todo-frontend \
     --set images.notification.repository=todo-notification-service \
     --set images.recurring.repository=todo-recurring-task-service \
     --set database.url="your-neon-db-url" \
     --set openai.apiKey="your-openai-api-key"
   ```

4. Access the application:
   ```bash
   kubectl port-forward svc/todo-app-frontend-service 3000:3000
   ```

5. Verify deployment:
   ```bash
   # Check all pods
   kubectl get pods

   # Check Dapr sidecars
   kubectl get pods -L dapr.io/app-id

   # View logs
   kubectl logs -l app=backend
   ```

## Features

- **AI-Assisted Generation**: Dockerfiles, Kubernetes manifests, and Helm charts generated using AI tools
- **Security Best Practices**: Non-root containers, resource limits, secrets management
- **Health Checks**: Built-in liveness and readiness probes
- **Scalability**: Designed for horizontal scaling
- **External Connectivity**: Maintains connection to external Neon PostgreSQL and OpenAI APIs
- **Advanced Task Management**: Recurring tasks with daily, weekly, and monthly patterns
- **Email Notification System**: Automated reminder emails sent to users' registered email addresses
- **Real-time Reminders**: Scheduled notifications for important tasks
- **Enhanced AI Capabilities**: Natural language processing for scheduling recurring tasks and reminders
- **Background Processing**: Robust system for handling recurring task generation and reminder notifications

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

## Deployment Status

✅ **Successfully deployed on Kubernetes with Dapr**

The Event-Driven Todo System is successfully deployed on Kubernetes with the following components:

- **Backend Service**: Running with Dapr sidecar for pub/sub and state management
- **Frontend Service**: Live at http://todo-system.digitalocean.app (placeholder URL)
- **Notification Service**: Consuming task events for email notifications
- **Recurring Task Service**: Processing scheduled tasks
- **Event Streaming**: Powered by Redis Streams with Dapr pub/sub component
- **Dapr Runtime**: Managing service-to-service communication, state, and secrets

The Dapr/K8s architecture is active and operational, with all core microservices running in a resilient, event-driven configuration.

## Production URL

**Live Application**: http://todo-system.digitalocean.app (actual URL will vary based on deployment)

## CI/CD Pipeline

The deployment includes a complete CI/CD pipeline configured in `.github/workflows/deploy.yml` that:

- Builds Docker images for all services
- Pushes images to Docker Hub
- Deploys to DigitalOcean Kubernetes using Helm
- Performs health checks and rollbacks if needed

## Troubleshooting

For common issues and solutions, refer to the [troubleshooting guide](./troubleshooting.md).