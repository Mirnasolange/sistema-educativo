from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import requests
from bs4 import BeautifulSoup

@login_required
def scraper_view(request):
    resultados = []
    palabra_clave = ''
    
    if request.method == 'POST':
        palabra_clave = request.POST.get('palabra_clave', '').strip()
        enviar_email = request.POST.get('enviar_email', False)
        
        if palabra_clave:
            try:
                # Scraping de Wikipedia (ejemplo educativo)
                url = f'http://es.wikipedia.org/wiki/{palabra_clave.replace(" ", "_")}'
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Obtener título
                    titulo = soup.find('h1', {'id': 'firstHeading'})
                    titulo_texto = titulo.text if titulo else 'Sin título'
                    
                    # Obtener primeros párrafos
                    content_div = soup.find('div', {'id': 'mw-content-text'})
                    if content_div:
                        paragraphs = content_div.find_all('p', limit=3)
                        for i, p in enumerate(paragraphs):
                            texto = p.get_text().strip()
                            if len(texto) > 50:
                                resultados.append({
                                    'numero': i + 1,
                                    'titulo': f'Párrafo {i + 1}',
                                    'contenido': texto[:300] + '...' if len(texto) > 300 else texto,
                                    'fuente': url
                                })
                    
                    # Buscar enlaces relacionados
                    enlaces = soup.find_all('a', limit=10)
                    enlaces_educativos = []
                    for enlace in enlaces:
                        href = enlace.get('href', '')
                        if href.startswith('/wiki/') and ':' not in href:
                            texto = enlace.get_text().strip()
                            if texto and len(texto) > 3:
                                enlaces_educativos.append({
                                    'numero': len(resultados) + len(enlaces_educativos) + 1,
                                    'titulo': texto,
                                    'contenido': f'Enlace relacionado: {texto}',
                                    'fuente': f'http://es.wikipedia.org{href}'
                                })
                                if len(enlaces_educativos) >= 5:
                                    break
                    
                    resultados.extend(enlaces_educativos)
                    
                    if resultados:
                        messages.success(request, f'Se encontraron {len(resultados)} resultados para "{palabra_clave}"')
                        
                        # Enviar por email si se solicitó
                        if enviar_email:
                            try:
                                email_body = f'Resultados de búsqueda para: {palabra_clave}\n\n'
                                for resultado in resultados:
                                    email_body += f"{resultado['numero']}. {resultado['titulo']}\n"
                                    email_body += f"   {resultado['contenido']}\n"
                                    email_body += f"   Fuente: {resultado['fuente']}\n\n"
                                
                                send_mail(
                                    subject=f'Resultados de Scraping: {palabra_clave}',
                                    message=email_body,
                                    from_email=settings.DEFAULT_FROM_EMAIL,
                                    recipient_list=[request.user.email],
                                    fail_silently=False,
                                )
                                messages.success(request, f'Resultados enviados a {request.user.email}')
                            except Exception as e:
                                messages.error(request, f'Error al enviar email: {str(e)}')
                    else:
                        messages.warning(request, 'No se encontraron resultados relevantes')
                else:
                    messages.error(request, f'No se pudo acceder a la información. Código: {response.status_code}')
                    
            except requests.exceptions.Timeout:
                messages.error(request, 'Tiempo de espera agotado. Intenta nuevamente.')
            except requests.exceptions.RequestException as e:
                messages.error(request, f'Error de conexión: {str(e)}')
            except Exception as e:
                messages.error(request, f'Error inesperado: {str(e)}')
        else:
            messages.warning(request, 'Por favor ingresa una palabra clave')
    
    return render(request, 'scraper/scraper.html', {
        'resultados': resultados,
        'palabra_clave': palabra_clave
    })