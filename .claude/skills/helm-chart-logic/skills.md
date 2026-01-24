### Phase 4 Objective: Define Helm Chart Logic for the Todo Chatbot

This skill provides templates and logic for creating a reusable and configurable Helm chart.

#### 1. `Chart.yaml` Template
```yaml
apiVersion: v2
name: todo-chatbot
description: A Helm chart for deploying the Todo Chatbot application on Kubernetes.
type: application
version: 0.1.0
appVersion: "1.0.0"

dependencies:
  - name: frontend
    version: "0.1.0"
    repository: "file://./charts/frontend"
  - name: backend
    version: "0.1.0"
    repository: "file://./charts/backend"
```

#### 2. `values.yaml` Template
```yaml
# Global values
replicaCount: 1

# Frontend specific values
frontend:
  replicaCount: 2
  image:
    repository: todo-chatbot-frontend
    tag: "v1.0.0"
    pullPolicy: IfNotPresent
  service:
    type: NodePort
    port: 3000

# Backend specific values
backend:
  replicaCount: 3
  image:
    repository: todo-chatbot-backend
    tag: "v1.0.0"
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  database:
    url: "postgresql://user:password@host:port/db"
```

#### 3. Template Logic (`backend-deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-backend
spec:
  replicas: {{ .Values.backend.replicaCount | default .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: backend
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
          ports:
            - containerPort: {{ .Values.backend.service.port }}
```
