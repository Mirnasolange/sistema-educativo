from django import forms
from .models import Alumno

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre_completo', 'email', 'curso', 'calificacion']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del alumno'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'curso': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Matemáticas Avanzadas'
            }),
            'calificacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'max': '10'
            }),
        }