from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import date
import random
import pandas as pd
import io
from collections import defaultdict

from .models import Lote, LoteDetalle, EstadoEnum, LoteModelo
from .forms import LoteForm, LoteDetalleForm, ImportarExcelForm, ModeloEquipoForm, LoteModeloForm, LoteDetalleMarcaModeloForm, LoteModeloCantidadImeisForm

def index(request):
    """Vista principal - Lista de lotes"""
    lotes = Lote.objects.all().order_by('-fecha_creacion')
    total_lotes = lotes.count()
    total_equipos = LoteDetalle.objects.count()
    
    # Calcular promedio de equipos por lote
    promedio_equipos = 0
    if total_lotes > 0:
        promedio_equipos = round(total_equipos / total_lotes, 1)
    
    context = {
        'lotes': lotes,
        'total_lotes': total_lotes,
        'total_equipos': total_equipos,
        'promedio_equipos': promedio_equipos,
    }
    return render(request, 'equipos/index.html', context)

def crear_lote(request):
    """Crear un nuevo lote"""
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            lote = form.save()
            messages.success(request, f'Lote {lote.numero_lote} creado exitosamente.')
            return redirect('equipos:detalle_lote', lote_id=lote.id)
    else:
        # Generar número de lote automático
        numero_lote = f"LOTE-{date.today().strftime('%Y%m%d')}-{random.randint(1000,9999)}"
        form = LoteForm(initial={'numero_lote': numero_lote})
    
    context = {
        'form': form,
        'fecha_hoy': date.today().strftime('%Y-%m-%d')
    }
    return render(request, 'equipos/crear_lote.html', context)

def detalle_lote(request, lote_id):
    """Ver detalles de un lote específico"""
    lote = get_object_or_404(Lote, id=lote_id)
    equipos = lote.equipos.all()
    
    # Agrupar por marca y modelo
    resumen = defaultdict(list)
    for equipo in equipos:
        resumen[(equipo.marca, equipo.modelo)].append(equipo)
    
    resumen_list = [
        {
            'marca': marca, 
            'modelo': modelo, 
            'cantidad': len(equipos_list), 
            'equipos': equipos_list
        }
        for (marca, modelo), equipos_list in resumen.items()
    ]
    
    context = {
        'lote': lote,
        'equipos': equipos,
        'resumen': resumen_list,
        'total_equipos': equipos.count(),
    }
    return render(request, 'equipos/detalle_lote.html', context)

