from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from resume.models import Resume
from resume.views import calculate_ats_score_and_tips

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    
    total_resumes = resumes.count()
    
    # Calculate average ATS score
    from django.db.models import Avg, Max
    avg_ats = resumes.aggregate(Avg('ats_score'))['ats_score__avg'] or 0
    average_ats_score = round(avg_ats, 1)
    
    # Highest ATS score
    highest_ats_score = resumes.aggregate(Max('ats_score'))['ats_score__max'] or 0
    
    # Completed/Draft counts
    completed_resumes = resumes.filter(completion_percentage=100).count()
    draft_resumes = resumes.exclude(completion_percentage=100).count()
    
    context = {
        'resumes': resumes,
        'has_resumes': total_resumes > 0,
        'total_resumes': total_resumes,
        'average_ats_score': average_ats_score,
        'highest_ats_score': highest_ats_score,
        'completed_resumes': completed_resumes,
        'draft_resumes': draft_resumes,
    }
    return render(request, 'core/dashboard.html', context)
