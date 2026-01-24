# Docker Configuration for Todo AI Chatbot

This directory contains Dockerfiles for containerizing the Todo AI Chatbot application.

## Overview

The Todo AI Chatbot consists of two main services:
- **Backend**: FastAPI application serving the API
- **Frontend**: Next.js application serving the UI

## Dockerfiles

### Backend Dockerfile (`backend.Dockerfile`)
- Multi-stage build for optimized image size
- Uses Python 3.13-slim as base image
- Includes build stage for compiling dependencies
- Implements security best practices (non-root user)
- Includes health checks

### Frontend Dockerfile (`frontend.Dockerfile`)
- Multi-stage build for optimized image size
- Uses Node.js 20-alpine as base image
- Implements standalone server deployment
- Includes proper signal handling with dumb-init
- Implements security best practices (non-root user)
- Includes health checks

## Building Images

To build the Docker images locally:

```bash
# Build backend image
docker build -f docker/backend.Dockerfile -t todo-backend:v1 .

# Build frontend image
docker build -f docker/frontend.Dockerfile -t todo-frontend:v1 .
```

## Environment Variables

The containers expect the following environment variables:

### Backend
- `DATABASE_URL`: Connection string for Neon PostgreSQL database
- `OPENAI_API_KEY`: API key for OpenAI services

### Frontend
- `NEXT_PUBLIC_BACKEND_URL`: URL of the backend service

## Security Features

- Non-root user execution
- Minimal base images
- Multi-stage builds to reduce attack surface
- Proper resource limits
- Health checks for monitoring

## Kubernetes Integration

These Docker images are designed to work with the Kubernetes manifests in the `k8s/` directory and the Helm chart in the `charts/` directory.