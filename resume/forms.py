from django import forms
from .models import Resume, Education, Skill, Project, Experience, Certificate, Language

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'email', 'phone', 'address', 'linkedin', 'github', 'portfolio', 'photo', 'objective']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Full Name', 'id': 'id_resume_full_name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Email Address', 'id': 'id_resume_email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Phone Number', 'id': 'id_resume_phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 2, 'placeholder': 'Full Address', 'id': 'id_resume_address'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'LinkedIn URL', 'id': 'id_resume_linkedin'}),
            'github': forms.URLInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'GitHub URL', 'id': 'id_resume_github'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Portfolio URL', 'id': 'id_resume_portfolio'}),
            'photo': forms.FileInput(attrs={'class': 'form-control form-control-custom', 'id': 'id_resume_photo'}),
            'objective': forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 3, 'placeholder': 'Brief professional summary or career goal', 'id': 'id_resume_objective'}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['college', 'degree', 'branch', 'cgpa', 'passing_year']
        widgets = {
            'college': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Institution/College Name', 'id': 'id_edu_college'}),
            'degree': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., Bachelor of Technology', 'id': 'id_edu_degree'}),
            'branch': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., Computer Science', 'id': 'id_edu_branch'}),
            'cgpa': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., 9.2 or 85%', 'id': 'id_edu_cgpa'}),
            'passing_year': forms.NumberInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., 2026', 'id': 'id_edu_passing_year'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'name']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select form-control-custom', 'id': 'id_skill_category'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., Python, Docker, UI/UX', 'id': 'id_skill_name'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'technologies', 'description', 'github', 'live_link']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Project Name', 'id': 'id_project_name'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., Django, SQLite, CSS3', 'id': 'id_project_technologies'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 3, 'placeholder': 'What did you build? Explain clearly.', 'id': 'id_project_description'}),
            'github': forms.URLInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'GitHub Repository URL', 'id': 'id_project_github'}),
            'live_link': forms.URLInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Live Demo URL (Optional)', 'id': 'id_project_live_link'}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'role', 'duration', 'description']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Company Name', 'id': 'id_exp_company'}),
            'role': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., Software Engineer Intern', 'id': 'id_exp_role'}),
            'duration': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., June 2024 - Present', 'id': 'id_exp_duration'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 3, 'placeholder': 'Your key tasks and achievements.', 'id': 'id_exp_description'}),
        }

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'organization', 'year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Certification Title', 'id': 'id_cert_name'}),
            'organization': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Issuing Organization', 'id': 'id_cert_organization'}),
            'year': forms.NumberInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., 2025', 'id': 'id_cert_year'}),
        }

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language']
        widgets = {
            'language': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'e.g., English, Spanish', 'id': 'id_lang_language'}),
        }
