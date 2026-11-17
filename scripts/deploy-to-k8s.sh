#!/bin/bash

# Script to deploy the Todo application to Kubernetes with Dapr
# Usage: ./deploy-to-k8s.sh <dockerhub_username>

set -e  # Exit on any error

DOCKERHUB_USERNAME=$1

if [ -z "$DOCKERHUB_USERNAME" ]; then
    echo "Usage: $0 <dockerhub_username>"
    echo "Example: $0 mydockerhubusername"
    exit 1
fi

echo "Deploying Todo application to Kubernetes with Dapr..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    echo "Helm is not installed. Please install Helm 3.x first."
    exit 1
fi

# Check if Dapr is initialized
if ! kubectl get pods -n dapr-system &> /dev/null; then
    echo "Dapr is not initialized in Kubernetes. Initializing Dapr..."
    dapr init -k
fi

# Create namespace if it doesn't exist
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Update Helm dependencies
helm dependency update charts/todo-app/

# Deploy the application using Helm
echo "Deploying application with Helm..."
helm upgrade --install todo-app charts/todo-app/ \
    --namespace todo-app \
    --set images.backend.repository=$DOCKERHUB_USERNAME/todo-backend \
    --set images.backend.tag=v1 \
    --set images.frontend.repository=$DOCKERHUB_USERNAME/todo-frontend \
    --set images.frontend.tag=v1 \
    --set images.notification.repository=$DOCKERHUB_USERNAME/todo-notification-service \
    --set images.notification.tag=v1 \
    --set images.recurring.repository=$DOCKERHUB_USERNAME/todo-recurring-task-service \
    --set images.recurring.tag=v1 \
    --create-namespace

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=dapr-backend --timeout=300s -n todo-app
kubectl wait --for=condition=ready pod -l app=dapr-frontend --timeout=300s -n todo-app
kubectl wait --for=condition=ready pod -l app=notification-service --timeout=300s -n todo-app
kubectl wait --for=condition=ready pod -l app=recurring-task-service --timeout=300s -n todo-app

echo "Deployment completed successfully!"
echo ""
echo "Services:"
kubectl get svc -n todo-app
echo ""
echo "Pods:"
kubectl get pods -n todo-app
echo ""
echo "Dapr sidecars:"
kubectl get pods -n todo-app -L dapr.io/app-id
echo ""
echo "To access the frontend:"
echo "kubectl port-forward svc/todo-app-frontend-service 3000:3000 -n todo-app"
echo ""
echo "To check logs:"
echo "kubectl logs -l app=backend -n todo-app"
echo "kubectl logs -l app=frontend -n todo-app"
echo "kubectl logs -l app=notification-service -n todo-app"
echo "kubectl logs -l app=recurring-task-service -n todo-app"