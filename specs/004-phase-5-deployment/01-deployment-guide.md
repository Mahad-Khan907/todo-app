# Phase 5 Deployment Guide

## Overview
This guide provides instructions for deploying the Todo AI Chatbot application with advanced features (recurring tasks and reminders) using Docker and Kubernetes.

## Prerequisites

### System Requirements
- Docker Desktop (with Kubernetes enabled) or standalone Docker
- Minikube installed and running
- kubectl command-line tool
- Git for version control

### Account Requirements
- Neon Serverless PostgreSQL account with a database created
- OpenAI API key for AI agent functionality

## Environment Setup

### 1. Set Up Environment Variables
Ensure your `.env` file in the project root contains your credentials:

```bash
# .env
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 2. Encode Secrets for Kubernetes
Before deploying to Kubernetes, you need to encode your sensitive data:

```bash
# Encode your database URL
echo -n 'postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require' | base64

# Encode your OpenAI API key
echo -n 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' | base64
```

Update the `k8s/secrets.yaml` file with these encoded values.

## Docker Deployment

### 1. Build Docker Images
```bash
# Build backend image
docker build -f docker/backend.Dockerfile -t todo-backend:v1 .

# Build frontend image
docker build -f docker/frontend.Dockerfile -t todo-frontend:v1 .
```

### 2. Run with Docker Compose (Local Development)
```bash
# Start the services
docker-compose up -d
```

### 3. Verify Local Deployment
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Health check: `http://localhost:8000/health`

## Kubernetes Deployment

### 1. Start Minikube (if not already running)
```bash
minikube start
```

### 2. Create Kubernetes Secrets
```bash
# Create secret for database (after updating secrets.yaml with encoded values)
kubectl apply -f k8s/secrets.yaml
```

### 3. Deploy to Kubernetes
```bash
# Apply Kubernetes configurations
kubectl apply -f k8s/deployments/backend-deployment.yaml
kubectl apply -f k8s/deployments/frontend-deployment.yaml
kubectl apply -f k8s/services/backend-service.yaml
kubectl apply -f k8s/services/frontend-service.yaml
```

### 4. Verify Kubernetes Deployment
```bash
# Check if pods are running
kubectl get pods

# Check services
kubectl get services

# Check logs for backend
kubectl logs -l app=backend
```

### 5. Access the Application
```bash
# Get the frontend service URL
minikube service frontend-service --url
```

## Advanced Features Configuration

### Recurring Tasks
- Users can create recurring tasks with daily, weekly, or monthly patterns
- The system automatically generates new task instances when recurring tasks are completed
- API endpoints are available for managing recurring tasks

### Reminder System
- Users can set reminders with specific timestamps
- Background worker checks for due reminders every minute
- API endpoints are available for scheduling and managing reminders

## Monitoring and Maintenance

### 1. Check Application Health
```bash
# Check pod status
kubectl get pods

# Check logs
kubectl logs <pod-name>

# Describe pod for detailed information
kubectl describe pod <pod-name>
```

### 2. Scaling the Application
```bash
# Scale backend deployment
kubectl scale deployment backend-deployment --replicas=2

# Scale frontend deployment
kubectl scale deployment frontend-deployment --replicas=2
```

### 3. Resource Utilization
```bash
# Check resource usage
kubectl top pods
```

## Troubleshooting

### Common Issues

#### Pods Not Starting
```bash
# Check pod status
kubectl get pods

# Check pod logs
kubectl logs <pod-name>

# Describe pod for detailed information
kubectl describe pod <pod-name>
```

#### Database Connection Issues
- Verify that your Neon DB connection string is correct
- Check that the secret was created properly: `kubectl get secrets`
- Ensure the database is accessible from the Kubernetes cluster

#### AI Agent Not Responding
- Confirm that your OpenAI API key is valid and has sufficient credits
- Check that the backend logs show successful connection to OpenAI API
- Verify that the AI system prompt was updated correctly

## Cleanup
To remove the deployment:
```bash
# Remove all resources
kubectl delete -f k8s/deployments/
kubectl delete -f k8s/services/
kubectl delete secret db-secret openai-secret

# Stop Minikube
minikube stop
```

## Updating the Application
To update the application with new changes:

1. Rebuild the Docker images with new tags
2. Update the image tags in the Kubernetes deployment files
3. Apply the updated configurations:
   ```bash
   kubectl apply -f k8s/deployments/backend-deployment.yaml
   kubectl apply -f k8s/deployments/frontend-deployment.yaml
   ```
4. The deployments will roll out the new changes automatically

---
**Version**: 1.0
**Date**: 2026-01-31