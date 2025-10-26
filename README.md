# AI Agent Development Stack

A comprehensive Docker Compose setup for building AI agents with multiple tools and services.

## 🚀 Quick Start

### Option 1: Run All Services (Recommended)
```bash
docker compose up -d
```

### Option 2: Run Individual Services
```bash
# Twenty CRM only
docker compose -f docker-compose.twenty.yml up -d

# n8n workflow automation only
docker compose -f docker-compose.n8n.yml up -d

# Ollama AI models only
docker compose -f docker-compose.ollama.yml up -d

# Typebot chatbot builder only
docker compose -f docker-compose.typebot.yml up -d

# BentoML model serving only
docker compose -f docker-compose.bentoml.yml up -d

# Portainer management UI only
docker compose -f docker-compose.portainer.yml up -d
```

## 📋 Services Overview

### 1. 🤖 Ollama (Port 11434)
- **AI Model Server** for Llama, Mistral, and other open-source models
- **Standalone service** - no dependencies
- Access: http://localhost:11434

### 2. 🔄 n8n (Port 5678)
- **Visual Workflow Automation** for AI agent orchestration
- **Database**: PostgreSQL (n8n dedicated)
- **Access**: http://localhost:5678
- **Credentials**: admin / CoolAI123!

### 3. 📊 Twenty CRM (Port 3000)
- **Open-source Pipeline Tracker** for sales and customer management
- **Database**: PostgreSQL (Twenty dedicated)
- **Cache**: Redis (shared)
- **Access**: http://127.0.0.1:3000

### 4. 💬 Typebot (Port 3001)
- **Chatbot Builder** with visual flow editor
- **Database**: MongoDB (Typebot dedicated)
- **Cache**: Redis (shared with Twenty)
- **Access**: http://localhost:3001

### 5. 🧠 BentoML (Port 5000)
- **Model Serving Platform** for ML microservices
- **Standalone service** - no dependencies
- **Access**: http://localhost:5000

### 6. 🐳 Portainer (Port 9000)
- **Docker Management UI** for monitoring all containers
- **Access**: http://localhost:9000
- **Setup**: Choose "Local" environment on first login

## 🛠️ Configuration

### Environment Variables (.env)
```bash
# Twenty CRM Database
PG_DATABASE_USER=postgres
PG_DATABASE_PASSWORD=twenty_password_2024
PG_DATABASE_NAME=default

# Redis (shared)
REDIS_URL=redis://redis:6379

# Server settings
SERVER_URL=http://127.0.0.1:3000
NODE_PORT=3000
HOST=0.0.0.0

# Security
APP_SECRET=X7kP9mR2tY4uI8wE1rT5yU3iO6pL9kJ2hN4bV1cX8zA5sD2fG6hJ8kL3mN7bV1cX4zA8sD

# Development settings
DISABLE_DB_MIGRATIONS=true
DISABLE_CRON_JOBS_REGISTRATION=true
```

## 📁 File Structure

```
DemoForge/
├── docker-compose.yml              # Main orchestration (all services)
├── docker-compose.ollama.yml       # Ollama only
├── docker-compose.n8n.yml          # n8n + PostgreSQL
├── docker-compose.twenty.yml       # Twenty CRM + PostgreSQL + Redis
├── docker-compose.typebot.yml      # Typebot + MongoDB + Redis
├── docker-compose.bentoml.yml      # BentoML only
├── docker-compose.portainer.yml    # Portainer only
├── .env                           # Environment variables
└── README.md                      # This file
```

## 🔧 Management Commands

### Start Everything
```bash
docker compose up -d
```

### Stop Everything
```bash
docker compose down
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f twenty-server-1
```

### Check Status
```bash
docker compose ps
```

### Restart Service
```bash
docker compose restart twenty-server-1
```

## 🔍 Troubleshooting

### Port Conflicts
If you get port binding errors, modify the ports in the compose files:
```yaml
ports:
  - "3001:3000"  # Change external port as needed
```

### Windows Firewall
Allow Docker backend through Windows Firewall:
```powershell
netsh advfirewall firewall add rule name="Docker Twenty CRM" dir=in action=allow program="C:\Program Files\Docker\Docker\resources\com.docker.backend.exe" enable=yes
```

### Database Issues
If services fail to start due to database connectivity:
```bash
# Remove volumes and start fresh
docker compose down -v
docker compose up -d
```

## 🌐 Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| Twenty CRM | http://127.0.0.1:3000 | Pipeline management |
| n8n | http://localhost:5678 | Workflow automation |
| Ollama | http://localhost:11434 | AI model API |
| Typebot | http://localhost:3001 | Chatbot builder |
| BentoML | http://localhost:5000 | Model serving |
| Portainer | http://localhost:9000 | Docker management |

## 📝 Notes

- **Redis is shared** between Twenty CRM and Typebot for caching
- **Each service has its own database** (PostgreSQL for Twenty/n8n, MongoDB for Typebot)
- **All services use health checks** for proper startup order
- **Persistent volumes** are configured for data persistence
- **Environment variables** are centralized in the .env file

## 🚀 Next Steps

1. Start with `docker compose up -d` to run everything
2. Access Twenty CRM at http://127.0.0.1:3000
3. Set up n8n workflows at http://localhost:5678
4. Use Portainer at http://localhost:9000 to manage containers
5. Pull AI models in Ollama and integrate with n8n workflows
