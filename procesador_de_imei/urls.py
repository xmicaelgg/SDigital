from django.urls import path
from .views import procesar_imeis, historial_imei, descargar_historial_txt

urlpatterns = [
    path('procesar-imeis/', procesar_imeis, name='procesar_imeis'),
    path('historial-imei/', historial_imei, name='historial_imei'),
    path('descargar-historial/<int:historial_id>/', descargar_historial_txt, name='descargar_historial_txt'),
] 