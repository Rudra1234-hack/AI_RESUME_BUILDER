from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import Resume, Education, Skill, Project, Experience, Certificate, Language
from .forms import ResumeForm, EducationForm, SkillForm, ProjectForm, ExperienceForm, CertificateForm, LanguageForm
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import json

# ATS Score Calculation and Tips
def calculate_ats_score_and_tips(resume):
    score = 0
    tips = []
    
    # 1. Personal Information & Format (Max 25 pts)
    personal_score = 0
    contact_fields = []
    if resume.full_name:
        personal_score += 5
    else:
        contact_fields.append("Full Name")
    if resume.email:
        personal_score += 5
    else:
        contact_fields.append("Email")
    if resume.phone:
        personal_score += 5
    else:
        contact_fields.append("Phone")
    if resume.linkedin or resume.github:
        personal_score += 5
    else:
        contact_fields.append("LinkedIn/GitHub")
    if resume.address:
        personal_score += 5
    else:
        contact_fields.append("Address")
        
    score += personal_score
    if contact_fields:
        tips.append({
            'section': 'Contact Info',
            'text': f"Add missing details: {', '.join(contact_fields)} to help recruiters reach you."
        })
    else:
        tips.append({
            'section': 'Contact Info',
            'text': "✔ Perfect! All contact channels and professional profiles are fully set up."
        })
        
    # 2. Career Objective (Max 15 pts)
    if resume.objective:
        objective_words = len(resume.objective.split())
        if objective_words < 15:
            score += 8
            tips.append({
                'section': 'Objective',
                'text': "Objective is too brief. Expand it to describe your goals and main technologies."
            })
        elif objective_words > 60:
            score += 10
            tips.append({
                'section': 'Objective',
                'text': "Objective is too long (keep under 60 words). Make it more concise."
            })
        else:
            score += 15
            tips.append({
                'section': 'Objective',
                'text': "✔ Career objective is concise, well-phrased, and matches recommended length."
            })
    else:
        tips.append({
            'section': 'Objective',
            'text': "Add a professional career summary or objective to state your target role."
        })
        
    # 3. Education (Max 15 pts)
    educations = resume.educations.all()
    if educations.exists():
        score += 15
        tips.append({
            'section': 'Education',
            'text': f"✔ List of {educations.count()} academic qualification(s) is properly indexed."
        })
    else:
        tips.append({
            'section': 'Education',
            'text': "Add your high school, college, or university degree information."
        })
        
    # 4. Skills (Max 20 pts)
    skills = resume.skills.all()
    if skills.exists():
        score += 10
        if skills.count() >= 5:
            score += 10
            tips.append({
                'section': 'Skills',
                'text': f"✔ Perfect! You have listed {skills.count()} skills across technical categories."
            })
        else:
            score += 5
            tips.append({
                'section': 'Skills',
                'text': "Add at least 5 technical or soft skills to optimize database keywords."
            })
    else:
        tips.append({
            'section': 'Skills',
            'text': "Define skills categories (Programming Languages, Databases, Tools) to match job descriptions."
        })
        
    # 5. Projects (Max 15 pts)
    projects = resume.projects.all()
    if projects.exists():
        score += 10
        # Check descriptions
        long_desc = all(len(p.description.split()) > 10 for p in projects)
        tech_listed = all(len(p.technologies) > 0 for p in projects)
        if long_desc and tech_listed:
            score += 5
            tips.append({
                'section': 'Projects',
                'text': "✔ Excellent project descriptions featuring technologies and clear achievements."
            })
        else:
            tips.append({
                'section': 'Projects',
                'text': "Include technologies used and expand descriptions to state your specific contribution."
            })
    else:
        tips.append({
            'section': 'Projects',
            'text': "Add at least 1-2 projects to showcase your practical application of skills."
        })
        
    # 6. Experience (Max 10 pts)
    experiences = resume.experiences.all()
    if experiences.exists():
        score += 10
        tips.append({
            'section': 'Experience',
            'text': f"✔ Professional experience shows active work duration of {experiences.count()} job role(s)."
        })
    else:
        # Don't penalize freshers heavily, but nudge them
        score += 5
        tips.append({
            'section': 'Experience',
            'text': "If you have prior internships, freelance work, or club roles, list them here."
        })
        
    # 7. Additional Sections: Certifications & Languages (Max 5 pts)
    has_cert = resume.certificates.exists()
    has_lang = resume.languages.exists()
    if has_cert or has_lang:
        score += 5
        tips.append({
            'section': 'Languages & Certs',
            'text': "✔ Additional credentials (languages/certifications) add value to your resume profile."
        })
    else:
        tips.append({
            'section': 'Languages & Certs',
            'text': "Include known languages and professional certifications to boost profile weight."
        })
        
    return {
        'overall_score': min(score, 100),
        'tips': tips
    }

