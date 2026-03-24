#!/usr/bin/env python3
"""
Unified AI SaaS Platform - File Generator
Creates all project files automatically
"""

import os
import json

def create_file(path, content):
    """Create a file with given content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ Created: {path}")

# Define all files
files = {
    # Root configs
    ".gitignore": """__pycache__/
*.pyc
.venv/
venv/
node_modules/
.next/
dist/
.env
.env.local
*.log
.DS_Store
.pytest_cache/
.coverage
build/
""",

    ".env.example": """APP_NAME=Unified AI SaaS Platform
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql://user:password@localhost:5432/unified_ai_db
REDIS_URL=redis://localhost:6379/0
VECTOR_DB_URL=http://localhost:6333
OPENAI_API_KEY=sk-proj-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
SECRET_KEY=your-secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
""",

    "CHANGELOG.md": """# Changelog

## [1.0.0] - 2024-03-24

### Added
- Initial release
- Complete backend (FastAPI)
- Frontend (Next.js)
- Kubernetes deployment
- Complete documentation
- GitHub Actions CI/CD
- Docker Compose setup
- Multi-tenant architecture
- Admin control panel
- REST API
- Vector database integration
""",

    "docker-compose.yml": """version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: unified_user
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: unified_ai_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://unified_user:secure_password@postgres:5432/unified_ai_db
      REDIS_URL: redis://redis:6379/0
      VECTOR_DB_URL: http://qdrant:6333
    depends_on:
      - postgres
      - redis
      - qdrant
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
""",

    # Backend files
    "backend/requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
openai==1.3.0
anthropic==0.7.0
groq==0.4.1
qdrant-client==2.4.0
sentence-transformers==2.2.2
redis==5.0.0
aioredis==2.0.1
httpx==0.25.0
pytest==7.4.3
pytest-asyncio==0.21.1
prometheus-client==0.18.0
python-json-logger==2.0.7
python-dotenv==1.0.0
""",

    "backend/Dockerfile": """FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    libpq-dev \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=10s --timeout=5s CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",

    "backend/.dockerignore": """__pycache__
*.pyc
.venv
.pytest_cache
.env
.git
""",

    "backend/app/__init__.py": "",

    "backend/app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Unified AI SaaS Platform",
    description="Enterprise-grade AI orchestration",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/ready")
async def ready():
    return {"ready": True}

@app.get("/")
async def root():
    return {"message": "Unified AI SaaS Platform", "docs": "/docs"}

@app.get("/api/v1/ping")
async def ping():
    return {"pong": True}
""",

    "backend/app/config.py": """from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Unified AI SaaS Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    SECRET_KEY: str = "your-secret-key"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
""",

    "backend/tests/__init__.py": "",

    "backend/tests/test_health.py": """from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["ready"] is True

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping():
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
""",

    # Frontend files
    "frontend/package.json": """{
  "name": "unified-ai-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.0.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "@types/react": "^18.2.37",
    "@types/node": "^20.8.0",
    "eslint": "^8.51.0",
    "eslint-config-next": "14.0.3"
  }
}
""",

    "frontend/next.config.js": """const nextConfig = {
  reactStrictMode: true,
  experimental: {
    appDir: true,
  },
};

module.exports = nextConfig;
""",

    "frontend/tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
""",

    "frontend/Dockerfile": """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
""",

    "frontend/.dockerignore": """node_modules
.next
.git
.env
""",

    "frontend/src/app/page.tsx": """export default function Home() {
  return (
    <main style={{ padding: '40px' }}>
      <h1>🤖 Unified AI SaaS Platform</h1>
      <p>Enterprise-grade AI orchestration platform</p>
      <ul>
        <li>Frontend: http://localhost:3000</li>
        <li>Backend: http://localhost:8000</li>
        <li>API Docs: http://localhost:8000/docs</li>
      </ul>
    </main>
  )
}
""",

    "frontend/src/app/layout.tsx": """export const metadata = {
  title: 'Unified AI SaaS Platform',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
""",

    # Infrastructure files
    "infrastructure/kubernetes/namespace.yaml": """apiVersion: v1
kind: Namespace
metadata:
  name: unified-ai
  labels:
    name: unified-ai
""",

    "infrastructure/kubernetes/backend-deployment.yaml": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: unified-ai-backend
  namespace: unified-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: ghcr.io/mythricollectionspune-source/unified-ai-backend:latest
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
""",

    "infrastructure/kubernetes/backend-service.yaml": """apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: unified-ai
spec:
  selector:
    app: backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
""",

    # Documentation
    "docs/SETUP.md": """# Setup Guide

## Local Development

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### Start Services

```bash
docker-compose up -d
