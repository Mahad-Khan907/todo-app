<!--
SYNC IMPACT REPORT:
- Version change: 2.0.0 → 2.1.0
- Modified sections: Project Overview, Technical Stack, Core Rules
- Added sections: Recurring Tasks & Real-time Features, AI System Prompt Enhancement, Phase 5 Specific Structure
- Templates requiring updates: ⚠ plan-template.md, ⚠ spec-template.md, ⚠ tasks-template.md
- Follow-up TODOs: None
-->

# Project Constitution: Todo AI Chatbot (Phase 5)

## Project Overview

### Project Mission
This project is an evolution of a Todo Web App. Phase 4 (Cloud-Native Deployment with Kubernetes) is COMPLETE. Phase 5 focuses on implementing advanced features including **Recurring Tasks**, **Real-time Reminders**, **Enhanced AI Capabilities**, and full cloud-native deployment using containerization, Kubernetes orchestration, and AIOps tools. The engineer acts as a "System Architect," using AI to build complex software without writing boilerplate code.

## Technical Stack (Phase 5 Integration)

### Containerization
- **Container Runtime**: Docker (Docker Desktop)
- **Docker AI**: Docker AI Agent (Gordon) for AI-assisted container operations
- **Image Management**: Automated container builds with multi-stage Dockerfiles for both frontend and backend
- **Orchestration Platform**: Kubernetes via Minikube (local cluster)
- **Package Management**: Helm Charts for deployment packaging
- **Cluster Management**: kubectl-ai and Kagent for AI-assisted Kubernetes operations

### Backend (API Layer)
- **Runtime**: Python 3.13+
- **Management**: `uv` (Mandatory for environments and dependencies)
- **Framework**: FastAPI (High-performance REST API)
- **AI Logic**: OpenAI Agents SDK + Official MCP SDK
- **MCP Server**: Integrated into FastAPI to expose Task operations as tools
- **Database**: Neon Serverless PostgreSQL (SQLModel ORM) with recurring tasks and reminder fields
- **Background Processing**: APScheduler or similar for triggering reminders and recurring tasks
- **Auth**: JWT-based security using `python-jose` - AI must be protected by existing auth

### Frontend (UI Layer)
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript (Strict typing)
- **Styling**: Tailwind CSS (Premium Dark Theme) + Shadcn/UI
- **State**: TanStack Query (Server-state management)
- **Auth**: Better Auth integration
- **AI Interface**: OpenAI ChatKit integrated into the existing Dashboard theme with enhanced notification capabilities

## Phase 5 Core Rules

### 1. Spec-Driven Development
- Every feature must have a Markdown Constitution and Spec before implementation
- New specifications must be stored in `specs/004-phase-5-deployment/`
- All changes must follow the refinement loop until correct output is generated

### 2. No Manual Coding Constraint
- Code or configuration (Dockerfiles, YAMLs) must not be written manually
- Dockerfiles, Kubernetes manifests, and Helm charts must be generated using AI tools
- All containerization and orchestration files must be AI-generated

### 3. AIOps Implementation
- You must use kubectl-ai and kagent to generate Helm charts and manage the local cluster
- All Kubernetes operations must leverage AI-assisted tools
- Deployment configurations must be managed through AIOps tools

### 4. Containerization Requirements
- Both the frontend (Next.js) and backend (FastAPI/MCP) must be containerized
- Separate containers for frontend and backend services
- Proper environment variable management for containerized applications
- Production-ready Dockerfiles for both services using multi-stage builds

### 5. Local Cluster Deployment
- The system must be deployed locally on Minikube
- All services must be orchestrated via Kubernetes
- Service discovery and networking must follow Kubernetes patterns
- Services configured for Minikube (NodePort/LoadBalancer)

### 6. Advanced Features Implementation
- **Recurring Tasks**: Implement recurring_interval field in database model
- **Real-time Reminders**: Implement reminder_at and last_notified fields
- **Background Worker**: Implement APScheduler or similar for triggering reminders and recurring task instances
- **Enhanced AI**: Update AI system prompt to handle recurrence parsing and immediate scheduling

