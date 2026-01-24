### Phase 4 Objective: Generate Kubernetes Manifests with `kubectl-ai`

This skill outlines the process for generating Kubernetes YAML manifests using `kubectl-ai` based on high-level descriptions.

#### 1. Generate Backend Deployment
- **Prompt to `kubectl-ai`**: "Create a Kubernetes Deployment named `backend-deployment` with 3 replicas. Use the image `todo-chatbot-backend:v1.0.0`. Expose container port 8000 and set the environment variable `DATABASE_URL` from a secret named `db-credentials` with the key `url`."
- **Output**: A `Deployment.yaml` file.

#### 2. Generate Backend Service
- **Prompt to `kubectl-ai`**: "Create a ClusterIP Service named `backend-service` for the `backend-deployment`. Map port 80 to target port 8000."
- **Output**: A `Service.yaml` file.

#### 3. Generate Frontend Deployment and Service
- **Prompt to `kubectl-ai`**: "Generate a Kubernetes Deployment and a NodePort Service for the frontend. The deployment should be named `frontend-deployment` with 2 replicas using the image `todo-chatbot-frontend:v1.0.0`. The service should be named `frontend-service` and expose port 3000 on the node."
- **Output**: Two YAML files for the frontend deployment and service.

#### 4. Scale Replicas
- **Prompt to `kubectl-ai`**: "Scale the `backend-deployment` to 5 replicas."
- **Action**: `kubectl-ai` will apply the scaling change directly to the cluster.
