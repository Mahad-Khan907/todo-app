<!--
SYNC IMPACT REPORT:
- Version change: 1.3.0 → 2.0.0
- Modified sections: Project Overview, Technical Stack, Core Rules, Implementation Workflow
- Added sections: Containerization Requirements, Orchestration Requirements, AIOps Integration
- Templates requiring updates: ⚠ plan-template.md, ⚠ spec-template.md, ⚠ tasks-template.md
- Follow-up TODOs: None
-->

# Project Constitution: Todo AI Chatbot (Phase 4)

## Project Overview

### Project Mission
This project is an evolution of a Todo Web App. Phase 3 (AI Chatbot with MCP Integration) is COMPLETE. Phase 4 focuses on transitioning the Todo AI Chatbot into a Cloud-Native application using containerization, Kubernetes orchestration, and AIOps tools. The engineer acts as a "System Architect," using AI to build complex software without writing boilerplate code.

## Technical Stack (Phase 4 Integration)

### Containerization
- **Container Runtime**: Docker (Docker Desktop)
- **Docker AI**: Docker AI Agent (Gordon) for AI-assisted container operations
- **Image Management**: Automated container builds with multi-stage Dockerfiles for both frontend and backend

### Orchestration
- **Platform**: Kubernetes via Minikube (local cluster)
- **Package Management**: Helm Charts for deployment packaging
- **Cluster Management**: kubectl-ai and Kagent for AI-assisted Kubernetes operations

### Backend (API Layer)
- **Runtime**: Python 3.13+
- **Management**: `uv` (Mandatory for environments and dependencies)
- **Framework**: FastAPI (High-performance REST API)
- **AI Logic**: OpenAI Agents SDK + Official MCP SDK
- **MCP Server**: Integrated into FastAPI to expose Task operations as tools
- **Database**: Neon Serverless PostgreSQL (SQLModel ORM)
- **Auth**: JWT-based security using `python-jose` - AI must be protected by existing auth

### Frontend (UI Layer)
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript (Strict typing)
- **Styling**: Tailwind CSS (Premium Dark Theme) + Shadcn/UI
- **State**: TanStack Query (Server-state management)
- **Auth**: Better Auth integration
- **AI Interface**: OpenAI ChatKit integrated into the existing Dashboard theme

## Phase 4 Core Rules

### 1. Spec-Driven Development
- Every feature must have a Markdown Constitution and Spec before implementation
- New specifications must be stored in `specs/004-kubernetes-deployment/`
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

### 5. Local Cluster Deployment
- The system must be deployed locally on Minikube
- All services must be orchestrated via Kubernetes
- Service discovery and networking must follow Kubernetes patterns

### 6. Conversational Interface Preservation
- The chatbot must maintain its functionality via the OpenAI Agents SDK and MCP server
- Existing AI capabilities must remain intact after containerization
- Authentication and security layers must be preserved

## Containerization Requirements

Phase 4 requires containerization of all services:
- `backend/Dockerfile`: Multi-stage build for FastAPI service
- `frontend/Dockerfile`: Multi-stage build for Next.js application
- Proper health checks and startup scripts for containerized services
- Environment-specific configurations for different deployment targets

## Orchestration Requirements

Phase 4 requires Kubernetes manifests:
- `k8s/backend-deployment.yaml`: Backend service deployment
- `k8s/frontend-deployment.yaml`: Frontend service deployment
- `k8s/services.yaml`: Service definitions for inter-service communication
- `k8s/configmaps-secrets.yaml`: Configuration and secret management
- `k8s/ingress.yaml`: Ingress configuration for external access

## AIOps Integration

Phase 4 leverages AI-assisted operations:
- Helm chart generation via kubectl-ai
- Automated deployment through Kagent
- AI-assisted troubleshooting and scaling recommendations
- Intelligent resource allocation and optimization

## Implementation Workflow (Spec-Driven)

### 1. Specify
Create `/specs/004-kubernetes-deployment/spec.md` for containerization and orchestration requirements.

### 2. Plan
Generate `/specs/004-kubernetes-deployment/plan.md` for Kubernetes implementation roadmap.

### 3. Tasks
Generate `/specs/004-kubernetes-deployment/tasks.md` for granular implementation checklist.

## Repository Standards

### Documentation Requirements
- The repo must contain a `/specs` folder with all historical specification files
- Each phase must have its own subdirectory in `/specs/`
- All architectural decisions must be documented in ADRs

### Claude Instructions
- A `CLAUDE.md` file must be present with specific instructions for Claude
- Instructions must reflect Phase 4 requirements and constraints
- AI tools must be properly configured for containerization and orchestration tasks

## Operational Rules & "No Error" Policy

### Development Standards
- **Cloud-Native Architecture**: Strictly follow containerization and microservices patterns
- **Dependency Isolation**: All container build dependencies must be managed via Docker. Never use global installations for container builds.
- **Validation**: Every feature must pass a `/sp.specify` check before implementation to ensure no logical gaps.
- **Error-Free Code**: Claude must verify Dockerfiles, Kubernetes manifests, and Helm charts before delivery to prevent deployment failures.
- **AI Integration**: All containerization and orchestration must leverage AIOps tools as mandated by Core Rules.

### CLI Commands
- `/sp.constitution`: Update project rules.
- `/sp.specify`: Generate or refine feature requirements.
- `/sp.plan`: Create a technical roadmap.
- `/sp.tasks`: Generate a granular checklist for implementation.
- `/sp.implement`: Execute code generation based on tasks.
- `/sp.adr`: Document architecturally significant decisions.
- `/sp.analyze`: Perform cross-artifact consistency analysis.

## Governance
All development must strictly adhere to this constitution to ensure alignment with cloud-native requirements. Constitution supersedes all other practices. All code generation must follow spec-driven development principles using Claude Code and Spec-Kit Plus tools. All deployments must verify compliance with containerization and orchestration principles. AI-native features must leverage MCP tools and OpenAI Agents SDK as mandated by the Core Rules.

**Version**: 2.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-18