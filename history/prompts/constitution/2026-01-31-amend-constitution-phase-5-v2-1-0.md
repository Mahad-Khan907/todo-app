---
title: "Amend Constitution Phase 5 v2.1.0"
date: "2026-01-31"
stage: "constitution"
id: "constitution-2026-01-31-001"
---

# Amend Constitution Phase 5 v2.1.0

## Summary
Updated the project constitution to transition to Phase 5 (Final Phase), focusing on implementing recurring tasks, real-time reminders, Neon Serverless Database integration, full containerization with Docker, local orchestration with Minikube, and enhanced AI Agent capabilities for proactive task management.

## PROMPT_TEXT
```
# Phase 5 Constitution: Advanced Features, AI & Cloud-Native Deployment

## 1. Objective & Project State
Transition the project to **Phase 5 (Final Phase)**. This phase focuses on:
- Implementing **Recurring Tasks** and **Real-time Reminders**.
- Integrating **Neon Serverless Database** for cloud persistence.
- Full containerization using **Docker** and local orchestration with **Minikube**.
- Enhancing **AI Agent** capabilities for proactive task management.

## 2. Infrastructure & Containerization (NEW)
- **Dockerization**:
  - Create a production-ready `Dockerfile` for the **Backend** (Python/FastAPI) using multi-stage builds.
  - Create a production-ready `Dockerfile` for the **Frontend** (Next.js/React) to serve static files.
  - Generate a `docker-compose.yml` for local testing on **Docker Desktop**.
- **Minikube & Kubernetes**:
  - Update/Create Kubernetes manifest files in a `k8s/` directory.
  - Ensure services are configured for Minikube (NodePort/LoadBalancer).
  - Use `kubectl` commands to manage pods and deployments.

## 3. Database & Real-time Features
- **Neon DB Migration**:
  - Update `src/database.py` to support Neon DB connection strings.
  - Run Alembic migrations to add: `recurring_interval`, `reminder_at`, and `last_notified`.
- **Logic**: Implement a background worker (or APScheduler) within the backend container to trigger reminders and generate recurring task instances.

## 4. AI System Prompt Strengthening
- Update the AI Agent's system prompt to handle:
  - "Every Friday at 5 PM" (Recurrence parsing).
  - "Remind me in 10 minutes" (Immediate scheduling).
- The AI must check the `reminder_at` field and proactively notify the user via the chat UI.

## 5. Folder & SDD Structure (Phase 5 Specific)
- **Specs Directory**: Create `specs/004-phase-5-deployment/` for all new functional specs.
- **History Directory**: Create `history/prompts/004-phase-5-deployment/` to log every step of the deployment and feature addition.
- **Deployment Spec**: Create `specs/004-phase-5-deployment/01-deployment
```

## RESPONSE_TEXT
Updated the constitution file to version 2.1.0, incorporating all Phase 5 requirements including:
- Recurring tasks and real-time reminders implementation
- Enhanced AI capabilities for proactive task management
- Updated technical stack with background processing capabilities
- New core rules for advanced feature implementation
- Proper repository structure for Phase 5 specifications
- Updated governance to reflect advanced feature requirements