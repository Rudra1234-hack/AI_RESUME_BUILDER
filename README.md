# ResumeHero AI

ResumeHero AI is a production-quality, modern ATS-friendly AI-powered Resume Builder designed for students, freshers, and professionals. It helps users build resumes, optimize content using a smart AI phrasing generator, calculate real-time ATS scores, and download recruiter-ready PDF templates.

## Tech Stack
- **Backend:** Python 3.12+ / Django 5+
- **Frontend:** HTML5, Vanilla CSS3 (Glassmorphism theme), JavaScript (ES6), Bootstrap 5 (CDN)
- **Database:** SQLite
- **PDF Generation:** ReportLab
- **AI Integration:** OpenAI API (with a seamless local phrasing generator fallback)

## Features
1. **Interactive Resume Wizard:** A clean step-by-step editor covering Personal Details, Career Objectives, Education, Skills, Projects, Experience, Certifications, and Languages.
2. **AI Phrasing Enhancer:** Dynamic inline buttons to elevate description blocks using professional action verbs.
3. **Live ATS Calculator & Tips:** Custom rating system out of 100 with actionable feedback tips for database indexing.
4. **Recruiter-Optimized PDF Export:** Clean, lightweight single-column layouts designed to parse perfectly through ATS scanners.

## Getting Started

### Prerequisites
Make sure Python 3.12+ is installed on your system.

### Installation
1. Clone or navigate to the project directory:
   ```bash
   cd c:/Users/Dell/Desktop/AI_Resume_Builder
   ```
2. (Optional but recommended) Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install standard requirements:
   ```bash
   pip install Django pillow reportlab requests
   ```

### Setup & Run
1. Run database migrations to initialize tables:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Start the local development server:
   ```bash
   python manage.py runserver
   ```
3. Open `http://127.0.0.1:8000` in your web browser.

### Configuring AI Assistant (Optional)
To enable the actual OpenAI GPT-4o-mini integration, configure your API key in your shell:
- **Windows PowerShell:**
  ```powershell
  $env:OPENAI_API_KEY="your-api-key-here"
  ```
- **Windows Command Prompt:**
  ```cmd
  set OPENAI_API_KEY="your-api-key-here"
  ```
- **Linux/macOS:**
  ```bash
  export OPENAI_API_KEY="your-api-key-here"
  ```
If no key is provided, the application will automatically fall back to its local rule-based professional phrasing engine so all features remain functional.
