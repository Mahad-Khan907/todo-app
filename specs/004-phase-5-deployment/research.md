# Research Findings: Phase 5 Implementation

## 1. Neon Serverless DB Integration

### Decision
Use standard PostgreSQL connection string format with Neon-specific endpoints

### Rationale
Neon is PostgreSQL-compatible, allowing minimal code changes to the existing application. The connection string format follows the standard PostgreSQL convention with Neon-specific host addresses.

### Alternatives Considered
- Traditional PostgreSQL hosting: Would require managing infrastructure
- Other serverless DBs: Would require changing database drivers and code

### Implementation Details
Connection string format: `postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require`

## 2. Background Scheduler Options

### Decision
Use APScheduler with a dedicated worker process

### Rationale
APScheduler is well-maintained, supports multiple schedulers, integrates well with FastAPI, and provides the flexibility needed for both recurring tasks and reminder notifications.

### Alternatives Considered
- Celery: More complex setup with Redis/RabbitMQ requirements
- Built-in threading: Less robust and harder to manage
- Cron-like services: Less suitable for dynamic task scheduling

### Implementation Details
Will use BackgroundScheduler for recurring task generation and reminder checking

## 3. Reminder Notification Mechanism

### Decision
Implement database polling with APScheduler and update AI to check for pending reminders

### Rationale
Simpler implementation than WebSocket pushes, fits existing architecture, and avoids the complexity of real-time communication channels.

### Alternatives Considered
- WebSocket real-time updates: More complex implementation with connection management
- External notification services: Adds external dependencies

### Implementation Details
Polling-based system with periodic checks in background worker every minute

## 4. Docker Multi-stage Optimization

### Decision
Separate build and runtime stages with proper layer caching

### Rationale
Reduces final image size, improves security posture, and speeds up build times through layer caching.

### Alternatives Considered
- Single-stage builds: Larger images and slower builds
- Distroless images: Potential compatibility issues with Python applications

### Implementation Details
Multi-stage with proper .dockerignore and layer caching for dependencies

## 5. Data Model Extension Strategy

### Decision
Add columns to existing task table with optional foreign key to recurring patterns table

### Rationale
Maintains backward compatibility while adding necessary functionality. Most recurring tasks can be handled with simple patterns.

### Implementation Details
Add is_recurring, recurring_pattern, reminder_at, last_notified, and next_occurrence columns to task table

## 6. AI Integration Approach

### Decision
Extend existing AI agent system prompt and add new MCP tools for recurring tasks and reminders

### Rationale
Leverages existing AI infrastructure while adding new capabilities. Maintains consistency with current AI behavior.

### Implementation Details
Update system prompt in backend/src/agent/runner.py and add new tools to MCP server

## 7. Kubernetes Deployment Strategy

### Decision
Update existing Kubernetes manifests with Neon DB connection and resource optimizations

### Rationale
Builds upon existing K8s setup from Phase 4, minimizing new infrastructure changes.

### Implementation Details
Update environment variables in deployments and add proper resource limits for background processes

---
**Date**: 2026-01-31
**Status**: Complete