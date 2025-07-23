from django.db import models

# Create your models here.

class IMEIRecord(models.Model):
    imei = models.CharField(max_length=15, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.imei

class HistorialProcesamiento(models.Model):
    MODELO_CHOICES = [
        ('generico', 'Genérico'),
        ('mojo', 'Mojo'),
    ]
    modelo = models.CharField(max_length=20, choices=MODELO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad = models.PositiveIntegerField()
    imeis = models.TextField()

    def __str__(self):
        return f"{self.get_modelo_display()} - {self.fecha.strftime('%Y-%m-%d %H:%M')} ({self.cantidad} IMEIs)"
