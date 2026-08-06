# 🚀 AI/ML Resume Reviewer & Career Recommendation System

An end-to-end, production-ready **Natural Language Processing (NLP)** and **Machine Learning (ML)** web application that parses resumes (`.pdf`, `.docx`, `.txt`), calculates ATS compliance scores using **TF-IDF & Cosine Similarity**, identifies critical skill gaps, and recommends matching career roles.

Built with **FastAPI**, **Scikit-Learn**, **PyPDF / python-docx**, and a modern **Glassmorphism Web Dashboard**.

---

## 🌟 Key Features

- 📄 **Multi-Format Resume Parsing**: Extracts structured text and metadata from PDF, DOCX, and TXT files.
- 🎯 **ATS Score Engine**: Calculates weighted ATS compliance based on TF-IDF cosine similarity, section completeness, action verb density, and word count.
- 🔍 **Skills Gap Analysis**: Compares candidate skills against target job description requirements and outputs matched vs missing skill badges.
- 💡 **Actionable Feedback**: Generates customized structural and formatting suggestions.
- 🧭 **Career Recommender**: Recommends top matching job roles (ML Engineer, Data Scientist, Full Stack Dev, Cloud/DevOps) with match percentages and skill gap advice.
- 🎨 **Modern Glassmorphism UI**: Built with HTML5, Vanilla CSS, and JS with an animated circular score gauge, sub-score bars, and responsive layout.
- ☁️ **Render Ready**: Includes `render.yaml`, `Procfile`, `Dockerfile`, `requirements.txt`, and `.gitignore`.

---

## 📁 Repository Structure

```
ai-resume-reviewer/
├── app/
│   ├── __init__.py          # Package initializer
│   ├── main.py              # FastAPI Web Application & REST API Endpoints
│   ├── parser.py            # PDF / DOCX / TXT text & metadata parser
│   ├── ml_engine.py         # TF-IDF, Cosine Similarity, Skill Extraction & ATS Scoring
│   └── recommender.py       # Career role matching recommendation system
├── static/
│   ├── css/
│   │   └── style.css        # Glassmorphism visual design system
│   └── js/
│       └── main.js          # Dynamic UI logic, AJAX calls, gauge chart, badges
├── templates/
│   └── index.html           # Modern dashboard template
├── sample_data/
│   └── sample_resume.txt    # Pre-loaded sample resume for demo
├── .gitignore               # Git exclusion rules
├── Dockerfile               # Production container image configuration
├── Procfile                 # Deployment process command for web servers
├── render.yaml              # Render infrastructure blueprint file
├── requirements.txt         # Production Python dependencies
└── README.md                # Documentation & Deployment guide
```

---

## 💻 Local Setup & Execution

### 1. Clone or Download Repository
```bash
cd ai-resume-reviewer
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Open your browser and navigate to `http://localhost:8000`.

---

## 🐙 Step-by-Step GitHub Upload Guide

Follow these simple steps to upload your repository to GitHub:

### Step 1: Initialize Git Repository
In your project root directory (`ai-resume-reviewer`), run:
```bash
git init
git add .
git commit -m "Initial commit: AI Resume Reviewer & Recommendation System"
```

### Step 2: Create a New GitHub Repository
1. Go to [GitHub.com](https://github.com/) and click **New Repository**.
2. Name it `ai-resume-reviewer`.
3. Keep it **Public** (recommended for free Render deployment).
4. **Do not** check "Initialize with README" (since we already created one).
5. Click **Create repository**.

### Step 3: Connect and Push Code to GitHub
Copy the commands shown by GitHub (replace `<YOUR-USERNAME>` with your GitHub handle):
```bash
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/ai-resume-reviewer.git
git push -u origin main
```

---

## ☁️ Step-by-Step Render Hosting Guide

Deploying this app live on Render takes less than 2 minutes!

### Option A: Automatic Blueprint Deployment (Easiest)
1. Log into your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** and select **Blueprints**.
3. Connect your GitHub account and select the `ai-resume-reviewer` repository.
4. Render will automatically detect `render.yaml` and configure the web service.
5. Click **Apply**. Your app will build and deploy live!

### Option B: Manual Web Service Setup
1. Log into [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Select **Build and deploy from a Git repository** and pick your `ai-resume-reviewer` repository.
4. Fill in the deployment details:
   - **Name**: `ai-resume-reviewer`
   - **Environment**: `Python 3`
   - **Region**: Any (e.g. Oregon / Singapore)
   - **Branch**: `main`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app`
   - **Instance Type**: `Free`
5. Click **Create Web Service**.
6. Render will automatically deploy your app and give you a free live URL (e.g., `https://ai-resume-reviewer.onrender.com`).

---

## 📡 REST API Documentation

### 1. `POST /api/review`
- **Description**: Upload resume file (`file`) and optional target job description (`job_description`) to get JSON analysis.
- **Request Body** (`multipart/form-data`):
  - `file`: Resume file (`.pdf`, `.docx`, `.txt`)
  - `job_description` (optional string): Target job text.

### 2. `GET /api/sample`
- **Description**: Returns instant demo JSON output using pre-computed sample resume.

---

## 📜 License
Licensed under the [MIT License](LICENSE). Built for AI/ML job seekers and recruiters.