def agregar_equipo(request, lote_id):
    """Agregar solo marca y modelo a un lote"""
    lote = get_object_or_404(Lote, id=lote_id)
    if request.method == 'POST':
        form = LoteDetalleMarcaModeloForm(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.lote = lote
            equipo.save()
            messages.success(request, f'Modelo {equipo.marca} {equipo.modelo} agregado exitosamente al lote.')
            return redirect('equipos:detalle_lote', lote_id=lote.id)
    else:
        form = LoteDetalleMarcaModeloForm()
    context = {
        'form': form,
        'lote': lote,
    }
    return render(request, 'equipos/agregar_equipo.html', context)

def ingresar_imeis(request, lote_id):
    """Ingresar múltiples IMEIs a un lote"""
    lote = get_object_or_404(Lote, id=lote_id)
    mensaje = None
    marca_sel = request.GET.get('marca', '')
    modelo_sel = request.GET.get('modelo', '')
    
    if request.method == 'POST':
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        imeis_text = request.POST.get('imeis')
        actualizar_cantidad = request.POST.get('actualizar_cantidad', 'no')
        
        if marca and modelo and imeis_text:
            imeis_list = [i.strip() for i in imeis_text.splitlines() if i.strip()]
            guardados = 0
            duplicados = 0
            total_imeis = len(imeis_list)
            
            # Validar si se excede la cantidad_modelos
            if lote.cantidad_modelos and total_imeis > lote.cantidad_modelos and actualizar_cantidad != 'si':
                mensaje = f"La cantidad de IMEIs ({total_imeis}) excede la cantidad registrada en el lote ({lote.cantidad_modelos}). ¿Deseas actualizar la cantidad de modelos a {total_imeis}?"
                # Renderizar confirmación
                equipos = lote.equipos.all()
                resumen = defaultdict(list)
                for eq in equipos:
                    resumen[(eq.marca, eq.modelo)].append(eq.imei)
                resumen_list = [
                    {'marca': m, 'modelo': mo, 'cantidad': len(imeis), 'imeis': imeis}
                    for (m, mo), imeis in resumen.items()
                ]
                imeis_filtrados = []
                if marca_sel and modelo_sel:
                    imeis_filtrados = resumen.get((marca_sel.upper(), modelo_sel.upper()), [])
                context = {
                    'lote': lote,
                    'equipos': equipos,
                    'resumen': resumen_list,
                    'marca_sel': marca_sel,
                    'modelo_sel': modelo_sel,
                    'imeis_filtrados': imeis_filtrados,
                    'estados': EstadoEnum.choices,
                    'mensaje_confirmacion': mensaje,
                    'marca': marca,
                    'modelo': modelo,
                    'imeis': imeis_text,
                }
                return render(request, 'equipos/ingresar_imeis.html', context)
            # Si el usuario acepta actualizar la cantidad
            if actualizar_cantidad == 'si':
                lote.cantidad_modelos = total_imeis
                lote.save()
            for imei in imeis_list:
                if not LoteDetalle.objects.filter(imei=imei).exists():
                    LoteDetalle.objects.create(
                        lote=lote,
                        imei=imei,
                        marca=marca.upper(),
                        modelo=modelo.upper(),
                        estado=EstadoEnum.PERDIDA,
                        caja_original=False,
                        observaciones=''
                    )
                    guardados += 1
                else:
                    duplicados += 1
            if guardados > 0:
                messages.success(request, f"{guardados} IMEIs guardados para {marca.upper()} {modelo.upper()}.")
            if duplicados > 0:
                messages.warning(request, f"{duplicados} IMEIs ya existían y fueron omitidos.")
            marca_sel = marca
            modelo_sel = modelo
    
    equipos = lote.equipos.all()
    
    # Agrupar por marca y modelo
    resumen = defaultdict(list)
    for eq in equipos:
        resumen[(eq.marca, eq.modelo)].append(eq.imei)
    
    resumen_list = [
        {'marca': m, 'modelo': mo, 'cantidad': len(imeis), 'imeis': imeis}
        for (m, mo), imeis in resumen.items()
    ]
    
    # Filtrar IMEIs si hay filtro
    imeis_filtrados = []
    if marca_sel and modelo_sel:
        imeis_filtrados = resumen.get((marca_sel.upper(), modelo_sel.upper()), [])
    
    context = {
        'lote': lote,
        'equipos': equipos,
        'resumen': resumen_list,
        'marca_sel': marca_sel,
        'modelo_sel': modelo_sel,
        'imeis_filtrados': imeis_filtrados,
        'estados': EstadoEnum.choices,
    }
    return render(request, 'equipos/ingresar_imeis.html', context)

def editar_equipo(request, equipo_id):
    """Editar un equipo específico"""
    equipo = get_object_or_404(LoteDetalle, id=equipo_id)
    
    if request.method == 'POST':
        form = LoteDetalleForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipo actualizado exitosamente.')
            return redirect('equipos:detalle_lote', lote_id=equipo.lote.id)
    else:
        form = LoteDetalleForm(instance=equipo)
    
    context = {
        'form': form,
        'equipo': equipo,
        'estados': EstadoEnum.choices,
    }
    return render(request, 'equipos/editar_equipo.html', context)

def eliminar_equipo(request, equipo_id):
    """Eliminar un equipo"""
    equipo = get_object_or_404(LoteDetalle, id=equipo_id)
    lote_id = equipo.lote.id
    
    if request.method == 'POST':
        equipo.delete()
        messages.success(request, 'Equipo eliminado exitosamente.')
        return redirect('equipos:detalle_lote', lote_id=lote_id)
    
    context = {
        'equipo': equipo,
    }
    return render(request, 'equipos/eliminar_equipo.html', context)

def importar_excel(request):
    """Importar equipos desde archivo Excel"""
    errores = []
    
    if request.method == 'POST':
        form = ImportarExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            lote = form.cleaned_data['lote']
            
            try:
                if archivo.name.endswith('.xlsx'):
                    df = pd.read_excel(archivo)
                else:
                    df = pd.read_csv(archivo)
                
                guardados = 0
                for _, row in df.iterrows():
                    imei = str(row.get('imei', '')).strip()
                    if not imei:
                        continue
                    
                    if LoteDetalle.objects.filter(imei=imei).exists():
                        errores.append(f"IMEI duplicado: {imei}")
                        continue
                    
                    LoteDetalle.objects.create(
                        lote=lote,
                        imei=imei,
                        marca=row.get('marca', ''),
                        modelo=row.get('modelo', ''),
                        estado=row.get('estado', EstadoEnum.NUEVO),
                        caja_original=bool(row.get('caja_original', False)),
                        observaciones=row.get('observaciones', '')
                    )
                    guardados += 1
                
                if guardados > 0:
                    messages.success(request, f'{guardados} equipos importados exitosamente.')
                if errores:
                    messages.warning(request, f'{len(errores)} equipos no pudieron ser importados.')
                    
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
    else:
        form = ImportarExcelForm()
    
    context = {
        'form': form,
        'errores': errores,
    }
    return render(request, 'equipos/importar_excel.html', context)

def exportar_lote(request, lote_id):
    """Exportar un lote a Excel"""
    lote = get_object_or_404(Lote, id=lote_id)
    equipos = lote.equipos.all()
    
    data = [{
        'Marca': e.marca,
        'Modelo': e.modelo,
        'IMEI': e.imei,
        'Estado': e.estado,
        'Caja Original': 'Sí' if e.caja_original else 'No',
        'Observaciones': e.observaciones or '',
        'Fecha Ingreso': e.fecha_ingreso.strftime('%Y-%m-%d %H:%M:%S')
    } for e in equipos]
    
    df = pd.DataFrame(data)
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=f'Lote_{lote.numero_lote}')
    
    output.seek(0)
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="lote_{lote.numero_lote}.xlsx"'
    
    return response

