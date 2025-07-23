from django.shortcuts import render
from django.contrib import messages
from .forms import IMEIForm
from .models import IMEIRecord, HistorialProcesamiento
from .utils import extraer_imeis
from django.http import HttpResponse
import urllib.parse

# Create your views here.

def procesar_imeis(request):
    resultados = {
        'imeis_encontrados': [],
        'nuevos': 0,
    }
    if request.method == 'POST':
        form = IMEIForm(request.POST)
        if 'limpiar' in request.POST:
            form = IMEIForm()
            messages.info(request, 'Formulario limpiado.')
            return render(request, 'procesador_de_imei/procesar_imeis.html', {'form': form, 'resultados': resultados})
        if form.is_valid():
            texto = form.cleaned_data['raw_text']
            modelo = form.cleaned_data['modelo']
            omitir_pares = (modelo == 'mojo')
            imeis = extraer_imeis(texto, omitir_pares=omitir_pares)
            resultados['imeis_encontrados'] = imeis
            nuevos = 0
            for imei in imeis:
                if len(imei) != 15:
                    messages.warning(request, f'IMEI inválido: {imei}')
                    continue
                obj, created = IMEIRecord.objects.get_or_create(imei=imei)
                if created:
                    nuevos += 1
            resultados['nuevos'] = nuevos
            if 'guardar_historial' in request.POST and imeis:
                HistorialProcesamiento.objects.create(
                    modelo=modelo,
                    cantidad=len(imeis),
                    imeis='\n'.join(imeis)
                )
                messages.success(request, 'Procesamiento guardado en historial.')
            messages.success(request, f"Procesados: {len(imeis)} | Nuevos guardados: {nuevos}")
    else:
        form = IMEIForm()
    return render(request, 'procesador_de_imei/procesar_imeis.html', {'form': form, 'resultados': resultados})

def historial_imei(request):
    historial = HistorialProcesamiento.objects.order_by('-fecha')
    return render(request, 'procesador_de_imei/historial_imei.html', {'historial': historial})

def descargar_historial_txt(request, historial_id):
    registro = HistorialProcesamiento.objects.get(id=historial_id)
    nombre = f"{registro.get_modelo_display()}_{registro.fecha.strftime('%Y%m%d_%H%M')}_{registro.cantidad}IMEIs.txt"
    response = HttpResponse(registro.imeis, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{urllib.parse.quote(nombre)}"'
    return response
