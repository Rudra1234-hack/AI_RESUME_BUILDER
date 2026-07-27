from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_resume, name='create_resume'),
    path('builder/<int:resume_id>/', views.builder_wizard, name='builder_wizard'),
    path('save/<int:resume_id>/', views.auto_save_resume, name='auto_save_resume'),
    path('add-item/<str:item_type>/<int:resume_id>/', views.add_item_ajax, name='add_item_ajax'),
    path('delete-item/<str:item_type>/<int:item_id>/<int:resume_id>/', views.delete_item_ajax, name='delete_item_ajax'),
    path('preview/<int:resume_id>/', views.resume_preview, name='resume_preview'),
    path('pdf/<int:resume_id>/', views.generate_pdf, name='generate_pdf'),
    path('duplicate/<int:resume_id>/', views.duplicate_resume, name='duplicate_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('rename/<int:resume_id>/', views.rename_resume, name='rename_resume'),
]