def editar_lote(request, lote_id):
    lote = get_object_or_404(Lote, id=lote_id)
    if request.method == 'POST':
        form = LoteForm(request.POST, instance=lote)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lote actualizado exitosamente.')
            return redirect('equipos:detalle_lote', lote_id=lote.id)
    else:
        form = LoteForm(instance=lote)
    context = {
        'form': form,
        'lote': lote
    }
    return render(request, 'equipos/editar_lote.html', context)

def crear_modelo_equipo(request):
    if request.method == 'POST':
        form = ModeloEquipoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo registrado correctamente.')
            return redirect('equipos:crear_modelo_equipo')
    else:
        form = ModeloEquipoForm()
    return render(request, 'equipos/crear_modelo_equipo.html', {'form': form})

def agregar_modelo_lote(request):
    if request.method == 'POST':
        form = LoteModeloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo agregado al lote correctamente.')
            return redirect('equipos:agregar_modelo_lote')
    else:
        form = LoteModeloForm()
    return render(request, 'equipos/agregar_modelo_lote.html', {'form': form})

def agregar_cantidad_imeis(request, lote_id):
    lote = get_object_or_404(Lote, id=lote_id)
    mensaje = None
    if request.method == 'POST':
        form = LoteModeloCantidadImeisForm(request.POST)
        if form.is_valid():
            lote_modelo = form.cleaned_data['modelo']
            cantidad = form.cleaned_data['cantidad']
            imeis_text = form.cleaned_data['imeis']
            imeis_list = [i.strip() for i in imeis_text.splitlines() if i.strip()] if imeis_text else []
            total_imeis = len(imeis_list)
            # Validar cantidad
            if cantidad and total_imeis > cantidad and not request.POST.get('confirmar'):
                mensaje = f"La cantidad de IMEIs ({total_imeis}) excede la cantidad registrada ({cantidad}). ¿Deseas actualizar la cantidad y continuar?"
                return render(request, 'equipos/agregar_cantidad_imeis.html', {'form': form, 'lote': lote, 'mensaje': mensaje, 'exceso': True})
            # Si el usuario confirma, actualizar cantidad
            if total_imeis > (cantidad or 0) and request.POST.get('confirmar'):
                cantidad = total_imeis
            # Guardar cantidad en el modelo
            lote_modelo.cantidad = cantidad or total_imeis
            lote_modelo.save()
            # Guardar IMEIs en LoteDetalle
            guardados = 0
            for imei in imeis_list:
                if not LoteDetalle.objects.filter(imei=imei).exists():
                    LoteDetalle.objects.create(
                        lote=lote,
                        marca=lote_modelo.marca,
                        modelo=lote_modelo.modelo,
                        imei=imei,
                        estado=EstadoEnum.NUEVO,
                        caja_original=False,
                        observaciones=''
                    )
                    guardados += 1
            if guardados > 0:
                messages.success(request, f"{guardados} IMEIs guardados para {lote_modelo.marca} {lote_modelo.modelo}.")
            return redirect('equipos:detalle_lote', lote_id=lote.id)
    else:
        form = LoteModeloCantidadImeisForm()
        form.fields['modelo'].queryset = LoteModelo.objects.filter(lote=lote)
    return render(request, 'equipos/agregar_cantidad_imeis.html', {'form': form, 'lote': lote})

