from django.contrib import admin
from .models import Alumno

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'curso', 'calificacion', 'usuario', 'fecha_registro']
    list_filter = ['curso', 'fecha_registro', 'usuario']
    search_fields = ['nombre_completo', 'email', 'curso']
    date_hierarchy = 'fecha_registro'
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Alumno', {
            'fields': ('nombre_completo', 'email', 'curso', 'calificacion')
        }),
        ('Sistema', {
            'fields': ('usuario', 'fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)