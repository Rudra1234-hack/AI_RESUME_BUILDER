from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .services import improve_resume_text
import json

@login_required
@require_POST
def improve_text_view(request):
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        section_type = data.get('section_type', 'general')
        
        if not text.strip():
            return JsonResponse({'error': 'Input text cannot be empty.'}, status=400)
            
        improved_text = improve_resume_text(text, section_type)
        return JsonResponse({'improved_text': improved_text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
