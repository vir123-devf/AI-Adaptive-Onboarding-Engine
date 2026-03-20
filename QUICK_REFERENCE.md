# 🎯 Quick Reference Guide

## Server Commands

### Windows PowerShell
```powershell
# Start server
.\run.bat

# Or manually
.\.venv\Scripts\Activate.ps1
python main.py

# Kill process
Get-Process python | Stop-Process -Force
```

### Linux/Mac
```bash
# Start server
bash run.sh

# Or manually
source .venv/bin/activate
python main.py

# Kill process
pkill -f "python main.py"
```

## API Quick Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### Analyze Skills
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume text here",
    "jd_text": "Job description text here",
    "max_hours": 40.0
  }'
```

### API Documentation
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Port 8000 in use | `Get-Process python \| Stop-Process -Force` |
| API key not found | Check `.env` file, set `ANTHROPIC_API_KEY` |
| Module not found | Run `pip install -r requirements.txt` |
| Permission denied | Run with admin/sudo or use `chmod +x *.sh` |
| Connection refused | Verify server is running with `curl http://localhost:8000/health` |

## File Structure

```
project/
├── main.py              ← FastAPI server (START HERE)
├── skill_extractor.py   ← Claude integration
├── gap_analyzer.py      ← Skill gap analysis
├── adaptive_pather.py   ← Learning paths
├── course_catalog.json  ← Course data
├── .env                 ← Configuration (API KEY HERE)
├── requirements.txt     ← Dependencies
├── index.html           ← Web UI
├── Dockerfile           ← Container image
└── .venv/               ← Virtual environment
```

## Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Server health check |
| POST | `/api/analyze` | Analyze skills & generate pathway |
| GET | `/docs` | Swagger API documentation |
| GET | `/redoc` | ReDoc API documentation |

## Environment Variables

```bash
ANTHROPIC_API_KEY       # Your API key (REQUIRED)
HOST                    # Server host (default: 0.0.0.0)
PORT                    # Server port (default: 8000)
DEBUG                   # Debug mode (default: False)
CATALOG_PATH            # Course catalog file
MAX_HOURS               # Default max hours for pathways
```

## Testing

### Health Check
```bash
# Should return {"status":"ok"}
curl http://localhost:8000/health
```

### Run Unit Tests
```bash
python test_app.py
python test_server.py
```

### Interactive Testing
Open `index.html` in your browser

## Docker Commands

```bash
# Build image
docker build -t onboarding-engine .

# Run container
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-api03-... \
  onboarding-engine

# Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## Useful Python Commands

```bash
# Check if module is installed
python -c "import fastapi; print(fastapi.__version__)"

# Test API programmatically
python -c "
import requests
r = requests.post('http://localhost:8000/api/analyze', json={
  'resume_text': 'Python developer',
  'jd_text': 'Senior engineer needed',
  'max_hours': 40
})
print(r.status_code, r.json())
"

# Check environment variables
python -c "import os; print(os.getenv('ANTHROPIC_API_KEY', 'NOT SET'))"
```

## Git Workflow

```bash
# Initialize repo
git init
git add .
git commit -m "Initial commit: Production-ready AI Onboarding Engine"

# Create ignored files list
echo ".env" >> .gitignore
echo ".venv/" >> .gitignore

# Push to remote
git remote add origin <your-repo-url>
git push -u origin main
```

## Performance Monitoring

```bash
# Monitor CPU/Memory
watch -n 1 'ps aux | grep python'      # Linux
Get-Process python | Select *          # Windows

# Monitor network
netstat -an | grep 8000                # Check port

# Monitor logs
tail -f logs/app.log                   # Follow logs
```

## Emergency Procedures

### Reset Everything
```bash
# Remove virtual environment
rm -rf .venv                            # Linux/Mac
rmdir /s .venv                          # Windows

# Reinstall
python -m venv .venv
.venv/Scripts/activate                  # Windows
source .venv/bin/activate               # Linux/Mac
pip install -r requirements.txt
python main.py
```

### Backup Configuration
```bash
cp .env .env.backup
cp course_catalog.json course_catalog.json.backup
git status                              # Check uncommitted changes
```

---

## 📚 Full Documentation

- **README.md** - Complete documentation
- **DEPLOYMENT.md** - Deployment guide
- **http://localhost:8000/docs** - Interactive API docs

## 🆘 Need Help?

1. Check error message
2. Review README.md section
3. Test with `curl` or `index.html`
4. Check `.env` configuration
5. Review server logs with `docker logs` or terminal output

---

**Version**: 1.0.0 | **Status**: Production Ready ✅
