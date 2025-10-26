# BentoML Setup Guide

This directory contains a complete BentoML (Bento Machine Learning) setup for serving machine learning models in the DemoForge stack.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start BentoML Services**
   ```bash
   docker-compose -f docker-compose.bentoml.yml up -d
   ```

3. **Access Services**
   - **BentoML API**: http://localhost:5000
   - **BentoML Dashboard**: http://localhost:5001
   - **Redis**: localhost:6379

## 📁 Project Structure

```
bentoml/
├── docker-compose.bentoml.yml    # Main docker-compose configuration
├── Dockerfile.bentoml           # BentoML container definition
├── bentoml_config.yml           # BentoML configuration
├── demo_bentoml_service.py      # Demo ML service
├── ml_service.py                # Additional ML service
└── scripts/
    └── train_model.py           # Model training script
```

## 🔧 Services

### **bentoml-api** (Port 5000)
- Main BentoML API server
- Serves machine learning models
- Provides prediction endpoints
- Health check: http://localhost:5000/health

### **bentoml-dashboard** (Port 5001)
- Web-based model management interface
- Model deployment and monitoring
- Visual model performance metrics

### **redis** (Port 6379)
- Caching and session storage
- Model result caching
- BentoML internal state management

## 🛠️ API Usage

### **Health Check**
```bash
curl http://localhost:5000/health
```

### **Make Predictions**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [1, 2, 3, 4, 5]}'
```

### **Get Service Info**
```bash
curl http://localhost:5000/info
```

## ⚙️ Configuration

Environment variables in `.env`:

```bash
# BentoML Configuration
BENTOML_HOST=0.0.0.0
BENTOML_PORT=5000
BENTOML_API_WORKERS=1
BENTOML_MODEL_STORE=/opt/bentoml/models
BENTOML_CONFIG=/opt/bentoml/bentoml_config.yml

# Redis Configuration for BentoML
REDIS_URL=redis://redis:6379
```

## 📊 Available Models

### **Demo Model**
- **Type**: Binary Classification
- **Input**: Array of numbers
- **Output**: Prediction (0 or 1) with confidence
- **Logic**: Sum of input values > 0 = class 1

## 🔄 Model Development

### **Creating New Models**

1. **Define Service** in `demo_bentoml_service.py`:
```python
@bentoml.service()
class MyModelService:
    @bentoml.api
    def predict(self, input_data: JSON) -> JSON:
        # Your model logic here
        return {"result": prediction}
```

2. **Build Bento**:
```bash
bentoml build demo_bentoml_service:latest
```

3. **Serve Model**:
```bash
bentoml serve demo_bentoml_service:latest
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose -f docker-compose.bentoml.yml up -d

# Stop all services
docker-compose -f docker-compose.bentoml.yml down

# View logs
docker-compose -f docker-compose.bentoml.yml logs -f

# Restart specific service
docker-compose -f docker-compose.bentoml.yml restart bentoml-api
```

## 📈 Monitoring

- **Container Status**: Check via Docker or the GUI manager
- **API Metrics**: Available through BentoML dashboard
- **Redis Stats**: `redis-cli info` or Redis dashboard
- **Logs**: `docker-compose logs -f bentoml-api`

## 🔧 Troubleshooting

### **Common Issues**

1. **Port Conflicts**
   - Check if ports 5000, 5001, 6379 are available
   - Modify ports in docker-compose.yml if needed

2. **Model Loading Errors**
   - Ensure models are in the `/models` directory
   - Check BentoML logs: `docker-compose logs bentoml-api`

3. **Redis Connection Issues**
   - Verify Redis is running: `docker-compose ps`
   - Check Redis logs: `docker-compose logs redis`

### **Debug Commands**

```bash
# Check running containers
docker ps

# Check container logs
docker logs bentoml_api

# Test Redis connection
docker exec bentoml_redis redis-cli ping

# Test API health
curl http://localhost:5000/health
```

## 🌐 Integration

BentoML integrates with:
- **GUI Manager**: Accessible via the DemoForge interface
- **Other Services**: Can serve models for N8N workflows
- **External APIs**: RESTful endpoints for any application

## 📚 Resources

- [BentoML Documentation](https://docs.bentoml.org/)
- [BentoML GitHub](https://github.com/bentoml/BentoML)
- [Model Serving Best Practices](https://docs.bentoml.org/en/latest/guides/)
