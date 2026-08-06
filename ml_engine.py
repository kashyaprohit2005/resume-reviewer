import re
from typing import Dict, Any, List, Set, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Comprehensive taxonomy of skills grouped by domain
SKILL_TAXONOMY = {
    "Programming & Languages": [
        "python", "java", "c++", "c#", "javascript", "typescript", "golang", "rust", "php", "ruby", "swift", "kotlin", "scala", "r", "sql", "html", "css", "bash", "powershell"
    ],
    "Data Science & AI/ML": [
        "machine learning", "deep learning", "nlp", "natural language processing", "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "scipy", "opencv", "transformers", "huggingface", "xgboost", "lightgbm", "spacy", "nltk", "generative ai", "llm", "prompt engineering", "langchain", "tableau", "power bi", "matplotlib", "seaborn"
    ],
    "Web & Backend Development": [
        "fastapi", "flask", "django", "node.js", "express", "react", "next.js", "vue.js", "angular", "rest api", "graphql", "microservices", "spring boot", "asp.net", "tailwind css", "bootstrap", "websockets"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "terraform", "ansible", "ci/cd", "jenkins", "github actions", "gitlab ci", "linux", "nginx", "prometheus", "grafana", "helm", "serverless"
    ],
    "Databases & Storage": [
        "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "sqlite", "oracle", "sql server", "dynamodb", "cassandra", "snowflake", "bigquery", "redshift"
    ],
    "Soft Skills & Management": [
        "leadership", "communication", "problem solving", "teamwork", "agile", "scrum", "jira", "project management", "time management", "critical thinking", "collaboration", "analytical thinking", "stakeholder management"
    ]
}

ACTION_VERBS = [
    "accelerated", "achieved", "architected", "built", "spearheaded", "created", "decreased", "delivered",
    "developed", "engineered", "established", "expanded", "generated", "implemented", "improved", "increased",
    "initiated", "launched", "managed", "maximized", "optimized", "orchestrated", "overhauled", "reduced",
    "designed", "streamlined", "transformed", "led", "automated", "mentored", "revamped", "deployed"
]

