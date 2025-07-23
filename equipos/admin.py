from django.contrib import admin
from .models import Lote, LoteDetalle, EstadoEnum

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['numero_lote', 'fecha_creacion', 'descripcion', 'cantidad_equipos']
    list_filter = ['fecha_creacion']
    search_fields = ['numero_lote', 'descripcion']
    readonly_fields = ['fecha_creacion']
    
    def cantidad_equipos(self, obj):
        return obj.cantidad_equipos()
    cantidad_equipos.short_description = 'Cantidad de Equipos'

@admin.register(LoteDetalle)
class LoteDetalleAdmin(admin.ModelAdmin):
    list_display = ['imei', 'marca', 'modelo', 'estado', 'lote', 'caja_original', 'fecha_ingreso']
    list_filter = ['estado', 'marca', 'modelo', 'caja_original', 'fecha_ingreso', 'lote']
    search_fields = ['imei', 'marca', 'modelo', 'observaciones']
    readonly_fields = ['fecha_ingreso']
    list_editable = ['estado', 'caja_original']
    
    fieldsets = (
        ('Información del Equipo', {
            'fields': ('lote', 'marca', 'modelo', 'imei')
        }),
        ('Estado y Condición', {
            'fields': ('estado', 'caja_original')
        }),
        ('Información Adicional', {
            'fields': ('observaciones', 'fecha_ingreso'),
            'classes': ('collapse',)
        }),
    )
