# Helm Chart for Todo AI Chatbot

This Helm chart deploys the Todo AI Chatbot application to Kubernetes.

## Overview

The Todo AI Chatbot is a microservices application consisting of:
- Backend: FastAPI application
- Frontend: Next.js application
- External dependencies: Neon PostgreSQL and OpenAI APIs

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
helm install my-release charts/todo-app \
  --set database.url="your-neon-db-url" \
  --set openai.apiKey="your-openai-api-key"
```

## Uninstalling the Chart

To uninstall the `my-release` deployment:

```bash
helm delete my-release
```

## Configuration

The following table lists the configurable parameters of the todo-app chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of application replicas | `1` |
| `image.backend.repository` | Backend image repository | `todo-backend` |
| `image.backend.tag` | Backend image tag | `v1` |
| `image.frontend.repository` | Frontend image repository | `todo-frontend` |
| `image.frontend.tag` | Frontend image tag | `v1` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Service type | `LoadBalancer` |
| `service.backendPort` | Backend service port | `8000` |
| `service.frontendPort` | Frontend service port | `3000` |
| `resources.requests.cpu` | CPU resource requests | `100m` |
| `resources.requests.memory` | Memory resource requests | `128Mi` |
| `resources.limits.cpu` | CPU resource limits | `500m` |
| `resources.limits.memory` | Memory resource limits | `512Mi` |
| `database.url` | Neon PostgreSQL database URL | `""` |
| `openai.apiKey` | OpenAI API key | `""` |

## Customizing the Chart

You can create a custom `values.yaml` file to override the default values:

```yaml
replicaCount: 2

image:
  backend:
    repository: my-backend-image
    tag: latest
  frontend:
    repository: my-frontend-image
    tag: latest

service:
  type: ClusterIP
  backendPort: 8000
  frontendPort: 3000

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 200m
    memory: 256Mi

database:
  url: "postgresql://user:pass@neon-host.region.aws.neon.tech/dbname"

openai:
  apiKey: "sk-..."
```

Then install using:

```bash
helm install my-release charts/todo-app -f values.yaml
```

## Secrets Management

The chart creates Kubernetes secrets for sensitive information:
- Database URL is stored in a secret named `<release-name>-db-secret`
- OpenAI API key is stored in a secret named `<release-name>-openai-secret`

## Verifying Installation

After installation, verify the pods are running:

```bash
kubectl get pods
```

Check the services are created:

```bash
kubectl get services
```

View the status of the Helm release:

```bash
helm status my-release
```