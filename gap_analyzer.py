import numpy as np
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

# Initialize the sentence transformer model
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("Loaded SentenceTransformer model: all-MiniLM-L6-v2")
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer: {e}")
    raise


@dataclass
class SkillGap:
    required_skill: str
    category: str
    gap_severity: float  # 0.0 (has it) → 1.0 (completely missing)
    closest_match: str | None  # best matching skill the candidate has
    similarity_score: float


class GapAnalyzer:
    def __init__(self):
        self.index = None
        self.candidate_skills: list[str] = []
        self.candidate_embeddings = None

    def build_candidate_index(self, candidate_skills: list[str]):
        """Encode candidate skills for semantic search."""
        self.candidate_skills = candidate_skills
        self.candidate_embeddings = model.encode(candidate_skills, normalize_embeddings=True)

    def compute_gaps(self, required_skills: list[str], threshold: float = 0.75) -> list[SkillGap]:
        """
        For each required skill, find semantic nearest-neighbor in candidate skills.
        Gap severity = 1 - max_similarity (capped by threshold logic).
        """
        if not self.candidate_skills or self.candidate_embeddings is None:
            return [SkillGap(s, "unknown", 1.0, None, 0.0) for s in required_skills]

        gaps = []
        req_embeddings = model.encode(required_skills, normalize_embeddings=True)

        # Simple cosine similarity using numpy dot product (since embeddings are normalized)
        for i, req_skill in enumerate(required_skills):
            req_emb = req_embeddings[i:i+1]  # shape (1, 384)
            similarities = np.dot(req_emb, self.candidate_embeddings.T).flatten()  # (n_candidates,)
            
            max_sim_idx = np.argmax(similarities)
            max_sim = float(similarities[max_sim_idx])
            closest = self.candidate_skills[max_sim_idx]

            if max_sim >= threshold:
                gap_severity = max(0.0, 1.0 - max_sim)
            else:
                gap_severity = 1.0 - (max_sim / threshold) * 0.3

            gaps.append(SkillGap(
                required_skill=req_skill,
                category="",
                gap_severity=gap_severity,
                closest_match=closest if max_sim > 0.4 else None,
                similarity_score=max_sim
            ))
        
        return gaps

        # Sort by severity descending — biggest gaps first
        return sorted(gaps, key=lambda g: g.gap_severity, reverse=True)