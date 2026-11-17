# Phase 5 Deployment Guide: Event-Driven Architecture with Dapr

This guide outlines the deployment process for the Todo application with event-driven architecture using Kafka/Redpanda and Dapr.

## Architecture Overview

The system consists of the following components:

1. **Backend Service**: Main FastAPI application with recurring tasks and reminders
2. **Frontend Service**: Next.js web interface
3. **Notification Service**: Handles reminder email notifications
4. **Recurring Task Service**: Processes recurring task events
5. **Kafka/Redpanda**: Event streaming platform for pub/sub
6. **PostgreSQL**: Primary database for task and user data
7. **Dapr**: Distributed application runtime for microservices patterns

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (Minikube, Docker Desktop, or cloud provider)
- Dapr CLI installed (`dapr init -k`)
- kubectl
- Helm 3

## Local Development Setup

### 1. Initialize Dapr

```bash
# Initialize Dapr in Kubernetes mode
dapr init -k

# Verify installation
dapr status -k
```

### 2. Set up Environment Variables

Create a `.env` file with your configuration:

```bash
DATABASE_URL="postgresql://username:password@neon_db_endpoint/dbname"
OPENAI_API_KEY="your_openai_api_key"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USERNAME="your_email@gmail.com"
SMTP_PASSWORD="your_app_password"
```

### 3. Build Docker Images

```bash
# Build backend image
docker build -f docker/backend.Dockerfile -t todo-backend:v1 .

# Build frontend image
docker build -f docker/frontend.Dockerfile -t todo-frontend:v1 .

# Build notification service image
docker build -f docker/notification.Dockerfile -t todo-notification-service:v1 .

# Build recurring task service image
docker build -f docker/recurring-task.Dockerfile -t todo-recurring-task-service:v1 .
```

### 4. Deploy to Kubernetes

#### Option A: Using individual manifests

```bash
# Create namespaces
kubectl create namespace todo-app || true

# Deploy secrets
kubectl apply -f k8s/secrets.yaml

# Deploy Dapr components
kubectl apply -f dapr/components/

# Deploy Dapr configuration
kubectl apply -f k8s/config/dapr-config.yaml

# Deploy Kafka/Redpanda
kubectl apply -f k8s/deployments/redpanda-deployment.yaml

# Wait for Kafka to be ready
kubectl wait --for=condition=ready pod -l app=redpanda --timeout=300s

# Initialize Kafka topics
kubectl apply -f k8s/jobs/kafka-topic-initializer.yaml

# Deploy services
kubectl apply -f k8s/deployments/dapr-backend-deployment.yaml
kubectl apply -f k8s/deployments/dapr-frontend-deployment.yaml
kubectl apply -f k8s/deployments/notification-service-deployment.yaml
kubectl apply -f k8s/deployments/recurring-task-service-deployment.yaml
```

#### Option B: Using Helm

```bash
# Add your Docker Hub images to values.yaml
# Then install the chart
helm install todo-app charts/todo-app/ --namespace todo-app --create-namespace
```

### 5. Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check Dapr sidecars
kubectl get pods -n todo-app -L dapr.io/app-id

# View logs
kubectl logs -l app=backend -n todo-app
kubectl logs -l app=frontend -n todo-app
```

## Event-Driven Architecture

### Kafka Topics

The system uses the following Kafka topics:

- `task-events`: Events for task creation, updates, and completions
- `reminders`: Events for reminder notifications
- `task-updates`: Events for task state changes

### Service Interactions

1. **Backend Service**: Publishes events to Kafka topics when tasks are created/updated/completed
2. **Notification Service**: Consumes `reminders` topic to send email notifications
3. **Recurring Task Service**: Consumes `task-events` topic to generate recurring task instances

### Dapr Components

- **Pub/Sub**: Kafka pubsub component for event streaming
- **State Store**: PostgreSQL state store for persistent data
- **Bindings**: Cron binding for scheduled reminder checks
- **Secrets**: Kubernetes secrets store for secure configuration

## Production Deployment

### 1. Update Values

Modify `charts/todo-app/values.yaml` with production values:

```yaml
images:
  backend:
    repository: your-dockerhub-username/todo-backend
    tag: latest
  frontend:
    repository: your-dockerhub-username/todo-frontend
    tag: latest
  # ... other images

replicaCount:
  backend: 3
  frontend: 2
  notification: 2
  recurring: 2
```

### 2. Push Docker Images

```bash
# Tag and push images to Docker Hub
docker tag todo-backend:v1 your-dockerhub-username/todo-backend:latest
docker push your-dockerhub-username/todo-backend:latest

docker tag todo-frontend:v1 your-dockerhub-username/todo-frontend:latest
docker push your-dockerhub-username/todo-frontend:latest

docker tag todo-notification-service:v1 your-dockerhub-username/todo-notification-service:latest
docker push your-dockerhub-username/todo-notification-service:latest

docker tag todo-recurring-task-service:v1 your-dockerhub-username/todo-recurring-task-service:latest
docker push your-dockerhub-username/todo-recurring-task-service:latest
```

### 3. Deploy Production

```bash
helm upgrade --install todo-app-prod charts/todo-app/ \
  --namespace todo-prod \
  --create-namespace \
  --values charts/todo-app/values-prod.yaml
```

## Monitoring and Maintenance

### Health Checks

Each service includes health check endpoints:
- Backend: `GET /health`
- Frontend: `GET /health`
- Notification: `GET /health`
- Recurring Task: `GET /health`

### Dapr Observability

```bash
# Check Dapr sidecar health
dapr status -k

# View Dapr logs
kubectl logs -l app=dapr-placement -n dapr-system
kubectl logs -l app=dapr-operator -n dapr-system
```

## Troubleshooting

### Common Issues

1. **Dapr Sidecar Not Injected**
   ```bash
   # Check if Dapr is properly installed
   kubectl get pods -n dapr-system

   # Verify annotations in deployment
   kubectl describe pod <pod-name> -n todo-app
   ```

2. **Kafka Connectivity Issues**
   ```bash
   # Check Kafka pods
   kubectl get pods -l app=redpanda

   # Test connectivity from within cluster
   kubectl run test-client --image=confluentinc/cp-kafka:latest --rm -it --restart=Never -- /bin/bash
   ```

3. **Service Discovery Problems**
   ```bash
   # Check services
   kubectl get svc -n todo-app

   # Test service connectivity
   kubectl run test --image=curlimages/curl --rm -it --restart=Never -- curl -v http://backend-service:8000/health
   ```

### Scaling Services

```bash
# Scale backend service
kubectl scale deployment todo-app-backend --replicas=3 -n todo-app

# Scale based on CPU utilization
kubectl autoscale deployment todo-app-backend --cpu-percent=70 --min=2 --max=10 -n todo-app
```

## Cleanup

To remove the deployment:

```bash
# Remove Helm release
helm uninstall todo-app -n todo-app

# Or remove individual resources
kubectl delete -f k8s/deployments/
kubectl delete -f k8s/config/
kubectl delete -f dapr/components/
kubectl delete -f k8s/secrets.yaml

# Remove Dapr
dapr uninstall -k
```

This completes the deployment of the event-driven Todo application with Dapr and Kafka integration.