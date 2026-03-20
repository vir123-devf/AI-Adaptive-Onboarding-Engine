import networkx as nx
import json
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class CourseNode:
    id: str
    title: str
    skills_covered: list[str]
    prerequisites: list[str]  # course IDs
    duration_hours: float
    difficulty: str  # "beginner" | "intermediate" | "advanced"
    domain: str  # for cross-domain scalability
    url: str = ""


@dataclass
class LearningPathway:
    ordered_courses: list[CourseNode]
    total_hours: float
    skill_coverage: dict[str, bool]  # skill → covered?
    reasoning_trace: list[str]  # step-by-step why each course was chosen


class AdaptivePather:
    def __init__(self, catalog_path: str = "course_catalog.json"):
        self.catalog: dict[str, CourseNode] = {}
        self.skill_to_courses: dict[str, list[str]] = {}  # inverted index
        self._load_catalog(catalog_path)

    def _load_catalog(self, path: str):
        # Try the provided path first, then try with "data/" prefix
        try:
            data = json.loads(Path(path).read_text())
        except FileNotFoundError:
            alt_path = f"data/{path}"
            data = json.loads(Path(alt_path).read_text())
        for item in data["courses"]:
            node = CourseNode(**item)
            self.catalog[node.id] = node
            for skill in node.skills_covered:
                self.skill_to_courses.setdefault(skill.lower(), []).append(node.id)

    def build_pathway(
            self,
            gaps: list,  # list[SkillGap] from GapAnalyzer
            max_hours: float = 40.0,
            difficulty_cap: str = "advanced"
    ) -> LearningPathway:
        """
        Core adaptive algorithm:
        1. Select minimal course set covering all skill gaps (greedy set cover)
        2. Build prerequisite DAG
        3. Topological sort to get valid learning order
        4. Prune by difficulty cap and time budget
        """
        trace = []
        difficulty_order = {"beginner": 0, "intermediate": 1, "advanced": 2}
        diff_cap = difficulty_order.get(difficulty_cap, 2)

        # Step 1: Greedy course selection (maximize gap coverage per hour)
        uncovered_gaps = {g.required_skill.lower(): g.gap_severity
                          for g in gaps if g.gap_severity > 0.2}
        selected_course_ids: set[str] = set()

        trace.append(f"Identified {len(uncovered_gaps)} skill gaps requiring coverage.")

        while uncovered_gaps:
            best_course_id = None
            best_score = -1.0

            for course_id, course in self.catalog.items():
                if course_id in selected_course_ids:
                    continue
                if difficulty_order.get(course.difficulty, 0) > diff_cap:
                    continue

                # Score = weighted gap coverage / duration (efficiency metric)
                coverage = sum(
                    uncovered_gaps.get(s.lower(), 0)
                    for s in course.skills_covered
                )
                if coverage > 0:
                    score = coverage / max(course.duration_hours, 0.5)
                    if score > best_score:
                        best_score = score
                        best_course_id = course_id

            if best_course_id is None:
                break  # No more courses can cover remaining gaps

            course = self.catalog[best_course_id]
            selected_course_ids.add(best_course_id)

            newly_covered = [s for s in course.skills_covered
                             if s.lower() in uncovered_gaps]
            for skill in newly_covered:
                uncovered_gaps.pop(skill.lower(), None)

            trace.append(
                f"Selected '{course.title}' (score={best_score:.2f}): "
                f"covers {newly_covered} — {len(uncovered_gaps)} gaps remain."
            )

        # Step 2: Resolve prerequisites — add required courses not yet selected
        to_resolve = list(selected_course_ids)
        while to_resolve:
            course_id = to_resolve.pop()
            course = self.catalog.get(course_id)
            if not course:
                continue
            for prereq_id in course.prerequisites:
                if prereq_id not in selected_course_ids and prereq_id in self.catalog:
                    selected_course_ids.add(prereq_id)
                    to_resolve.append(prereq_id)
                    trace.append(f"Added prerequisite '{self.catalog[prereq_id].title}' required by '{course.title}'.")

        # Step 3: Build DAG and topological sort
        G = nx.DiGraph()
        for course_id in selected_course_ids:
            G.add_node(course_id)
            for prereq_id in self.catalog[course_id].prerequisites:
                if prereq_id in selected_course_ids:
                    G.add_edge(prereq_id, course_id)  # prereq → course

        try:
            ordered_ids = list(nx.topological_sort(G))
        except nx.NetworkXUnfeasible:
            # Cycle detected (shouldn't happen with well-formed catalog)
            ordered_ids = list(selected_course_ids)
            trace.append("Warning: Cycle in prerequisites detected, using unordered fallback.")

        # Step 4: Apply time budget constraint
        final_courses = []
        total_hours = 0.0
        for cid in ordered_ids:
            course = self.catalog[cid]
            if total_hours + course.duration_hours <= max_hours:
                final_courses.append(course)
                total_hours += course.duration_hours

        trace.append(f"Final pathway: {len(final_courses)} courses, {total_hours:.1f}h total.")

        # Build skill coverage map
        all_required = {g.required_skill.lower() for g in gaps}
        covered = {s.lower() for c in final_courses for s in c.skills_covered}
        skill_coverage = {skill: (skill in covered) for skill in all_required}

        return LearningPathway(
            ordered_courses=final_courses,
            total_hours=total_hours,
            skill_coverage=skill_coverage,
            reasoning_trace=trace
        )