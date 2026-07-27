from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100, default="My Resume")
    target_role = models.CharField(max_length=150, blank=True)
    ats_score = models.IntegerField(default=0)
    completion_percentage = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='Draft')
    
    # Personal Info
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    linkedin = models.URLField(blank=True, max_length=500)
    github = models.URLField(blank=True, max_length=500)
    portfolio = models.URLField(blank=True, max_length=500)
    photo = models.ImageField(upload_to='resume_photos/', blank=True, null=True)
    
    # Career Objective
    objective = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name or 'Untitled'} - {self.title}"

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    college = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, blank=True)
    cgpa = models.CharField(max_length=20)  # GPA or percentage as string
    passing_year = models.IntegerField()

    def __str__(self):
        return f"{self.degree} at {self.college}"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('languages', 'Programming Languages'),
        ('frameworks', 'Frameworks'),
        ('databases', 'Databases'),
        ('tools', 'Tools'),
        ('soft_skills', 'Soft Skills'),
    ]
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    technologies = models.CharField(max_length=255)  # comma separated or text
    description = models.TextField()
    github = models.URLField(blank=True, max_length=500)
    live_link = models.URLField(blank=True, max_length=500, null=True)

    def __str__(self):
        return self.name

class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)  # e.g., "Jan 2023 - Present"
    description = models.TextField()

    def __str__(self):
        return f"{self.role} at {self.company}"

class Certificate(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} by {self.organization}"

class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language
