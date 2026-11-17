---
title: "Phase 5 Plan Creation"
date: "2026-01-31"
stage: "plan"
id: "phase5-plan-2026-01-31-001"
feature: "advanced-task-features"
---

# Phase 5 Plan Creation

## Summary
Created the implementation plan for Phase 5 - Advanced Intelligence & Cloud-Native Deployment, focusing on recurring tasks, real-time reminders, and containerized deployment.

## PROMPT_TEXT
```
# Implementation Plan: Phase 5 - Advanced Intelligence & Cloud-Native Deployment

## 1. Project Background & Intent
We are transitioning from a local Kubernetes setup (Phase 4) to a production-ready, cloud-native AI Todo App. This plan focuses on implementing advanced backend logic for recurring tasks/reminders, migrating to Neon Serverless DB, and full containerization for Docker Desktop and Minikube.

## 2. Technical Strategy
- **Database**: Switch from local PostgreSQL to **Neon Serverless DB**. Implement schema migrations to add fields for recurrence and reminders.
- **Containerization**: Build production-grade Docker images for both Frontend and Backend.
- **Orchestration**: Orchestrate services using Minikube with optimized resource limits.
- **AI Agent**: Strengthen the system prompt to handle natural language scheduling.

## 3. Step-by-Step Execution Plan

### Step 1: Database Migration & Schema Update
- Update `src/database.py` with the provided Neon DB connection string.
- Create a new Alembic migration to add:
    - `is_recurring`: Boolean
    - `recurring_interval`: String (e.g., "daily", "weekly")
    - `reminder_at`: DateTime (with timezone)
- **Goal**: Verify connectivity and schema integrity on Neon DB.

### Step 2: Advanced Task Logic (Backend)
- Implement a background scheduler (e.g., `APScheduler`) in the FastAPI backend.
- Logic for **Recurring Tasks**: When a task is marked 'complete', automatically create a new task with the next due date based on the interval.
- Logic for **Reminders**: A background worker to check for tasks where `reminder_at` matches current time and send notifications (mock or console-based for now).

### Step 3: Dockerization (Docker Desktop)
- Create `backend/Dockerfile`: Multi-stage build for Python 3.13.
- Create `frontend/Dockerfile`: Multi-stage build for Next.js 16.
- Create `docker-compose.yml` to run the full stack (Frontend, Backend) locally for testing before K8s deployment.

### Step 4: Kubernetes Orchestration (Minikube)
- Refine manifests in `k8s/`:
    - `backend-deployment.yaml`: Include environment variables for Neon DB and AI API keys.
    - `frontend-deployment.yaml`: Ensure it points to the backend service.
- Deploy to Minikube using `kubectl apply -f k8s/`.
- Document commands in `specs/004-phase-5-deployment/01-deployment-guide.md`.

### Step 5: AI Integration Enhancement
- Update the AI Agent prompt in `backend/src/agent/runner.py`.
- Add tools for the AI to "Schedule Reminder" and "Set Recurring Pattern".
- Test natural language inputs like: "Add a gym task for every Monday at 8 AM and remind me 10 mins before."

## 4. Verification & Testing
- **Persistence**: Verify tasks are saved in Neon DB.
- **Recurrence**: Complete a daily task and verify a new one is created for tomorrow.
- **Deployment**: `kubectl get pods` must show all pods running without `ImagePullBackOff`.

## 5. Folders & Governance
- Plan and progress to be tracked in:
    - `specs/004-phase-5-deployment/plan.md`
    - `history/prompts/004-phase-5-deployment/`

/sp.plan --phase 5 --depl
```

## RESPONSE_TEXT
Created a comprehensive implementation plan for Phase 5 with the following deliverables:
- Implementation plan document (plan.md) with technical context, constitution check, and roadmap
- Research document (research.md) with findings on Neon DB, background schedulers, and reminder mechanisms
- Data model document (data-model.md) with extended Task entity and new RecurringPatterns entity
- API contract (task-api-v1.yaml) with endpoints for recurring tasks and reminders
- Quickstart guide (quickstart.md) with setup and deployment instructions
All components follow the specification and prepare for implementation of advanced features.