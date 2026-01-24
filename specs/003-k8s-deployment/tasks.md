---
description: "Task list for Kubernetes deployment feature"
---

# Tasks: Kubernetes Deployment

**Input**: Design documents from `/specs/003-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Install Minikube with Docker driver
- [X] T002 Install kubectl and Helm
- [X] T003 [P] Install kubectl-ai plugin
- [X] T004 [P] Install Docker AI Agent (Gordon)
- [X] T005 [P] Verify all tools are accessible in PATH

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T006 Initialize Minikube cluster using Docker driver
- [X] T007 [P] Enable Ingress addon for traffic management
- [X] T008 [P] Configure local terminal to use Minikube's Docker daemon
- [X] T009 [P] Create docker/ directory structure for Dockerfiles
- [X] T010 [P] Create k8s/ directory structure for Kubernetes manifests
- [X] T011 [P] Create charts/ directory structure for Helm charts
- [X] T012 [P] Verify Minikube cluster is running and accessible

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Containerize Application Services (Priority: P1) 🎯 MVP

**Goal**: Generate Dockerfiles for both frontend and backend services and build container images

**Independent Test**: The application services can be built into Docker images and run successfully in isolation, accepting traffic and performing their core functions.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Verify Docker AI Agent (Gordon) can generate Dockerfiles
- [X] T014 [P] [US1] Test Docker image builds successfully

### Implementation for User Story 1

- [X] T015 [P] [US1] Generate Multi-stage Dockerfile for Backend (FastAPI + MCP) using Docker AI Agent
- [X] T016 [P] [US1] Generate Production Dockerfile for Frontend (Next.js) using Docker AI Agent
- [X] T017 [US1] Optimize Docker images for security and size
- [X] T018 [US1] Build local backend image with tag todo-backend:v1
- [X] T019 [US1] Build local frontend image with tag todo-frontend:v1
- [X] T020 [US1] Verify Docker images can be run in isolation with proper health checks

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Deploy with AI-Assisted Tools (Priority: P2)

**Goal**: Use AI-driven tools (kubectl-ai, kagent) to generate Kubernetes manifests and Helm charts without manual coding

**Independent Test**: Kubernetes manifests and Helm charts are generated via AI tools and can successfully deploy the application to a local cluster.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T021 [P] [US2] Test kubectl-ai can generate valid Kubernetes manifests
- [X] T022 [P] [US2] Test Helm chart installation works correctly

### Implementation for User Story 2

- [X] T023 [P] [US2] Generate K8s Secrets manifest for sensitive data using kubectl-ai
- [X] T024 [P] [US2] Generate Backend Deployment manifest using kubectl-ai
- [X] T025 [P] [US2] Generate Frontend Deployment manifest using kubectl-ai
- [X] T026 [P] [US2] Generate Backend Service manifest using kubectl-ai
- [X] T027 [P] [US2] Generate Frontend Service manifest using kubectl-ai
- [X] T028 [US2] Create Helm Chart structure using kubectl-ai
- [X] T029 [US2] Configure values.yaml for environment variables and ports
- [X] T030 [US2] Update Helm chart templates with generated manifests

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Maintain External Connectivity (Priority: P3)

**Goal**: Ensure the chatbot can run inside Kubernetes cluster while maintaining connectivity to external Neon PostgreSQL database and OpenAI APIs

**Independent Test**: The deployed application can successfully connect to Neon PostgreSQL and OpenAI APIs and perform its core functions.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T031 [P] [US3] Test connectivity to external Neon PostgreSQL from within cluster
- [X] T032 [P] [US3] Test connectivity to OpenAI APIs from within cluster

### Implementation for User Story 3

- [X] T033 [P] [US3] Create K8s Secrets for DATABASE_URL and OPENAI_API_KEY
- [X] T034 [US3] Configure backend deployment to use external database connection
- [X] T035 [US3] Configure backend deployment to use OpenAI API key
- [X] T036 [US3] Verify service-to-service communication via K8s DNS
- [X] T037 [US3] Test end-to-end functionality with external services

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Deployment & Orchestration

**Goal**: Deploy the application to Kubernetes and verify everything works together

- [X] T038 Deploy Application using Helm chart
- [X] T039 Verify Pod Health and readiness
- [X] T040 Expose frontend service externally
- [X] T041 Test complete application flow end-to-end
- [X] T042 Verify AI Integration works with backend via Service DNS

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T043 [P] Update README with Minikube setup instructions
- [X] T044 [P] Documentation updates in docs/
- [X] T045 Code cleanup and refactoring
- [X] T046 Performance optimization across all stories
- [X] T047 [P] Additional unit tests (if requested) in tests/unit/
- [X] T048 Security hardening
- [X] T049 [P] Run quickstart.md validation
- [X] T050 Record 90-second Demo Video showing K8s deployment process

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Deployment & Orchestration (Phase 6)**: Depends on all user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 Docker images
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 Docker images and US2 deployments

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Dockerfiles before image builds
- Image builds before deployments
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Dockerfile generation tasks can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all Dockerfile generation tasks together:
Task: "Generate Multi-stage Dockerfile for Backend (FastAPI + MCP) using Docker AI Agent"
Task: "Generate Production Dockerfile for Frontend (Next.js) using Docker AI Agent"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2 (after Docker images ready)
   - Developer C: User Story 3 (after Docker images and deployments ready)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence