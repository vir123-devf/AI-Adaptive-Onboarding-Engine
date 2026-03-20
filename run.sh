#!/bin/bash
# AI-Adaptive Onboarding Engine - Startup Script

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎓 AI-Adaptive Onboarding Engine${NC}"
echo "=================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    cat > .env << EOF
ANTHROPIC_API_KEY=your-key-here
HOST=0.0.0.0
PORT=8000
DEBUG=False
CATALOG_PATH=course_catalog.json
MAX_HOURS=40.0
EOF
    echo -e "${YELLOW}📝 Please update .env with your API key${NC}"
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source .venv/bin/activate

# Install/update dependencies
echo -e "${YELLOW}📚 Installing dependencies...${NC}"
pip install -q -r requirements.txt

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}❌ Error: ANTHROPIC_API_KEY not set in .env${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Starting server...${NC}"
python main.py

deactivate