class MLEngine:
    """Natural Language Processing and Machine Learning Engine for Resume Review & ATS Matching."""

    @staticmethod
    def extract_skills(text: str) -> Dict[str, List[str]]:
        """Extract matched skills from text based on taxonomy."""
        text_lower = text.lower()
        extracted_skills = {}
        all_flat_skills = []

        for category, skills in SKILL_TAXONOMY.items():
            category_matches = []
            for skill in skills:
                # Word boundary match for precise matching (avoids matching 'c' in 'cat')
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    category_matches.append(skill.title())
                    all_flat_skills.append(skill.title())
            if category_matches:
                extracted_skills[category] = category_matches

        extracted_skills["_all"] = list(set(all_flat_skills))
        return extracted_skills

    @classmethod
    def calculate_match_similarity(cls, resume_text: str, job_description: str) -> float:
        """Calculate TF-IDF Cosine Similarity percentage between resume and job description."""
        if not job_description or len(job_description.strip()) < 10:
            return 0.0

        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(float(similarity) * 100, 2)
        except Exception:
            return 0.0

    @classmethod
    def analyze_ats_compliance(cls, resume_text: str, job_description: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Compute detailed ATS compliance score, sub-scores, breakdown, and formatting suggestions."""
        # 1. Similarity Match Score (40% weight)
        tfidf_match_score = cls.calculate_match_similarity(resume_text, job_description) if job_description else 70.0

        # 2. Skill Extraction & Keyword Gap Analysis (25% weight)
        resume_skills_dict = cls.extract_skills(resume_text)
        resume_skills_set = set([s.lower() for s in resume_skills_dict.get("_all", [])])

        job_skills_dict = cls.extract_skills(job_description) if job_description else {}
        job_skills_set = set([s.lower() for s in job_skills_dict.get("_all", [])])

        matched_skills = sorted(list(resume_skills_set.intersection(job_skills_set)))
        missing_skills = sorted(list(job_skills_set - resume_skills_set))

        if job_skills_set:
            skill_match_ratio = len(matched_skills) / len(job_skills_set)
            skill_score = min(round(skill_match_ratio * 100, 1), 100.0)
        else:
            skill_score = min(len(resume_skills_set) * 5.0, 85.0)

        # 3. Section Completeness (15% weight)
        detected_sections = metadata.get("detected_sections", [])
        expected_sections = ["Education", "Experience", "Skills", "Projects"]
        found_expected = [sec for sec in expected_sections if any(sec.lower() in d.lower() for d in detected_sections)]
        section_score = round((len(found_expected) / len(expected_sections)) * 100, 1)

        # 4. Word Count & Length Appropriateness (10% weight)
        word_count = metadata.get("word_count", 0)
        if 400 <= word_count <= 1000:
            word_count_score = 100.0
        elif 250 <= word_count < 400 or 1000 < word_count <= 1500:
            word_count_score = 75.0
        else:
            word_count_score = 50.0

        # 5. Action Verbs & Impact Metrics (10% weight)
        text_lower = resume_text.lower()
        matched_verbs = [verb for verb in ACTION_VERBS if re.search(r'\b' + verb + r'\b', text_lower)]
        action_verb_score = min(round((len(matched_verbs) / 8) * 100, 1), 100.0)

        # Quantitative Metrics detection (numbers, %, $)
        metrics_found = len(re.findall(r'\b\d+%\b|\$\d+|\b\d+\+\b|\b\d+x\b', resume_text))

        # Overall Weighted Score
        if job_description:
            overall_ats_score = round(
                (tfidf_match_score * 0.40) +
                (skill_score * 0.25) +
                (section_score * 0.15) +
                (word_count_score * 0.10) +
                (action_verb_score * 0.10), 1
            )
        else:
            overall_ats_score = round(
                (skill_score * 0.35) +
                (section_score * 0.25) +
                (word_count_score * 0.20) +
                (action_verb_score * 0.20), 1
            )

        # Generate Actionable Suggestions
        suggestions = []
        if overall_ats_score < 70:
            suggestions.append("Increase keyword density matching the targeted job description in your Experience section.")
        if len(missing_skills) > 0:
            suggestions.append(f"Add critical missing job skills: {', '.join([s.title() for s in missing_skills[:5]])}.")
        if word_count < 400:
            suggestions.append("Your resume appears too short (<400 words). Add details about your projects and responsibilities.")
        elif word_count > 1000:
            suggestions.append("Your resume is over 1,000 words. Consider condensing to 1-2 focused pages.")
        if len(found_expected) < len(expected_sections):
            missing_secs = [sec for sec in expected_sections if sec not in found_expected]
            suggestions.append(f"Ensure clear section headings for: {', '.join(missing_secs)}.")
        if metrics_found < 3:
            suggestions.append("Quantify your achievements! Add metrics like '% increase', '$ cost saved', or 'X users served'.")
        if len(matched_verbs) < 5:
            suggestions.append("Use strong action verbs like 'Architected', 'Spearheaded', 'Optimized', or 'Automated'.")

        if not suggestions:
            suggestions.append("Excellent resume structure! High ATS compliance detected.")

        return {
            "overall_ats_score": overall_ats_score,
            "sub_scores": {
                "content_match": tfidf_match_score if job_description else 75.0,
                "skills_alignment": skill_score,
                "section_structure": section_score,
                "length_appropriateness": word_count_score,
                "action_oriented": action_verb_score
            },
            "skills_extracted": resume_skills_dict,
            "matched_skills": [s.title() for s in matched_skills],
            "missing_skills": [s.title() for s in missing_skills],
            "action_verbs_used": [v.title() for v in matched_verbs],
            "metrics_count": metrics_found,
            "suggestions": suggestions
        }
