from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('editar/<int:pk>/', views.editar_alumno, name='editar_alumno'),
    path('eliminar/<int:pk>/', views.eliminar_alumno, name='eliminar_alumno'),
    path('enviar-pdf/<int:pk>/', views.enviar_pdf_email, name='enviar_pdf'),
    path('descargar-pdf/<int:pk>/', views.descargar_pdf, name='descargar_pdf'),
]