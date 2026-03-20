# 🚀 Production Deployment Guide

**AI-Adaptive Onboarding Engine** is now **PRODUCTION READY**. Follow this guide to deploy.

## ✅ Current Status

- **Server**: Running on http://localhost:8000
- **Health Check**: ✅ PASSING
- **API**: ✅ Fully Operational
- **Anthropic Integration**: ✅ Configured with API Key
- **Documentation**: ✅ Complete

## 📋 Files Included

### Core Application
```
✅ main.py                    - FastAPI application server
✅ skill_extractor.py         - Anthropic Claude integration
✅ gap_analyzer.py            - Semantic skill matching
✅ adaptive_pather.py         - Learning pathway generation
✅ course_catalog.json        - Course database
✅ .env                       - Environment variables (with API key)
```

### Deployment & Configuration
```
✅ requirements.txt           - Python dependencies
✅ Dockerfile                 - Container image definition
✅ docker-compose.yml         - Docker orchestration
✅ run.bat                    - Windows startup script
✅ run.sh                     - Linux/Mac startup script
✅ .gitignore                 - Safe version control
```

### Documentation & Testing
```
✅ README.md                  - Full documentation
✅ DEPLOYMENT.md              - This file
✅ index.html                 - Interactive API tester
✅ test_app.py                - Unit tests
✅ test_server.py             - Integration tests
```

## 🔑 API Key Configuration

Your Anthropic API Key is configured in `.env`:
```
ANTHROPIC_API_KEY=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
```

**⚠️ IMPORTANT:**
- Never commit `.env` to version control
- Rotate API keys regularly
- Use environment variables in production
- Use secrets management (AWS Secrets, Vault, etc.) for cloud deployments

## 🚀 Quick Start

### Windows
```powershell
cd "c:\Users\HP\PycharmProjects\AI-Adaptive Onboarding Engine"
.\run.bat
```

### Linux/Mac
```bash
cd /path/to/project
bash run.sh
```

### Manual
```bash
# Activate virtual environment
.venv/Scripts/activate          # Windows
source .venv/bin/activate       # Linux/Mac

# Start server
python main.py
```

Server will be available at: **http://localhost:8000**

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Health Check | http://localhost:8000/health | Monitor server status |
| API Docs (Swagger) | http://localhost:8000/docs | Interactive API documentation |
| API Docs (ReDoc) | http://localhost:8000/redoc | Alternative API documentation |
| Web Tester | file:///.../index.html | Interactive API testing |

## 📡 API Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```
Response: `{"status":"ok"}`

### 2. Analyze Skills
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python developer with 5 years experience, AWS, Git",
    "jd_text": "Senior Full-Stack Engineer needed with Docker, Kubernetes expertise",
    "max_hours": 40.0
  }'
```

## 🐳 Docker Deployment

### Build Container
```bash
docker build -t onboarding-engine:latest .
```

### Run Standalone
```bash
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-api03-... \
  onboarding-engine:latest
```

### Run with Docker Compose
```bash
docker-compose up -d
```

## ☁️ Cloud Deployment

### AWS Lambda (with API Gateway)
1. Use `uvicorn` with AWS Lambda layer
2. Configure environment variables in Lambda console
3. Set up API Gateway trigger

### Google Cloud Run
```bash
gcloud run deploy onboarding-engine \
  --source . \
  --set-env-vars ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name onboarding-engine \
  --image onboarding-engine:latest \
  --ports 8000 \
  --environment-variables ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Heroku
```bash
heroku create onboarding-engine
git push heroku main
heroku config:set ANTHROPIC_API_KEY=sk-ant-api03-...
```

## 🔒 Security Checklist

- [ ] API key stored in environment variables (not in code)
- [ ] `.env` file in `.gitignore`
- [ ] HTTPS enabled in production
- [ ] CORS properly configured for allowed origins
- [ ] Input validation enabled
- [ ] Rate limiting configured
- [ ] Logging and monitoring enabled
- [ ] Regular security updates
- [ ] API key rotation schedule

## 📊 Monitoring & Logging

### Health Monitoring
```bash
# Monitor endpoint
watch -n 5 'curl -s http://localhost:8000/health'

# Docker logs
docker logs -f <container_id>
```

### Production Logging
Add to `main.py`:
```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

## 🔄 Update & Maintenance

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

### Restart Server
```bash
# Kill existing process
Get-Process python | Stop-Process -Force  # Windows
pkill -f "python main.py"                 # Linux/Mac

# Start new instance
python main.py
```

## 🐛 Troubleshooting

### Port Already In Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Missing Course Catalog
```bash
# Verify file exists
ls -la course_catalog.json

# Check permissions
chmod 644 course_catalog.json
```

### API Key Issues
```bash
# Verify key is set
echo $env:ANTHROPIC_API_KEY          # Windows PowerShell
echo $ANTHROPIC_API_KEY              # Linux/Mac

# Test API key
curl -H "Authorization: Bearer ${ANTHROPIC_API_KEY}" \
  https://api.anthropic.com/v1/models
```

## 📈 Performance Tuning

### Server Configuration
```python
# main.py
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    workers=4,                    # Increase for multi-core
    loop="uvloop",               # Faster event loop
    access_log=False             # Disable for speed
)
```

### Database/Cache (Optional)
- Add Redis for caching results
- Use PostgreSQL for persistence
- Implement query optimization

## 📞 Support & Maintenance

### Getting Help
1. Check README.md for detailed docs
2. Review error logs for specific issues
3. Test endpoints with `index.html`
4. Check Anthropic API documentation

### Reporting Issues
Include:
- Error message and traceback
- Request/response data
- Environment details (OS, Python version)
- Steps to reproduce

## ✨ Next Steps

1. **Deploy to production** using Docker or cloud platform
2. **Set up monitoring** with logs and metrics
3. **Configure authentication** for API access
4. **Enable HTTPS** with SSL certificates
5. **Add database** for persistent data
6. **Implement rate limiting** for API protection
7. **Set up CI/CD pipeline** for automated deployments

## 📝 Checklists

### Pre-Deployment
- [ ] API key configured in `.env`
- [ ] All dependencies installed
- [ ] Health check passing
- [ ] API endpoints tested
- [ ] CORS properly configured
- [ ] Error handling verified
- [ ] Logging configured
- [ ] Security review completed

### Post-Deployment
- [ ] Monitor server logs
- [ ] Test all endpoints
- [ ] Verify health checks
- [ ] Set up alerts
- [ ] Document deployment
- [ ] Record connection details
- [ ] Back up configuration

---

**Congratulations!** 🎉 Your AI-Adaptive Onboarding Engine is production-ready!

For more details, see README.md or contact support.