from django.core.exceptions import PermissionDenied

# Calculate completion percentage
def calculate_completion_percentage(resume):
    filled_sections = 0
    total_sections = 7 # Personal info, Objective, Education, Skills, Projects, Experience, Certifications/Languages
    
    if resume.full_name and resume.email and resume.phone:
        filled_sections += 1
    if resume.objective:
        filled_sections += 1
    if resume.educations.exists():
        filled_sections += 1
    if resume.skills.exists():
        filled_sections += 1
    if resume.projects.exists():
        filled_sections += 1
    if resume.experiences.exists():
        filled_sections += 1
    if resume.certificates.exists() or resume.languages.exists():
        filled_sections += 1
        
    return int((filled_sections / total_sections) * 100)

@login_required
@require_POST
def create_resume(request):
    title = request.POST.get('title', 'My Professional Resume').strip() or 'My Professional Resume'
    target_role = request.POST.get('target_role', '').strip()
    
    resume = Resume.objects.create(
        user=request.user,
        title=title,
        target_role=target_role,
        email=request.user.email,
        full_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
    )
    messages.success(request, "New draft resume initialized!")
    return redirect('builder_wizard', resume_id=resume.id)

@login_required
def builder_wizard(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if resume.user != request.user:
        raise PermissionDenied()
        
    # Prepare individual forms for editing
    resume_form = ResumeForm(instance=resume)
    education_form = EducationForm()
    skill_form = SkillForm()
    project_form = ProjectForm()
    experience_form = ExperienceForm()
    certificate_form = CertificateForm()
    language_form = LanguageForm()
    
    context = {
        'resume': resume,
        'resume_form': resume_form,
        'education_form': education_form,
        'skill_form': skill_form,
        'project_form': project_form,
        'experience_form': experience_form,
        'certificate_form': certificate_form,
        'language_form': language_form,
        'educations': resume.educations.all(),
        'skills': resume.skills.all(),
        'projects': resume.projects.all(),
        'experiences': resume.experiences.all(),
        'certificates': resume.certificates.all(),
        'languages': resume.languages.all(),
    }
    return render(request, 'resume/builder.html', context)

@login_required
@require_POST
def auto_save_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if resume.user != request.user:
        raise PermissionDenied()
        
    # Get standard fields and update
    resume.full_name = request.POST.get('full_name', resume.full_name)
    resume.email = request.POST.get('email', resume.email)
    resume.phone = request.POST.get('phone', resume.phone)
    resume.address = request.POST.get('address', resume.address)
    resume.linkedin = request.POST.get('linkedin', resume.linkedin)
    resume.github = request.POST.get('github', resume.github)
    resume.portfolio = request.POST.get('portfolio', resume.portfolio)
    resume.objective = request.POST.get('objective', resume.objective)
    
    if 'photo' in request.FILES:
        resume.photo = request.FILES['photo']
        
    resume.save()
    
    # Recalculate score & completion
    ats_data = calculate_ats_score_and_tips(resume)
    resume.ats_score = ats_data['overall_score']
    resume.completion_percentage = calculate_completion_percentage(resume)
    resume.save()
    
    return JsonResponse({
        'status': 'success',
        'ats_score': ats_data['overall_score']
    })

# dynamic additions
@login_required
@require_POST
def add_item_ajax(request, item_type, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if resume.user != request.user:
        raise PermissionDenied()
        
    if item_type == 'education':
        form = EducationForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.resume = resume
            item.save()
            resume.completion_percentage = calculate_completion_percentage(resume)
            ats_data = calculate_ats_score_and_tips(resume)
            resume.ats_score = ats_data['overall_score']
            resume.save()
            return JsonResponse({
                'status': 'success',
                'id': item.id,
                'html': f"<tr id='education-row-{item.id}' class='border-bottom border-secondary border-opacity-5'><td class='py-3 px-4 text-white'>{item.college}</td><td class='py-3 text-secondary'>{item.degree}</td><td class='py-3 text-secondary'>{item.branch}</td><td class='py-3 text-secondary'>{item.cgpa}</td><td class='py-3 text-secondary'>{item.passing_year}</td><td class='py-3 text-center'><button onclick='deleteItem({item.id}, \"education\")' class='btn btn-outline-danger btn-sm border-0'><i class='bi bi-trash'></i></button></td></tr>"
            })
    elif item_type == 'skill':
        form = SkillForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.resume = resume
            item.save()
            resume.completion_percentage = calculate_completion_percentage(resume)
            ats_data = calculate_ats_score_and_tips(resume)
            resume.ats_score = ats_data['overall_score']
            resume.save()
            return JsonResponse({
                'status': 'success',
                'id': item.id,
                'html': f"<div class='badge bg-secondary bg-opacity-20 text-secondary border border-secondary border-opacity-30 p-2.5 d-inline-flex align-items-center gap-2' id='skill-{item.id}' style='font-size:0.85rem; border-radius:8px;'>{item.name} ({item.get_category_display()})<i onclick='deleteItem({item.id}, \"skill\")' class='bi bi-x-circle text-danger pointer-cursor' style='cursor:pointer; font-size:1rem;'></i></div>"
            })
    elif item_type == 'project':
        form = ProjectForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.resume = resume
            item.save()
            resume.completion_percentage = calculate_completion_percentage(resume)
            ats_data = calculate_ats_score_and_tips(resume)
            resume.ats_score = ats_data['overall_score']
            resume.save()
            return JsonResponse({
                'status': 'success',
                'id': item.id,
                'html': f"<div class='p-3 rounded mb-3 border border-secondary border-opacity-10 d-flex justify-content-between align-items-start' id='project-{item.id}' style='background:rgba(255,255,255,0.01);'><div class='text-start'><h6 class='text-white fw-bold mb-1'>{item.name}</h6><p class='text-muted small mb-2'><i class='bi bi-cpu text-primary me-1'></i> Technologies: {item.technologies}</p><p class='text-secondary small mb-0'>{item.description}</p></div><button onclick='deleteItem({item.id}, \"project\")' class='btn btn-outline-danger btn-sm border-0'><i class='bi bi-trash'></i></button></div>"
            })
    elif item_type == 'experience':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.resume = resume
            item.save()
            resume.completion_percentage = calculate_completion_percentage(resume)
            ats_data = calculate_ats_score_and_tips(resume)
            resume.ats_score = ats_data['overall_score']
            resume.save()
            return JsonResponse({
                'status': 'success',
                'id': item.id,
                'html': f"<div class='p-3 rounded mb-3 border border-secondary border-opacity-10 d-flex justify-content-between align-items-start' id='experience-{item.id}' style='background:rgba(255,255,255,0.01);'><div class='text-start'><h6 class='text-white fw-bold mb-1'>{item.role} at {item.company}</h6><p class='text-muted small mb-2'><i class='bi bi-calendar3 text-primary me-1'></i> Duration: {item.duration}</p><p class='text-secondary small mb-0'>{item.description}</p></div><button onclick='deleteItem({item.id}, \"experience\")' class='btn btn-outline-danger btn-sm border-0'><i class='bi bi-trash'></i></button></div>"
            })
    elif item_type == 'certificate':
        form = CertificateForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.resume = resume
            item.save()
            resume.completion_percentage = calculate_completion_percentage(resume)
            ats_data = calculate_ats_score_and_tips(resume)
            resume.ats_score = ats_data['overall_score']
            resume.save()
            return JsonResponse({
                'status': 'success',
                'id': item.id,
                'html': f"<div class='p-3 rounded mb-3 border border-secondary border-opacity-10 d-flex justify-content-between align-items-center' id='certificate-{item.id}' style='background:rgba(255,255,255,0.01);'><span class='text-white'>{item.name} - {item.organization} ({item.year})</span><button onclick='deleteItem({item.id}, \"certificate\")' class='btn btn-outline-danger btn-sm border-0'><i class='bi bi-trash'></i></button></div>"
            })
    elif item_type == 'language':
        form = LanguageForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.resume = resume
            item.save()
            resume.completion_percentage = calculate_completion_percentage(resume)
            ats_data = calculate_ats_score_and_tips(resume)
            resume.ats_score = ats_data['overall_score']
            resume.save()
            return JsonResponse({
                'status': 'success',
                'id': item.id,
                'html': f"<div class='badge bg-info bg-opacity-15 text-info border border-info border-opacity-25 p-2.5 d-inline-flex align-items-center gap-2' id='language-{item.id}' style='font-size:0.85rem; border-radius:8px;'>{item.language}<i onclick='deleteItem({item.id}, \"language\")' class='bi bi-x-circle text-danger pointer-cursor' style='cursor:pointer; font-size:1rem;'></i></div>"
            })
            
    return JsonResponse({'error': 'Invalid request or validation failed.'}, status=400)

@login_required
@require_POST
def delete_item_ajax(request, item_type, item_id, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if resume.user != request.user:
        raise PermissionDenied()
        
    try:
        if item_type == 'education':
            item = get_object_or_404(Education, id=item_id, resume=resume)
        elif item_type == 'skill':
            item = get_object_or_404(Skill, id=item_id, resume=resume)
        elif item_type == 'project':
            item = get_object_or_404(Project, id=item_id, resume=resume)
        elif item_type == 'experience':
            item = get_object_or_404(Experience, id=item_id, resume=resume)
        elif item_type == 'certificate':
            item = get_object_or_404(Certificate, id=item_id, resume=resume)
        elif item_type == 'language':
            item = get_object_or_404(Language, id=item_id, resume=resume)
        else:
            return JsonResponse({'error': 'Invalid item type.'}, status=404)
            
        item.delete()
        resume.completion_percentage = calculate_completion_percentage(resume)
        ats_data = calculate_ats_score_and_tips(resume)
        resume.ats_score = ats_data['overall_score']
        resume.save()
        return JsonResponse({
            'status': 'success',
            'ats_score': ats_data['overall_score']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def resume_preview(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    context = {
        'resume': resume,
        'educations': resume.educations.all(),
        'skills': resume.skills.all(),
        'projects': resume.projects.all(),
        'experiences': resume.experiences.all(),
        'certificates': resume.certificates.all(),
        'languages': resume.languages.all(),
    }
    return render(request, 'resume/preview.html', context)

@login_required
def generate_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Create the HTTP response with PDF headers
    response = HttpResponse(content_type='application/pdf')
    # Use inline instead of attachment so the browser opens/shows the PDF directly
    filename = f"{resume.full_name or 'Resume'}_ATS_Resume.pdf".replace(" ", "_")
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    
    # Setup document template (A4, small margins for single page fit if possible)
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        alignment=1, # Centered
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#475569'),
        alignment=1, # Centered
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=colors.HexColor('#1e3a8a'), # Dark Blue
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4
    )
    
    bold_body_style = ParagraphStyle(
        'DocBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    # --- 1. Header (Name & Contacts) ---
    story.append(Paragraph(resume.full_name or "YOUR NAME", title_style))
    
    contacts = []
    if resume.email:
        contacts.append(resume.email)
    if resume.phone:
        contacts.append(resume.phone)
    if resume.address:
        contacts.append(resume.address)
    
    contact_str = "  |  ".join(contacts)
    story.append(Paragraph(contact_str, subtitle_style))
    
    # Social profile links
    socials = []
    if resume.linkedin:
        socials.append(f"LinkedIn: {resume.linkedin}")
    if resume.github:
        socials.append(f"GitHub: {resume.github}")
    if resume.portfolio:
        socials.append(f"Portfolio: {resume.portfolio}")
        
    if socials:
        socials_str = "  |  ".join(socials)
        story.append(Paragraph(socials_str, ParagraphStyle('Socials', parent=subtitle_style, spaceAfter=8)))
        
    def add_section_divider(title):
        # Adds section heading and a neat thin border beneath it
        story.append(Paragraph(title.upper(), heading_style))
        # Draw line using Table
        t = Table([['']], colWidths=[523], rowHeights=[1])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1.5, colors.HexColor('#3b82f6')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))
        
    # --- 2. Objective ---
    if resume.objective:
        add_section_divider("Career Objective")
        story.append(Paragraph(resume.objective, body_style))
        story.append(Spacer(1, 4))
        
    # --- 3. Experience ---
    experiences = resume.experiences.all()
    if experiences.exists():
        add_section_divider("Professional Experience")
        for exp in experiences:
            # Table layout for Job Title and duration
            exp_data = [
                [Paragraph(f"<b>{exp.role}</b>", body_style), Paragraph(exp.duration, ParagraphStyle('Dur', parent=body_style, alignment=2))]
            ]
            t = Table(exp_data, colWidths=[380, 143])
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('TOPPADDING', (0,0), (-1,-1), 2),
            ]))
            story.append(t)
            story.append(Paragraph(f"<i>{exp.company}</i>", body_style))
            story.append(Paragraph(exp.description, body_style))
            story.append(Spacer(1, 3))
            
    # --- 4. Projects ---
    projects = resume.projects.all()
    if projects.exists():
        add_section_divider("Projects")
        for proj in projects:
            proj_header = [
                [Paragraph(f"<b>{proj.name}</b> | <i>{proj.technologies}</i>", body_style), 
                 Paragraph(f"<a href='{proj.github}' color='#3b82f6'>GitHub</a>" if proj.github else "", ParagraphStyle('ProjL', parent=body_style, alignment=2))]
            ]
            t = Table(proj_header, colWidths=[400, 123])
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
            ]))
            story.append(t)
            story.append(Paragraph(proj.description, body_style))
            story.append(Spacer(1, 3))
            
    # --- 5. Education ---
    educations = resume.educations.all()
    if educations.exists():
        add_section_divider("Education")
        for edu in educations:
            edu_data = [
                [Paragraph(f"<b>{edu.degree}</b> {f'in {edu.branch}' if edu.branch else ''}", body_style), 
                 Paragraph(str(edu.passing_year), ParagraphStyle('PassY', parent=body_style, alignment=2))]
            ]
            t = Table(edu_data, colWidths=[430, 93])
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
            ]))
            story.append(t)
            story.append(Paragraph(f"{edu.college} | CGPA/Score: <b>{edu.cgpa}</b>", body_style))
            story.append(Spacer(1, 3))
            
    # --- 6. Skills ---
    skills = resume.skills.all()
    if skills.exists():
        add_section_divider("Technical Skills")
        
        # Group skills by category
        categories = {
            'languages': 'Programming Languages',
            'frameworks': 'Frameworks',
            'databases': 'Databases',
            'tools': 'Tools',
            'soft_skills': 'Soft Skills'
        }
        
        grouped_skills = {}
        for skill in skills:
            cat_name = categories.get(skill.category, 'Other')
            if cat_name not in grouped_skills:
                grouped_skills[cat_name] = []
            grouped_skills[cat_name].append(skill.name)
            
        for cat, items in grouped_skills.items():
            skill_line = f"<b>{cat}:</b> {', '.join(items)}"
            story.append(Paragraph(skill_line, body_style))
            
        story.append(Spacer(1, 4))
        
    # --- 7. Certifications & Languages (Two-column layout to save space) ---
    certs = resume.certificates.all()
    langs = resume.languages.all()
    
    if certs.exists() or langs.exists():
        add_section_divider("Certifications & Languages")
        
        left_flowables = []
        if certs.exists():
            for cert in certs:
                left_flowables.append(f"• {cert.name} - {cert.organization} ({cert.year})")
        
        right_flowables = []
        if langs.exists():
            lang_names = [l.language for l in langs]
            right_flowables.append(f"<b>Languages:</b> {', '.join(lang_names)}")
            
        # Format as table
        left_text = "<br/>".join(left_flowables)
        right_text = "<br/>".join(right_flowables)
        
        extra_data = [
            [Paragraph(left_text, body_style), Paragraph(right_text, body_style)]
        ]
        t = Table(extra_data, colWidths=[280, 243])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(t)
        
    # Build Document
    doc.build(story)
    return response

