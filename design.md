# Design Document

## Overview

This design document outlines the architecture and implementation approach for a comprehensive user authentication system built from scratch. The system will be developed using a loosely coupled microservices architecture with Python FastAPI for the backend, React for the frontend, PostgreSQL for data persistence, and Docker for containerization. The authentication system supports traditional email/password registration with email verification, Google OAuth, and Facebook OAuth integration.

## Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[React Frontend]
    end
    
    subgraph "API Gateway Layer"
        B[FastAPI Backend]
    end
    
    subgraph "Data Layer"
        C[PostgreSQL Database]
    end
    
    subgraph "External Services"
        D[Google OAuth]
        E[Facebook OAuth]
        F[SMTP Email Service]
    end
    
    A --> B
    B --> C
    B --> D
    B --> E
    B --> F
```

### Project Structure

```
auth-system/
├── README.md
├── docker-compose.yml
├── .gitignore
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── auth.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       └── users.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── email_service.py
│   │   │   └── oauth_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── email.py
│   │       └── security.py
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── alembic.ini
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_auth.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── .env
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── index.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Header.js
│   │   │   │   ├── Footer.js
│   │   │   │   └── LoadingSpinner.js
│   │   │   └── auth/
│   │   │       ├── LoginForm.js
│   │   │       ├── RegisterForm.js
│   │   │       ├── SocialLogin.js
│   │   │       └── EmailVerification.js
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Dashboard.js
│   │   │   └── EmailVerify.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   └── oauth.js
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   └── utils/
│   │       ├── validation.js
│   │       └── constants.js
│   └── tests/
│       └── components/
└── database/
    ├── init.sql
    └── migrations/
```

## Components and Interfaces

### Backend Components

#### 1. FastAPI Application Structure

**Main Application (`app/main.py`)**
- FastAPI application initialization
- CORS middleware configuration
- API router registration
- Health check endpoints

**Core Configuration (`app/core/`)**
- `config.py`: Environment variables and application settings
- `security.py`: JWT token handling, password hashing
- `database.py`: SQLAlchemy database connection and session management

**Models (`app/models/`)**
- `user.py`: SQLAlchemy User model with all required fields

**API Routes (`app/api/v1/`)**
- `auth.py`: Authentication endpoints (register, login, logout, verify-email)
- `users.py`: User management endpoints

**Services (`app/services/`)**
- `auth_service.py`: Authentication business logic
- `email_service.py`: Email sending functionality
- `oauth_service.py`: Google and Facebook OAuth integration

#### 2. API Endpoints Design

```
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/verify-email
GET  /api/v1/auth/google
GET  /api/v1/auth/google/callback
GET  /api/v1/auth/facebook
GET  /api/v1/auth/facebook/callback
GET  /api/v1/users/me
PUT  /api/v1/users/me
GET  /health
```

### Frontend Components

#### 1. React Application Structure

**Authentication Components**
- `LoginForm.js`: Email/password login form with validation
- `RegisterForm.js`: Registration form with password strength validation
- `SocialLogin.js`: Google and Facebook OAuth buttons
- `EmailVerification.js`: Email verification status and resend functionality

**Page Components**
- `Login.js`: Login page layout
- `Register.js`: Registration page layout
- `Dashboard.js`: Protected dashboard page
- `EmailVerify.js`: Email verification confirmation page

**Services**
- `api.js`: Axios configuration and API client
- `auth.js`: Authentication service methods
- `oauth.js`: OAuth integration helpers

**Context and Hooks**
- `AuthContext.js`: Global authentication state management
- `useAuth.js`: Custom hook for authentication operations

## Data Models

### User Table Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'suspended')),
    verification_token VARCHAR(255),
    verification_token_expires TIMESTAMP,
    provider VARCHAR(50) DEFAULT 'local' CHECK (provider IN ('local', 'google', 'facebook')),
    provider_id VARCHAR(255),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_verification_token ON users(verification_token);
CREATE INDEX idx_users_provider_id ON users(provider, provider_id);
```

### Session Management

```sql
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
```

## Error Handling

### Backend Error Handling Strategy

1. **Custom Exception Classes**
   - `AuthenticationError`: Invalid credentials
   - `ValidationError`: Input validation failures
   - `EmailNotVerifiedError`: Unverified account access attempts
   - `TokenExpiredError`: Expired verification tokens

2. **Global Exception Handler**
   - Standardized error response format
   - Appropriate HTTP status codes
   - Detailed error messages for development
   - Generic messages for production

3. **Error Response Format**
```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Password does not meet security requirements",
        "details": {
            "field": "password",
            "requirements": ["8+ characters", "uppercase", "lowercase", "number", "special character"]
        }
    }
}
```

### Frontend Error Handling

1. **Error Boundary Components**
   - Global error boundary for unhandled errors
   - Form-specific error handling

2. **User-Friendly Error Messages**
   - Real-time validation feedback
   - Clear error descriptions
   - Actionable error messages

## Testing Strategy

### Backend Testing

1. **Unit Tests**
   - Service layer testing with mocked dependencies
   - Model validation testing
   - Utility function testing

2. **Integration Tests**
   - API endpoint testing
   - Database integration testing
   - OAuth flow testing

3. **Test Database**
   - Separate test database configuration
   - Database fixtures and cleanup

### Frontend Testing

1. **Component Tests**
   - Form validation testing
   - User interaction testing
   - OAuth button functionality

2. **Integration Tests**
   - Authentication flow testing
   - API integration testing
   - Route protection testing

## Security Considerations

### Password Security
- bcrypt hashing with salt rounds (12+)
- Password strength validation
- Password confirmation matching

### Session Management
- JWT tokens with appropriate expiration
- Secure HTTP-only cookies for session storage
- Token refresh mechanism

### OAuth Security
- State parameter validation
- Secure redirect URI validation
- Token exchange security

### Email Verification
- Cryptographically secure token generation
- Token expiration (24 hours)
- Rate limiting for verification email requests

## Docker Configuration

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose Configuration
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/authdb
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=authdb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Environment Configuration

### Backend Environment Variables
```
DATABASE_URL=postgresql://user:password@localhost:5432/authdb
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
FRONTEND_URL=http://localhost:3000
```

### Frontend Environment Variables
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
REACT_APP_FACEBOOK_APP_ID=your-facebook-app-id
```

## Development Workflow

### Git Workflow
1. **Repository Structure**: Monorepo with separate directories for frontend, backend, and infrastructure
2. **Branch Strategy**: Feature branches with pull request reviews
3. **Commit Convention**: Conventional commits for automated versioning

### Development Setup
1. Clone repository
2. Copy environment files from examples
3. Run `docker-compose up` for full stack development
4. Access frontend at `http://localhost:3000`
5. Access backend API at `http://localhost:8000`
6. Access database at `localhost:5432`

This design provides a solid foundation for building a secure, scalable authentication system with modern development practices and clear separation of concerns.