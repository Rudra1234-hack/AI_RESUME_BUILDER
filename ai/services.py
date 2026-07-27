import os
import requests
from django.conf import settings

def improve_resume_text(input_text, section_type="general"):
    """
    Improves input text using OpenAI API or falls back to a smart local phrased engine.
    """
    api_key = getattr(settings, 'OPENAI_API_KEY', '')
    
    if api_key:
        try:
            # Call OpenAI Chat Completion API
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            prompt = (
                f"You are an expert resume writer and recruiter. Optimize the following text for a resume "
                f"section of type '{section_type}'. Make it highly professional, active, action-oriented, "
                f"and ATS-friendly. Keep it concise (1-2 sentences or bullet points). Do not add any conversational text.\n\n"
                f"Original Text: {input_text}\n\n"
                f"Optimized Professional Text:"
            )
            data = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 150
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                improved_text = result['choices'][0]['message']['content'].strip()
                # Clean up wrapping quotes if any
                if improved_text.startswith('"') and improved_text.endswith('"'):
                    improved_text = improved_text[1:-1]
                return improved_text
        except Exception as e:
            # Fallback to local mock on network error
            pass

    # --- Smart Local Mock Phrasing Engine ---
    text_lower = input_text.lower()
    
    # Career Objective Fallbacks
    if section_type == "objective":
        if "student" in text_lower or "fresher" in text_lower:
            return "Detail-oriented and passionate aspiring software engineer looking to leverage strong academic foundations in computer science and hands-on project experience to solve real-world problems in a collaborative team."
        if "developer" in text_lower or "engineer" in text_lower or "coder" in text_lower:
            return "Innovative and results-driven Software Engineer with a proven track record of developing scalable web applications, optimizing databases, and collaborating with cross-functional teams to deliver high-quality code."
        return f"Dedicated professional seeking to leverage skills in {input_text.strip()} to drive success, optimize operational workflows, and contribute value within a growth-oriented organization."

    # Projects / Experience Fallbacks
    if "ecommerce" in text_lower or "e-commerce" in text_lower or "shopping" in text_lower:
        return "Engineered a high-performance e-commerce platform incorporating secure user authentication, responsive UI layouts, and structured database transactions, resulting in improved checkout efficiency."
    if "portfolio" in text_lower or "website" in text_lower:
        return "Designed and deployed a responsive personal portfolio website showcasing projects and technical skills, optimized for cross-browser compatibility and quick page load times."
    if "database" in text_lower or "sql" in text_lower:
        return "Designed and optimized complex relational database schemas, writing efficient queries and indexing strategies that reduced data retrieval latency by 30%."
    if "android" in text_lower or "ios" in text_lower or "app" in text_lower:
        return "Developed and published a user-centric mobile application using modern design patterns, integrating RESTful APIs and local storage for seamless offline access."
    if "python" in text_lower or "django" in text_lower:
        return f"Developed a scalable web application utilizing the Django framework, implementing robust model-view-template architectures and secure authentication pipelines."
    
    # Generic phrasing improvement
    words = input_text.strip().split()
    if len(words) > 0:
        # Capitalize and add active verb
        first_word = words[0].lower()
        active_verbs = {
            "made": "Designed and implemented",
            "built": "Engineered and deployed",
            "did": "Executed and managed",
            "worked": "Collaborated on the development of",
            "helped": "Assisted in optimizing",
            "wrote": "Authored clean, maintainable code for",
            "created": "Developed and launched",
        }
        
        replacement = active_verbs.get(first_word, "Led the design, implementation, and optimization of")
        remaining_text = " ".join(words[1:]) if len(words) > 1 else " ".join(words)
        
        return f"{replacement} {remaining_text.lower()} to enhance system performance, security, and user experience."

    return "Detail-oriented professional dedicated to driving project success, executing clean development standards, and optimizing code quality."
