# 🎓 AI-Adaptive Onboarding Engine

A production-ready FastAPI application that analyzes skill gaps and generates personalized learning pathways using the Anthropic Claude API.

## ✅ Status: PRODUCTION READY

- ✅ Full API integration with Anthropic Claude
- ✅ Error handling & fallback systems
- ✅ Health checks & monitoring
- ✅ Environment configuration (.env)
- ✅ CORS enabled for frontend integration
- ✅ Comprehensive API documentation
- ✅ Docker-ready deployment

## 🚀 Features

### Core Functionality
- **Skill Extraction**: Analyzes resumes and job descriptions to extract technical & soft skills
- **Gap Analysis**: Identifies skill gaps and provides similarity matching
- **Adaptive Pathways**: Generates personalized learning paths based on gaps
- **Smart Fallbacks**: Works without API key using pattern matching

### API Endpoints

#### Health Check
```
GET /health
Response: {"status": "ok"}
```

#### Skill Analysis
```
POST /api/analyze
Content-Type: application/json

{
  "resume_text": "string",
  "jd_text": "string",
  "max_hours": 40.0
}

Response:
{
  "candidate_profile": {...},
  "required_profile": {...},
  "skill_gaps": [{...}],
  "pathway": {
    "courses": [{...}],
    "total_hours": number,
    "skill_coverage": {...},
    "reasoning_trace": [...]
  }
}
```

#### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📋 Prerequisites

- Python 3.11+
- Anthropic API Key (optional, but recommended)

## 🔧 Installation

### 1. Clone and Setup
```bash
cd "c:\Users\HP\PycharmProjects\AI-Adaptive Onboarding Engine"
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create/update `.env` file:
```
ANTHROPIC_API_KEY= your_api_key
HOST=0.0.0.0
PORT=8000
DEBUG=False
CATALOG_PATH=course_catalog.json
MAX_HOURS=40.0
```

### 4. Run Server
```bash
python main.py
```

Server will start on http://localhost:8000

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### API Test
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python developer with 5 years experience",
    "jd_text": "Senior Full-Stack Engineer with Docker expertise",
    "max_hours": 40
  }'
```

### Web UI Test
Open `index.html` in your browser for interactive API testing

## 📁 Project Structure

```
├── main.py                      # FastAPI application
├── skill_extractor.py           # Skill extraction & Claude integration
├── gap_analyzer.py              # Gap analysis engine
├── adaptive_pather.py           # Learning pathway generation
├── gap_analyzer.py              # Semantic skill matching
├── course_catalog.json          # Courses database
├── .env                         # Environment variables
├── index.html                   # Web UI for testing
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .venv/                       # Virtual environment
```

## 🔑 Configuration

### Environment Variables
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: False)
- `CATALOG_PATH`: Path to course catalog JSON
- `MAX_HOURS`: Default max learning path hours (default: 40.0)
- `ALLOWED_ORIGINS`: CORS whitelist

## 📦 Dependencies

### Core
- fastapi >= 0.135.0
- uvicorn >= 0.42.0
- pydantic >= 2.12.0
- anthropic >= 0.86.0
- python-dotenv >= 1.0.0

### Optional
- numpy >= 2.4.0
- networkx >= 3.6.0
- pymupdf >= 1.27.0

## 🐳 Docker Deployment

Build and run with Docker:
```bash
docker build -t onboarding-engine .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-api03-... \
  onboarding-engine
```

## 🚨 Error Handling

The application includes comprehensive error handling:

1. **Missing API Key**: Falls back to pattern-matching-based skill extraction
2. **Invalid Input**: Returns detailed validation errors
3. **API Failures**: Attempts retry and falls back gracefully
4. **Course Catalog Issues**: Handles missing or malformed catalog files

## 📊 Response Schema

### SkillEntry
```json
{
  "skill": "Python",
  "category": "technical|tool|domain|soft|certification",
  "proficiency": "beginner|intermediate|advanced|expert",
  "evidence": "Quote or source from document"
}
```

### SkillGap
```json
{
  "required_skill": "Docker",
  "severity": 0.85,
  "closest_match": "Git",
  "similarity": 0.45
}
```

### LearningPathway
```json
{
  "ordered_courses": [...],
  "total_hours": 24.5,
  "skill_coverage": {"Docker": true, "Kubernetes": false},
  "reasoning_trace": [...]
}
```

## 🔐 Security Considerations

1. **API Key Protection**: Store in environment variables, never in code
2. **CORS Configuration**: Whitelist only trusted domains
3. **Input Validation**: All inputs validated with Pydantic
4. **Rate Limiting**: Consider adding in production
5. **Authentication**: Add JWT tokens for production use

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill existing process
Get-Process python | Stop-Process -Force
python main.py
```

### API Key Issues
```bash
# Verify API key is set
echo $env:ANTHROPIC_API_KEY
.env file exists and is readable
```

### Course Catalog Not Found
```bash
# Ensure course_catalog.json exists in the project root
ls course_catalog.json
```

## 📝 Development

### Add New Skills to Detection
Edit `skill_extractor.py` - `technical_skills` dictionary

### Customize Learning Pathways
Edit `adaptive_pather.py` - `build_pathway()` method

### Modify Course Catalog
Update `course_catalog.json` with new courses and skills

## 📜 License

This project is licensed under the MIT License.

## 📧 Support

For API key issues or Anthropic integration:
- Get API key: https://console.anthropic.com

For deployment issues:
- Check environment variables
- Review server logs
- Test health endpoint

---

**Version**: 1.0.0  
**Last Updated**: March 20, 2026  
**Status**: Production Ready ✅