@login_required
def duplicate_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if resume.user != request.user:
        raise PermissionDenied()
    
    # Clone main resume object
    new_resume = Resume.objects.create(
        user=request.user,
        title=f"{resume.title} (Copy)",
        target_role=resume.target_role,
        full_name=resume.full_name,
        email=resume.email,
        phone=resume.phone,
        address=resume.address,
        linkedin=resume.linkedin,
        github=resume.github,
        portfolio=resume.portfolio,
        photo=resume.photo,
        objective=resume.objective,
        ats_score=resume.ats_score,
        completion_percentage=resume.completion_percentage,
        status=resume.status
    )
    
    # Clone nested child items
    for edu in resume.educations.all():
        Education.objects.create(
            resume=new_resume,
            college=edu.college,
            degree=edu.degree,
            branch=edu.branch,
            cgpa=edu.cgpa,
            passing_year=edu.passing_year
        )
    for skill in resume.skills.all():
        Skill.objects.create(
            resume=new_resume,
            category=skill.category,
            name=skill.name
        )
    for proj in resume.projects.all():
        Project.objects.create(
            resume=new_resume,
            name=proj.name,
            technologies=proj.technologies,
            description=proj.description,
            github=proj.github,
            live_link=proj.live_link
        )
    for exp in resume.experiences.all():
        Experience.objects.create(
            resume=new_resume,
            company=exp.company,
            role=exp.role,
            duration=exp.duration,
            description=exp.description
        )
    for cert in resume.certificates.all():
        Certificate.objects.create(
            resume=new_resume,
            name=cert.name,
            organization=cert.organization,
            year=cert.year
        )
    for lang in resume.languages.all():
        Language.objects.create(
            resume=new_resume,
            language=lang.language
        )
        
    messages.success(request, f"Duplicated resume: {new_resume.title}")
    return redirect('dashboard')

@login_required
@require_POST
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if resume.user != request.user:
        raise PermissionDenied()
    title = resume.title
    resume.delete()
    messages.success(request, f"Deleted resume: {title}")
    return redirect('dashboard')

@login_required
@require_POST
def rename_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if resume.user != request.user:
        raise PermissionDenied()
    new_title = request.POST.get('title', '').strip()
    if new_title:
        resume.title = new_title
        resume.save()
        messages.success(request, f"Renamed resume to: {new_title}")
    else:
        messages.error(request, "Resume title cannot be empty.")
    return redirect('dashboard')
