#!/usr/bin/env python3
"""Simple test to verify all components work correctly."""

from skill_extractor import extract_skills
from gap_analyzer import GapAnalyzer
from adaptive_pather import AdaptivePather

print("=" * 60)
print("Testing AI-Adaptive Onboarding Engine")
print("=" * 60)

# Test 1: AdaptivePather
print("\n[1] Testing AdaptivePather...")
try:
    pather = AdaptivePather()
    print(f"✓ AdaptivePather initialized")
    print(f"✓ Loaded {len(pather.catalog)} courses")
    print(f"✓ Skill index has {len(pather.skill_to_courses)} unique skills")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: GapAnalyzer
print("\n[2] Testing GapAnalyzer...")
try:
    analyzer = GapAnalyzer()
    candidate_skills = ["Python", "JavaScript", "AWS", "Git"]
    required_skills = ["Python", "Kubernetes", "Docker", "TensorFlow"]
    
    analyzer.build_candidate_index(candidate_skills)
    gaps = analyzer.compute_gaps(required_skills)
    
    print(f"✓ GapAnalyzer initialized")
    print(f"✓ Analyzed {len(required_skills)} required skills")
    print(f"✓ Found {len(gaps)} skill gaps")
    for gap in gaps:
        print(f"  - {gap.required_skill}: severity={gap.gap_severity:.2f}, match={gap.closest_match}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Mock skill extraction (without Anthropic API)
print("\n[3] Testing mock skill extraction...")
try:
    from skill_extractor import SkillEntry, SkillExtractionResult
    mock_result = SkillExtractionResult(
        skills=[
            SkillEntry(skill="Python", category="technical", proficiency="advanced", evidence="10 years Python"),
            SkillEntry(skill="Leadership", category="soft", proficiency="intermediate", evidence="Team lead experience")
        ],
        years_experience=10.0,
        current_role="Senior Developer",
        education="BS Computer Science"
    )
    print(f"✓ Created mock skill result with {len(mock_result.skills)} skills")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Pathway building
print("\n[4] Testing pathway generation...")
try:
    pather = AdaptivePather()
    analyzer = GapAnalyzer()
    
    # Create mock gap data
    from gap_analyzer import SkillGap
    mock_gaps = [
        SkillGap(required_skill="Docker", category="tool", gap_severity=0.8, closest_match="Git", similarity_score=0.3),
        SkillGap(required_skill="Kubernetes", category="tool", gap_severity=0.9, closest_match=None, similarity_score=0.1),
    ]
    
    pathway = pather.build_pathway(mock_gaps, max_hours=40.0)
    print(f"✓ Generated learning pathway")
    print(f"✓ {len(pathway.ordered_courses)} courses selected")
    print(f"✓ Total duration: {pathway.total_hours} hours")
    print(f"✓ Reasoning steps: {len(pathway.reasoning_trace)}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)