# API Views
@csrf_exempt
@require_http_methods(["GET"])
def api_listar_equipos(request):
    """API para listar equipos"""
    estado = request.GET.get('estado')
    lote_id = request.GET.get('lote_id')
    
    equipos = LoteDetalle.objects.all()
    
    if estado:
        equipos = equipos.filter(estado=estado)
    if lote_id:
        equipos = equipos.filter(lote_id=lote_id)
    
    data = [{
        'id': e.id,
        'imei': e.imei,
        'marca': e.marca,
        'modelo': e.modelo,
        'estado': e.estado,
        'caja_original': e.caja_original,
        'observaciones': e.observaciones,
        'fecha_ingreso': e.fecha_ingreso.isoformat(),
        'lote_id': e.lote.id,
        'lote_numero': e.lote.numero_lote
    } for e in equipos]
    
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def api_crear_equipo(request):
    """API para crear un equipo"""
    import json
    data = json.loads(request.body)
    
    imei = data.get('imei')
    if not imei:
        return JsonResponse({'error': 'IMEI es requerido'}, status=400)
    
    if LoteDetalle.objects.filter(imei=imei).exists():
        return JsonResponse({'error': 'IMEI duplicado'}, status=400)
    
    try:
        lote = Lote.objects.get(id=data.get('lote_id'))
        equipo = LoteDetalle.objects.create(
            lote=lote,
            imei=imei,
            marca=data.get('marca', ''),
            modelo=data.get('modelo', ''),
            estado=data.get('estado', EstadoEnum.NUEVO),
            caja_original=data.get('caja_original', False),
            observaciones=data.get('observaciones', '')
        )
        return JsonResponse({'success': True, 'id': equipo.id})
    except Lote.DoesNotExist:
        return JsonResponse({'error': 'Lote no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def api_eliminar_equipo(request, equipo_id):
    """API para eliminar un equipo"""
    try:
        equipo = LoteDetalle.objects.get(id=equipo_id)
        equipo.delete()
        return JsonResponse({'success': True})
    except LoteDetalle.DoesNotExist:
        return JsonResponse({'error': 'Equipo no encontrado'}, status=404)
