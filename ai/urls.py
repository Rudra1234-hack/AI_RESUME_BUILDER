from django.urls import path
from . import views

urlpatterns = [
    path('improve/', views.improve_text_view, name='improve_text'),
]
