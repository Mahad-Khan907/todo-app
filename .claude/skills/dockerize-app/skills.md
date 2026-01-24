### Phase 4 Objective: Dockerize the Todo Chatbot Application

This skill provides a specification-driven approach to containerizing the application using Gordon, the Docker AI assistant.

#### 1. Analyze Project Structure
- Identify the backend (Python/FastAPI) and frontend (Next.js) directories.
- Note the language, framework, and dependency files (`requirements.txt`, `package.json`).

#### 2. Generate Backend Dockerfile
- **Prompt to `Gordon`**: "Create a multi-stage `Dockerfile` for a Python 3.11 FastAPI application. The source code is in `backend/src`, and dependencies are listed in `backend/requirements.txt`. Optimize for a small image size and production readiness."
- **Review and Optimize**: Ensure the generated `Dockerfile` uses an official slim base image, copies only necessary files, and runs the application as a non-root user.

#### 3. Generate Frontend Dockerfile
- **Prompt to `Gordon`**: "Generate a multi-stage `Dockerfile` for a Next.js application. The project uses `npm`. The build context is the `frontend` directory. Ensure the final stage uses a lightweight static web server like Nginx."
- **Review and Optimize**: Verify that the build stage correctly installs dependencies and builds the static assets, and that the final stage is minimal.

#### 4. Build and Tag Images
- Use `docker build` to create images for both frontend and backend.
- Tag the images with a consistent naming convention (e.g., `todo-chatbot-backend:v1.0.0`).
