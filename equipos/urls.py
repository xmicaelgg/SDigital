from django.urls import path
from . import views

app_name = 'equipos'

urlpatterns = [
    # Vistas principales
    path('', views.index, name='index'),
    path('lote/crear/', views.crear_lote, name='crear_lote'),
    path('lote/<int:lote_id>/', views.detalle_lote, name='detalle_lote'),
    path('lote/<int:lote_id>/agregar-equipo/', views.agregar_equipo, name='agregar_equipo'),
    path('lote/<int:lote_id>/ingresar-imeis/', views.ingresar_imeis, name='ingresar_imeis'),
    path('lote/<int:lote_id>/editar/', views.editar_lote, name='editar_lote'),
    path('lote/<int:lote_id>/agregar-cantidad-imeis/', views.agregar_cantidad_imeis, name='agregar_cantidad_imeis'),
    
    # Gestión de equipos
    path('equipo/<int:equipo_id>/editar/', views.editar_equipo, name='editar_equipo'),
    path('equipo/<int:equipo_id>/eliminar/', views.eliminar_equipo, name='eliminar_equipo'),
    
    # Importación y exportación
    path('importar-excel/', views.importar_excel, name='importar_excel'),
    path('lote/<int:lote_id>/exportar/', views.exportar_lote, name='exportar_lote'),
    
    # API endpoints
    path('api/equipos/', views.api_listar_equipos, name='api_listar_equipos'),
    path('api/equipos/crear/', views.api_crear_equipo, name='api_crear_equipo'),
    path('api/equipos/<int:equipo_id>/eliminar/', views.api_eliminar_equipo, name='api_eliminar_equipo'),
    path('crear-modelo/', views.crear_modelo_equipo, name='crear_modelo_equipo'),
    path('agregar-modelo-lote/', views.agregar_modelo_lote, name='agregar_modelo_lote'),
] 