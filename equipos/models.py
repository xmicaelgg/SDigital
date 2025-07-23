from django.db import models
from django.core.validators import RegexValidator
import uuid

class EstadoEnum(models.TextChoices):
    NUEVO = 'Nuevo', 'Nuevo'
    USADO = 'Usado', 'Usado'
    ROTO = 'Roto', 'Roto'
    MEZCLA = 'Mezcla', 'Mezcla'
    PERDIDA = 'Perdida', 'Perdida'

class Lote(models.Model):
    numero_lote = models.CharField(max_length=50, unique=True, verbose_name="Número de Lote")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    cantidad_modelos = models.PositiveIntegerField(default=0, verbose_name="Cantidad de Modelos")
    
    class Meta:
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Lote {self.numero_lote}"
    
    def cantidad_equipos(self):
        return self.equipos.count()

class ModeloEquipo(models.Model):
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")

    class Meta:
        unique_together = ['marca', 'modelo']
        verbose_name = "Modelo de Equipo"
        verbose_name_plural = "Modelos de Equipo"
        ordering = ['marca', 'modelo']

    def __str__(self):
        return f"{self.marca} {self.modelo}"

class LoteDetalle(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='equipos', verbose_name="Lote")
    marca = models.CharField(max_length=50, verbose_name="Marca", null=True, blank=True)
    modelo = models.CharField(max_length=50, verbose_name="Modelo", null=True, blank=True)
    imei = models.CharField(
        max_length=50, 
        verbose_name="IMEI",
        validators=[
            RegexValidator(
                regex=r'^\d{15}$',
                message='El IMEI debe tener exactamente 15 dígitos numéricos.'
            )
        ]
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoEnum.choices,
        default=EstadoEnum.NUEVO,
        verbose_name="Estado"
    )
    caja_original = models.BooleanField(default=False, verbose_name="Caja Original")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    fecha_ingreso = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    
    class Meta:
        verbose_name = "Detalle de Lote"
        verbose_name_plural = "Detalles de Lote"
        unique_together = ['lote', 'imei']
        ordering = ['-fecha_ingreso']
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.imei}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Verificar que el IMEI no esté duplicado en otros lotes
        if LoteDetalle.objects.filter(imei=self.imei).exclude(id=self.id).exists():
            raise ValidationError({'imei': 'Este IMEI ya existe en otro lote.'})

class LoteModelo(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='modelos', verbose_name="Lote")
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")

    class Meta:
        unique_together = ['lote', 'marca', 'modelo']
        verbose_name = "Modelo en Lote"
        verbose_name_plural = "Modelos en Lote"
        ordering = ['lote', 'marca', 'modelo']

    def __str__(self):
        return f"{self.lote} - {self.marca} {self.modelo}"