### 7. Conversational Interface Enhancement
- The chatbot must maintain its functionality via the OpenAI Agents SDK and MCP server
- Enhanced AI capabilities for proactive task management
- Updated system prompt to handle "Every Friday at 5 PM" (Recurrence parsing) and "Remind me in 10 minutes" (Immediate scheduling)
- AI must check reminder_at field and proactively notify user via chat UI

## Recurring Tasks & Real-time Features

Phase 5 requires database schema updates:
- Update `src/database.py` to support Neon DB connection strings
- Run Alembic migrations to add: `recurring_interval`, `reminder_at`, and `last_notified` fields
- Implement background worker within backend container to trigger reminders and generate recurring task instances
- Ensure proper timezone handling for recurring tasks and reminders

## AI System Prompt Enhancement

Phase 5 requires AI system prompt updates:
- Handle recurrence patterns: "Every Friday at 5 PM" (Recurrence parsing)
- Handle immediate scheduling: "Remind me in 10 minutes" (Immediate scheduling)
- Proactive notification via chat UI when reminder_at timestamp is reached
- Maintain existing task management capabilities while adding new features

## Phase 5 Specific Structure

### Specs Directory
- Create `specs/004-phase-5-deployment/` for all new functional specs

### History Directory
- Create `history/prompts/004-phase-5-deployment/` to log every step of the deployment and feature addition

### Deployment Spec
- Create `specs/004-phase-5-deployment/01-deployment-spec.md` for deployment requirements

## Implementation Workflow (Spec-Driven)

### 1. Specify
Create `/specs/004-phase-5-deployment/spec.md` for advanced features and deployment requirements.

### 2. Plan
Generate `/specs/004-phase-5-deployment/plan.md` for advanced features and Kubernetes implementation roadmap.

### 3. Tasks
Generate `/specs/004-phase-5-deployment/tasks.md` for granular implementation checklist.

## Repository Standards

### Documentation Requirements
- The repo must contain a `/specs` folder with all historical specification files
- Each phase must have its own subdirectory in `/specs/`
- All architectural decisions must be documented in ADRs
- Deployment artifacts must be organized in `k8s/` and `charts/` directories

### Claude Instructions
- A `CLAUDE.md` file must be present with specific instructions for Claude
- Instructions must reflect Phase 5 requirements and constraints
- AI tools must be properly configured for containerization, orchestration, and advanced feature implementation tasks

## Operational Rules & "No Error" Policy

### Development Standards
- **Cloud-Native Architecture**: Strictly follow containerization and microservices patterns
- **Dependency Isolation**: All container build dependencies must be managed via Docker. Never use global installations for container builds.
- **Validation**: Every feature must pass a `/sp.specify` check before implementation to ensure no logical gaps.
- **Error-Free Code**: Claude must verify Dockerfiles, Kubernetes manifests, and Helm charts before delivery to prevent deployment failures.
- **AI Integration**: All containerization and orchestration must leverage AIOps tools as mandated by Core Rules.
- **Feature Completeness**: All advanced features (recurring tasks, reminders) must be fully implemented and tested before deployment.

### CLI Commands
- `/sp.constitution`: Update project rules.
- `/sp.specify`: Generate or refine feature requirements.
- `/sp.plan`: Create a technical roadmap.
- `/sp.tasks`: Generate a granular checklist for implementation.
- `/sp.implement`: Execute code generation based on tasks.
- `/sp.adr`: Document architecturally significant decisions.
- `/sp.analyze`: Perform cross-artifact consistency analysis.

## Governance
All development must strictly adhere to this constitution to ensure alignment with cloud-native requirements and advanced feature implementation. Constitution supersedes all other practices. All code generation must follow spec-driven development principles using Claude Code and Spec-Kit Plus tools. All deployments must verify compliance with containerization, orchestration, and advanced feature requirements. AI-native features must leverage MCP tools and OpenAI Agents SDK as mandated by the Core Rules.

**Version**: 2.1.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-31