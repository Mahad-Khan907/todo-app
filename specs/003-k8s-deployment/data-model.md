# Data Model: Kubernetes Deployment

**Feature**: Kubernetes Deployment
**Date**: 2026-01-18
**Author**: Claude Code

## Overview

This document describes the data structures and entities relevant to the Kubernetes deployment of the Todo AI Chatbot application. Since this feature focuses on infrastructure and deployment, the primary data models are configuration and deployment entities.

## Kubernetes Entities

### 1. Container Image

**Description**: Represents a packaged application with its dependencies for consistent deployment across environments

**Fields**:
- `name`: String - Name of the image (e.g., "todo-backend", "todo-frontend")
- `tag`: String - Version tag for the image (e.g., "v1.0.0", "latest")
- `registry`: String - Registry location (optional, defaults to local/minikube registry)
- `size`: Integer - Size of the image in MB
- `layers`: Array - List of layers in the image
- `build_context`: String - Path to the build context

**Relationships**:
- One Pod can contain multiple Container Images
- Referenced by Deployment entities

**Validation rules**:
- Name must follow Docker naming conventions
- Tag must follow semantic versioning or "latest"
- Size should be minimized for security and efficiency

### 2. Kubernetes Pod

**Description**: The smallest deployable unit that contains one or more containers and shared storage/network resources

**Fields**:
- `name`: String - Unique name of the pod
- `namespace`: String - Kubernetes namespace (defaults to "default")
- `containers`: Array - List of container images to run in the pod
- `init_containers`: Array - Optional init containers to run before main containers
- `volumes`: Array - Volumes to mount in the pod
- `labels`: Map - Key-value pairs for organizing and selecting resources
- `annotations`: Map - Non-identifying metadata for tooling
- `node_selector`: Map - Constraints for which nodes the pod can run on
- `resources`: Object - CPU and memory requests/limits

**Relationships**:
- Belongs to a Deployment
- Exposes ports via Service entities
- Mounted volumes may connect to PersistentVolumeClaim

**Validation rules**:
- Name must be unique within namespace
- Must have at least one container
- Resource requests/limits should be defined for production

### 3. Kubernetes Service

**Description**: An abstraction that defines a logical set of Pods and a policy for accessing them

**Fields**:
- `name`: String - Unique name of the service
- `namespace`: String - Kubernetes namespace (defaults to "default")
- `selector`: Map - Labels to select the pods to expose
- `ports`: Array - List of ports to expose
- `type`: Enum - Service type (ClusterIP, NodePort, LoadBalancer, ExternalName)
- `cluster_ip`: String - IP address allocated by Kubernetes (for ClusterIP type)
- `external_ips`: Array - IPs for clients to access the service

**Relationships**:
- Selects multiple Pods based on labels
- May be exposed externally via Ingress
- Connects frontend to backend services

**Validation rules**:
- Name must be unique within namespace
- Must have at least one port defined
- Selector must match actual pod labels

### 4. Kubernetes Secret

**Description**: A way to store sensitive information such as passwords, OAuth tokens, and SSH keys

**Fields**:
- `name`: String - Unique name of the secret
- `namespace`: String - Kubernetes namespace (defaults to "default")
- `type`: String - Type of secret (Opaque, kubernetes.io/service-account-token, etc.)
- `data`: Map - Base64 encoded key-value pairs of sensitive data
- `string_data`: Map - Unencoded key-value pairs (encoded at creation time)

**Relationships**:
- Referenced by Deployments to inject sensitive data
- May be mounted as volumes or environment variables

**Validation rules**:
- Name must be unique within namespace
- Data must be base64 encoded for the data field
- Should not exceed 1MB in size

## Configuration Entities

### 5. Helm Chart

**Description**: A package of pre-configured Kubernetes resources that can be deployed as a unit

**Fields**:
- `name`: String - Name of the chart
- `version`: String - Semantic version of the chart
- `app_version`: String - Version of the application contained in the chart
- `description`: String - Brief description of the chart
- `dependencies`: Array - List of chart dependencies
- `maintainers`: Array - Maintainer contact information
- `values`: Map - Default configuration values
- `templates`: Array - List of Kubernetes manifest templates

**Relationships**:
- Contains multiple Kubernetes resource templates
- Values can be overridden during installation
- May depend on other charts

**Validation rules**:
- Name should follow DNS-1123 label standard
- Version must follow semantic versioning
- Templates must be valid Kubernetes manifests with proper templating

### 6. Deployment Configuration

**Description**: Configuration parameters for deploying the application to Kubernetes

**Fields**:
- `replicas`: Integer - Number of pod replicas to maintain
- `image_pull_policy`: String - When to pull container images (Always, IfNotPresent, Never)
- `environment`: Map - Environment variables to inject into containers
- `secrets`: Map - References to Kubernetes secrets to mount
- `resource_limits`: Object - CPU and memory limits per container
- `resource_requests`: Object - CPU and memory requests per container
- `health_checks`: Object - Liveness and readiness probe configurations
- `security_context`: Object - Security settings for the pod/container

**Relationships**:
- Maps to Kubernetes Deployment resources
- References ConfigMaps and Secrets
- Defines resource requirements for Pods

**Validation rules**:
- Replicas must be >= 0
- Resource requests should not exceed limits
- Health check timeouts must be reasonable

## State Transitions

### Pod Lifecycle States
1. Pending → Pod accepted by Kubernetes, containers not yet running
2. Running → Pod bound to a node, all containers running
3. Succeeded → All containers terminated successfully
4. Failed → At least one container terminated with failure
5. Unknown → Status could not be obtained

### Deployment States
1. Progressing → Deployment is rolling out changes
2. Complete → Deployment successfully rolled out
3. Failed → Deployment failed to rollout
4. Paused → Deployment is paused and will not process updates

## API Endpoints Mapping

The following API endpoints from the original application will be accessible through the Kubernetes services:

- `/api/chat` → Chat endpoint for the AI chatbot functionality
- `/api/tasks` → Task management endpoints
- `/api/auth` → Authentication endpoints
- `/health` → Health check endpoint

These will be accessible via the frontend service and routed to the backend service using Kubernetes DNS resolution (e.g., `backend-service:8000`).