#!/bin/bash

# Script to build and push Docker images to Docker Hub
# Usage: ./build-and-push-images.sh <dockerhub_username>

set -e  # Exit on any error

DOCKERHUB_USERNAME=$1

if [ -z "$DOCKERHUB_USERNAME" ]; then
    echo "Usage: $0 <dockerhub_username>"
    echo "Example: $0 mydockerhubusername"
    exit 1
fi

echo "Building and pushing Docker images for user: $DOCKERHUB_USERNAME"

# Login to Docker Hub
echo "Logging into Docker Hub..."
docker login

# Build and push backend image
echo "Building backend image..."
docker build -f docker/backend.Dockerfile -t $DOCKERHUB_USERNAME/todo-backend:v1 .
docker tag $DOCKERHUB_USERNAME/todo-backend:v1 $DOCKERHUB_USERNAME/todo-backend:latest
echo "Pushing backend image..."
docker push $DOCKERHUB_USERNAME/todo-backend:v1
docker push $DOCKERHUB_USERNAME/todo-backend:latest

# Build and push frontend image
echo "Building frontend image..."
docker build -f docker/frontend.Dockerfile -t $DOCKERHUB_USERNAME/todo-frontend:v1 .
docker tag $DOCKERHUB_USERNAME/todo-frontend:v1 $DOCKERHUB_USERNAME/todo-frontend:latest
echo "Pushing frontend image..."
docker push $DOCKERHUB_USERNAME/todo-frontend:v1
docker push $DOCKERHUB_USERNAME/todo-frontend:latest

# Build and push notification service image
echo "Building notification service image..."
docker build -f docker/notification.Dockerfile -t $DOCKERHUB_USERNAME/todo-notification-service:v1 .
docker tag $DOCKERHUB_USERNAME/todo-notification-service:v1 $DOCKERHUB_USERNAME/todo-notification-service:latest
echo "Pushing notification service image..."
docker push $DOCKERHUB_USERNAME/todo-notification-service:v1
docker push $DOCKERHUB_USERNAME/todo-notification-service:latest

# Build and push recurring task service image
echo "Building recurring task service image..."
docker build -f docker/recurring-task.Dockerfile -t $DOCKERHUB_USERNAME/todo-recurring-task-service:v1 .
docker tag $DOCKERHUB_USERNAME/todo-recurring-task-service:v1 $DOCKERHUB_USERNAME/todo-recurring-task-service:latest
echo "Pushing recurring task service image..."
docker push $DOCKERHUB_USERNAME/todo-recurring-task-service:v1
docker push $DOCKERHUB_USERNAME/todo-recurring-task-service:latest

echo "All images have been built and pushed to Docker Hub!"
echo "Images:"
echo "  - $DOCKERHUB_USERNAME/todo-backend:v1"
echo "  - $DOCKERHUB_USERNAME/todo-frontend:v1"
echo "  - $DOCKERHUB_USERNAME/todo-notification-service:v1"
echo "  - $DOCKERHUB_USERNAME/todo-recurring-task-service:v1"

echo ""
echo "To deploy with Helm, update your values.yaml with your Docker Hub images:"
echo "images:"
echo "  backend:"
echo "    repository: $DOCKERHUB_USERNAME/todo-backend"
echo "    tag: v1"
echo "  frontend:"
echo "    repository: $DOCKERHUB_USERNAME/todo-frontend"
echo "    tag: v1"
echo "  notification:"
echo "    repository: $DOCKERHUB_USERNAME/todo-notification-service"
echo "    tag: v1"
echo "  recurring:"
echo "    repository: $DOCKERHUB_USERNAME/todo-recurring-task-service"
echo "    tag: v1"