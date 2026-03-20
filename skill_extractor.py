import anthropic
import json
from pydantic import BaseModel, Field
from typing import Optional
import fitz  # PyMuPDF
import os
import re

# Try to initialize Anthropic client, fall back to mock if no API key
try:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        client = anthropic.Anthropic(api_key=api_key)
    else:
        client = None
except Exception:
    client = None


class SkillEntry(BaseModel):
    skill: str
    category: str  # e.g. "technical", "domain", "soft"
    proficiency: str  # "beginner" | "intermediate" | "advanced" | "expert"
    evidence: str  # direct quote from source document


class SkillExtractionResult(BaseModel):
    skills: list[SkillEntry]
    years_experience: Optional[float]
    current_role: Optional[str]
    education: Optional[str]


EXTRACTION_PROMPT = """
You are a precise skill extraction engine. Analyze the provided document and extract ALL skills.

For each skill, you MUST:
1. Identify the exact skill name (normalize to standard terminology)
2. Categorize it: "technical" | "domain" | "soft" | "tool" | "certification"
3. Infer proficiency from context clues (years mentioned, project complexity, job titles)
4. Quote the exact evidence from the text

Rules:
- Extract only what is explicitly mentioned or strongly implied
- Normalize skill names (e.g. "ML" → "Machine Learning", "JS" → "JavaScript")  
- Do NOT invent or hallucinate skills not present in the document
- Return ONLY valid JSON matching the schema, no preamble

Schema: {schema}

Document:
{document_text}
"""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join(page.get_text() for page in doc)


def extract_skills_from_text(text: str, doc_type: str = "resume") -> tuple[list[SkillEntry], Optional[float], Optional[str]]:
    """
    Mock skill extraction using regex and pattern matching.
    Fallback when Anthropic API is not available.
    """
    skills = []
    text_lower = text.lower()
    
    # Technical skills database
    technical_skills = {
        'python': 'technical', 'java': 'technical', 'javascript': 'technical',
        'typescript': 'technical', 'c++': 'technical', 'c#': 'technical',
        'go': 'technical', 'rust': 'technical', 'php': 'technical',
        'ruby': 'technical', 'kotlin': 'technical', 'swift': 'technical',
        'react': 'technical', 'angular': 'technical', 'vue': 'technical',
        'node.js': 'technical', 'express': 'technical', 'django': 'technical',
        'flask': 'technical', 'fastapi': 'technical', 'spring': 'technical',
        'postgresql': 'technical', 'mysql': 'technical', 'mongodb': 'technical',
        'redis': 'technical', 'elasticsearch': 'technical', 'sql': 'technical',
        'aws': 'tool', 'azure': 'tool', 'gcp': 'tool', 'docker': 'tool',
        'kubernetes': 'tool', 'terraform': 'tool', 'jenkins': 'tool',
        'git': 'tool', 'github': 'tool', 'gitlab': 'tool', 'bitbucket': 'tool',
        'machine learning': 'domain', 'deep learning': 'domain', 'nlp': 'domain',
        'computer vision': 'domain', 'tensorflow': 'domain', 'pytorch': 'domain',
        'scikit-learn': 'domain', 'pandas': 'domain', 'numpy': 'domain',
        'communication': 'soft', 'leadership': 'soft', 'teamwork': 'soft',
        'problem solving': 'soft', 'critical thinking': 'soft', 'project management': 'soft',
    }
    
    # Find skills in text
    found_skills = set()
    for skill, category in technical_skills.items():
        if skill in text_lower:
            found_skills.add((skill, category))
    
    # Extract years of experience
    years_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)', text_lower)
    years_exp = float(years_match.group(1)) if years_match else None
    
    # Extract role (simplified)
    role_patterns = [
        r'(?:currently\s+)?(?:working\s+as\s+)?(?:a\s+)?(.*?)\s+(?:at|with|in|engineer|developer|manager)',
        r'(senior|junior|lead|staff|principal)?\s+(engineer|developer|architect|analyst|manager)'
    ]
    current_role = None
    for pattern in role_patterns:
        match = re.search(pattern, text_lower)
        if match:
            current_role = match.group(0).title()
            break
    
    # Create skill entries
    for skill, category in sorted(found_skills):
        skills.append(SkillEntry(
            skill=skill.title(),
            category=category,
            proficiency='intermediate' if years_exp and years_exp > 2 else 'beginner',
            evidence=f"Found in {doc_type}"
        ))
    
    return skills, years_exp, current_role


def extract_skills(document_text: str, doc_type: str = "resume") -> SkillExtractionResult:
    """
    Extract structured skills from resume or JD.
    Uses Claude API if available, otherwise uses pattern matching.
    """
    if client:
        # Use Claude API
        try:
            schema = SkillExtractionResult.model_json_schema()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                system="You are a precise skill extraction engine. Return ONLY valid JSON. No markdown, no preamble.",
                messages=[{
                    "role": "user",
                    "content": EXTRACTION_PROMPT.format(
                        schema=json.dumps(schema, indent=2),
                        document_text=document_text[:8000]
                    )
                }]
            )
            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw)
            return SkillExtractionResult(**data)
        except Exception as e:
            # Fall back to mock if API fails
            print(f"Warning: Claude API failed ({str(e)[:50]}...), using mock extractor")
            skills, years_exp, role = extract_skills_from_text(document_text, doc_type)
            return SkillExtractionResult(
                skills=skills,
                years_experience=years_exp,
                current_role=role,
                education=None
            )
    else:
        # Use mock extraction
        skills, years_exp, role = extract_skills_from_text(document_text, doc_type)
        return SkillExtractionResult(
            skills=skills,
            years_experience=years_exp,
            current_role=role,
            education=None
        )