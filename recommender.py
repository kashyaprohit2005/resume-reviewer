from typing import List, Dict, Any

# Knowledge Base of standard tech roles and their core required skills
JOB_ROLE_PROFILES = [
    {
        "title": "Machine Learning Engineer",
        "category": "AI & Data",
        "description": "Designs, builds, and deploys scalable ML models and AI pipelines.",
        "required_skills": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "docker", "rest api", "sql", "git"],
        "recommended_courses": ["Stanford Machine Learning (Coursera)", "DeepLearning.AI Specialization", "AWS Certified Machine Learning - Specialty"]
    },
    {
        "title": "Data Scientist",
        "category": "AI & Data",
        "description": "Analyzes complex datasets to extract insights, build predictive models, and drive decisions.",
        "required_skills": ["python", "r", "sql", "pandas", "numpy", "scikit-learn", "tableau", "power bi", "statistics", "machine learning"],
        "recommended_courses": ["Google Data Analytics Professional Certificate", "IBM Data Science Professional", "Kaggle Competitions Practice"]
    },
    {
        "title": "Full Stack Web Developer",
        "category": "Software Engineering",
        "description": "Develops complete end-to-end web applications combining frontend UIs and backend APIs.",
        "required_skills": ["javascript", "typescript", "react", "node.js", "html", "css", "postgresql", "mongodb", "rest api", "git", "docker"],
        "recommended_courses": ["The Complete Web Development Bootcamp (Udemy)", "Full Stack Open (University of Helsinki)"]
    },
    {
        "title": "Backend Software Engineer",
        "category": "Software Engineering",
        "description": "Architects high-performance server-side logic, microservices, databases, and APIs.",
        "required_skills": ["python", "fastapi", "django", "java", "golang", "postgresql", "redis", "docker", "microservices", "sql", "rest api"],
        "recommended_courses": ["Designing Data-Intensive Applications", "AWS Certified Developer Associate"]
    },
    {
        "title": "DevOps & Cloud Engineer",
        "category": "Infrastructure",
        "description": "Automates CI/CD deployment pipelines, manages cloud infrastructure, and enforces reliability.",
        "required_skills": ["aws", "azure", "docker", "kubernetes", "terraform", "ansible", "ci/cd", "linux", "bash", "python", "jenkins"],
        "recommended_courses": ["AWS Certified Solutions Architect Associate", "Certified Kubernetes Administrator (CKA)"]
    },
    {
        "title": "Data Engineer",
        "category": "AI & Data",
        "description": "Builds robust ETL pipelines, data warehouses, and data infrastructure.",
        "required_skills": ["python", "sql", "spark", "hadoop", "postgresql", "snowflake", "bigquery", "airflow", "docker", "aws"],
        "recommended_courses": ["Data Engineering with Google Cloud Professional", "Data Engineering Nanodegree (Udacity)"]
    },
    {
        "title": "Frontend Engineer",
        "category": "Software Engineering",
        "description": "Crafts responsive, modern, user-focused web interfaces and interactive components.",
        "required_skills": ["javascript", "typescript", "react", "next.js", "vue.js", "html", "css", "tailwind css", "figma"],
        "recommended_courses": ["Meta Frontend Developer Professional Certificate", "Frontend Masters Core Path"]
    }
]


class CareerRecommender:
    """Recommendation Engine matching candidate skill profiles to targeted job roles."""

    @staticmethod
    def recommend_roles(candidate_skills: List[str]) -> List[Dict[str, Any]]:
        """Calculate match score for each role profile and recommend top matches."""
        candidate_skills_lower = set([s.lower() for s in candidate_skills])
        recommendations = []

        for role in JOB_ROLE_PROFILES:
            req_set = set(role["required_skills"])
            matched = candidate_skills_lower.intersection(req_set)
            missing = req_set - candidate_skills_lower

            match_percentage = round((len(matched) / len(req_set)) * 100, 1) if req_set else 0

            recommendations.append({
                "title": role["title"],
                "category": role["category"],
                "description": role["description"],
                "match_percentage": match_percentage,
                "matched_skills_count": len(matched),
                "required_skills_count": len(req_set),
                "matching_skills": sorted([s.title() for s in matched]),
                "missing_skills_to_learn": sorted([s.title() for s in missing]),
                "recommended_learning": role["recommended_courses"]
            })

        # Sort recommendations by highest match score
        recommendations.sort(key=lambda x: x["match_percentage"], reverse=True)
        return recommendations[:4] # Return top 4 matching roles
