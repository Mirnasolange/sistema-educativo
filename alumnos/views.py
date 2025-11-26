from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO
from .models import Alumno
from .forms import AlumnoForm

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'alumnos/dashboard.html', {'alumnos': alumnos})

@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, 'Alumno creado exitosamente.')
            return redirect('dashboard')
    else:
        form = AlumnoForm()
    return render(request, 'alumnos/crear_alumno.html', {'form': form})

@login_required
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno actualizado exitosamente.')
            return redirect('dashboard')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'alumnos/editar_alumno.html', {'form': form, 'alumno': alumno})

@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    if request.method == 'POST':
        alumno.delete()
        messages.success(request, 'Alumno eliminado exitosamente.')
        return redirect('dashboard')
    return render(request, 'alumnos/eliminar_alumno.html', {'alumno': alumno})

def generar_pdf_alumno(alumno):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=1
    )
    
    title = Paragraph("Informe de Alumno", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    data = [
        ['Campo', 'Información'],
        ['Nombre Completo', alumno.nombre_completo],
        ['Email', alumno.email],
        ['Curso', alumno.curso],
        ['Calificación', str(alumno.calificacion) if alumno.calificacion else 'N/A'],
        ['Fecha de Registro', alumno.fecha_registro.strftime('%d/%m/%Y %H:%M')],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(table)
    doc.build(story)
    
    buffer.seek(0)
    return buffer

@login_required
def enviar_pdf_email(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    try:
        pdf_buffer = generar_pdf_alumno(alumno)
        
        email = EmailMessage(
            subject=f'Informe del Alumno: {alumno.nombre_completo}',
            body=f'Adjunto encontrarás el informe del alumno {alumno.nombre_completo} del curso {alumno.curso}.\n\nSaludos cordiales.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[request.user.email],
        )
        
        email.attach(f'informe_{alumno.nombre_completo.replace(" ", "_")}.pdf', pdf_buffer.getvalue(), 'application/pdf')
        email.send()
        
        messages.success(request, f'PDF enviado exitosamente a {request.user.email}')
    except Exception as e:
        messages.error(request, f'Error al enviar el PDF: {str(e)}')
    
    return redirect('dashboard')

@login_required
def descargar_pdf(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    pdf_buffer = generar_pdf_alumno(alumno)
    
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_{alumno.nombre_completo.replace(" ", "_")}.pdf"'
    
    return response