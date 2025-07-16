# Local Development Setup Guide

This document provides a step-by-step guide to setting up the `auth-system` project for local development.

## 1. Prerequisites

Before you begin, ensure you have the following installed on your machine:
-   **Git:** For version control.
-   **Docker & Docker Compose:** For running the containerized services. Make sure the Docker daemon is running.
-   **Node.js & npm:** For installing frontend dependencies.

## 2. Initial Setup

### a. Clone the Repository
First, clone the project repository from GitHub:
```bash
git clone https://github.com/SudheerNarra7/SpecCoding.git
cd auth-system
```

### b. Create Environment File
This is a critical step. The backend and database services require environment variables to function correctly.

Create a new file named `.env` inside the `backend` directory (`backend/.env`).

Copy and paste the following content into `backend/.env`:
```
# PostgreSQL Database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=auth_db
DATABASE_URL=postgresql://user:password@db:5432/auth_db

# FastAPI Backend
SECRET_KEY=a_very_secret_key_that_should_be_changed
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
**Note:** This file is intentionally not committed to Git for security reasons.

### c. Install Frontend Dependencies
The frontend Docker build requires the `package-lock.json` file to exist. Generate it by running `npm install` in the `frontend` directory:
```bash
cd frontend
npm install
cd ..
```

## 3. Build and Run the Application

With the setup complete, you can now build the Docker images and start all the services using a single command from the project root directory:
```bash
docker-compose up --build -d
```
The `-d` flag runs the containers in detached mode (in the background).

## 4. Verify the Services

After a few moments for the services to initialize, you can verify that everything is running correctly.

### a. Check Container Status
List all running containers to ensure `frontend`, `backend`, and `db` are all `Up`:
```bash
docker-compose ps
```

### b. Verify Backend Health
The backend exposes a health check endpoint. You can test it using `curl`:
```bash
curl http://localhost:8000/health
```
You should see the response: `{"status":"ok"}`

### c. Verify Frontend Access
The frontend should be accessible in your browser at `http://localhost:3000`. You can also check it from the command line:
```bash
curl http://localhost:3000
```
This should return the HTML content of the main page.

### d. Verify Database Initialization
You can connect to the running database container and list the tables to confirm the `init.sql` script was executed:
```bash
docker-compose exec -T db psql -U user -d auth_db -c "\dt"
```
You should see the `users` and `user_sessions` tables listed.

## 5. Stopping the Application
To stop all running services, use:
```bash
docker-compose down
```
To stop the services and also remove the database volume (deleting all data), use:
```bash
docker-compose down -v
``` 