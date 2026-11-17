# Phase 5: Event-Driven Cloud-Native Deployment

This Phase 5 implementation transforms the Todo AI Chatbot into an event-driven architecture using Kafka/Redpanda for messaging and Dapr for distributed runtime abstractions.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Components](#components)
- [Event-Driven Design](#event-driven-design)
- [Dapr Integration](#dapr-integration)
- [Deployment Options](#deployment-options)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The system implements a microservices architecture with event-driven communication patterns:

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

## Components

### Core Services
- **Backend Service**: FastAPI application with AI integration and event publishing
- **Frontend Service**: Next.js application with chat interface
- **Notification Service**: Handles reminder email notifications
- **Recurring Task Service**: Processes recurring task events

### Infrastructure
- **Kafka/Redpanda**: Event streaming platform for pub/sub messaging
- **PostgreSQL**: Primary database for task and user data
- **Dapr**: Distributed application runtime for microservices patterns
- **Redis**: Caching and session storage

## Event-Driven Design

### Kafka Topics
- `task-events`: Events for task creation, updates, and completions
- `reminders`: Events for reminder notifications
- `task-updates`: Events for task state changes

### Event Flow
1. User interacts with frontend → events published to Kafka
2. Backend receives events and processes business logic
3. Backend publishes events to Kafka topics based on actions
4. Notification service consumes reminder events and sends emails
5. Recurring task service consumes task events and generates recurring instances

## Dapr Integration

### Components Used
- **Pub/Sub**: Kafka pubsub component for event streaming
- **State Store**: PostgreSQL state store for persistent data
- **Bindings**: Cron binding for scheduled reminder checks
- **Secrets**: Kubernetes secrets store for secure configuration
- **Service Invocation**: For inter-service communication

### Configuration
Located in `dapr/components/`:
- `pubsub.yaml`: Kafka pubsub configuration
- `statestore.yaml`: PostgreSQL state store configuration
- `cron-binding.yaml`: Cron binding for scheduled tasks
- `secrets.yaml`: Kubernetes secrets configuration

## Deployment Options

### Local Development
```bash
# Start all services with Docker Compose
docker-compose -f docker-compose-full.yml up --build

# Initialize Kafka topics manually
docker exec -it <kafka-container> kafka-topics --create --topic task-events --bootstrap-server localhost:9092
docker exec -it <kafka-container> kafka-topics --create --topic reminders --bootstrap-server localhost:9092
docker exec -it <kafka-container> kafka-topics --create --topic task-updates --bootstrap-server localhost:9092
```

### Kubernetes with Dapr
```bash
# Initialize Dapr
dapr init -k

# Build and push images
./scripts/build-and-push-images.sh <dockerhub-username>

# Deploy to Kubernetes
./scripts/deploy-to-k8s.sh <dockerhub-username>
```

### Helm Deployment
```bash
# Update values.yaml with your Docker Hub images
helm upgrade --install todo-app charts/todo-app/ \
  --namespace todo-app \
  --create-namespace \
  --values charts/todo-app/values.yaml
```

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Kubernetes cluster (Minikube, Docker Desktop, or cloud provider)
- Dapr CLI (`dapr init -k`)
- kubectl
- Helm 3.x

### Environment Variables
Create a `.env` file:
```bash
DATABASE_URL="postgresql://username:password@localhost:5432/todo_db"
OPENAI_API_KEY="your_openai_api_key"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USERNAME="your_email@gmail.com"
SMTP_PASSWORD="your_app_password"
```

### Local Development Workflow
1. Make code changes
2. Rebuild containers: `docker-compose -f docker-compose-full.yml up --build`
3. Test functionality
4. Commit changes

## Production Deployment

### Image Building and Pushing
```bash
# Build and push all images to Docker Hub
./scripts/build-and-push-images.sh <dockerhub-username>
```

### Configuration
Update `charts/todo-app/values.yaml` with production values:
- Docker image repositories
- Resource limits and requests
- Replica counts
- External service configurations

### Deployment
```bash
# Deploy with custom values
helm upgrade --install todo-app-prod charts/todo-app/ \
  --namespace todo-app-prod \
  --create-namespace \
  --values charts/todo-app/values-prod.yaml
```

## Monitoring

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

# Check Dapr sidecars in application
kubectl get pods -n <namespace> -L dapr.io/app-id
```

### Service Logs
```bash
# View application logs
kubectl logs -l app=backend -n <namespace>
kubectl logs -l app=frontend -n <namespace>
kubectl logs -l app=notification-service -n <namespace>
kubectl logs -l app=recurring-task-service -n <namespace>
```

## Troubleshooting

### Common Issues

1. **Dapr Sidecar Not Injected**
   ```bash
   # Check if Dapr is properly installed
   kubectl get pods -n dapr-system

   # Verify annotations in deployment
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. **Kafka Connectivity Issues**
   ```bash
   # Check Kafka pods
   kubectl get pods -l app=kafka

   # Test connectivity from within cluster
   kubectl run test-client --image=confluentinc/cp-kafka:latest --rm -it --restart=Never -- /bin/bash
   ```

3. **Service Discovery Problems**
   ```bash
   # Check services
   kubectl get svc -n <namespace>

   # Test service connectivity
   kubectl run test --image=curlimages/curl --rm -it --restart=Never -- curl -v http://backend-service:8000/health
   ```

4. **Event Processing Delays**
   ```bash
   # Check Kafka topics
   kubectl exec -it <kafka-pod> -- kafka-topics --list --bootstrap-server localhost:9092

   # Check consumer groups
   kubectl exec -it <kafka-pod> -- kafka-consumer-groups --list --bootstrap-server localhost:9092
   ```

### Scaling Services
```bash
# Scale backend service
kubectl scale deployment todo-app-backend --replicas=3 -n <namespace>

# Scale based on CPU utilization
kubectl autoscale deployment todo-app-backend --cpu-percent=70 --min=2 --max=10 -n <namespace>
```

## Cleanup

To remove the deployment:
```bash
# Remove Helm release
helm uninstall todo-app -n <namespace>

# Remove Dapr
dapr uninstall -k

# Clean up volumes (optional)
kubectl delete pvc --all -n <namespace>
```

This completes the deployment of the event-driven Todo application with Dapr and Kafka integration.