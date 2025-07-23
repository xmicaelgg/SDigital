# Sistema de Recepción RMA - Django

Sistema web para la gestión de recepción de equipos RMA (Return Merchandise Authorization) desarrollado con Django.

## Características

- ✅ Gestión de lotes de equipos
- ✅ Registro de equipos con IMEI único
- ✅ Estados de equipos (Nuevo, Usado, Roto, Mezcla, Perdida)
- ✅ Importación masiva desde archivos Excel/CSV
- ✅ Exportación de lotes a Excel
- ✅ Interfaz web moderna con Bootstrap 5
- ✅ API REST para integración con otros sistemas
- ✅ Panel de administración de Django
- ✅ Validación de IMEIs (15 dígitos numéricos)

## Tecnologías Utilizadas

- **Backend**: Django 5.2+
- **Base de Datos**: SQLite (configurable para producción)
- **Frontend**: Bootstrap 5, Font Awesome
- **Procesamiento de datos**: Pandas, OpenPyXL
- **Validación**: Django Forms con validadores personalizados

## Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd "RMA RECEPCION"
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Crear superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

6. **Acceder a la aplicación**
   - Aplicación principal: http://127.0.0.1:8000/
   - Panel de administración: http://127.0.0.1:8000/admin/

## Uso del Sistema

### 1. Crear un Lote

1. Accede a la página principal
2. Haz clic en "Nuevo Lote"
3. Completa la información del lote:
   - Número de lote (se genera automáticamente)
   - Descripción (opcional)
4. Haz clic en "Crear Lote"

### 2. Agregar Equipos

#### Opción A: Agregar Equipo Individual
1. Desde el detalle del lote, haz clic en "Agregar Equipo"
2. Completa la información:
   - Marca y modelo
   - IMEI (15 dígitos)
   - Estado del equipo
   - Si tiene caja original
   - Observaciones
3. Haz clic en "Guardar Equipo"

#### Opción B: Ingresar Múltiples IMEIs
1. Desde el detalle del lote, haz clic en "Ingresar IMEIs"
2. Completa marca y modelo
3. Pega la lista de IMEIs (uno por línea)
4. Haz clic en "Guardar IMEIs"

#### Opción C: Importar desde Excel
1. Ve a "Importar Excel" en el menú principal
2. Selecciona el lote de destino
3. Sube el archivo Excel/CSV
4. El sistema procesará automáticamente los datos

### 3. Gestionar Equipos

- **Ver detalles**: Haz clic en el lote para ver todos los equipos
- **Editar**: Usa el botón de editar en cada equipo
- **Eliminar**: Usa el botón de eliminar (con confirmación)
- **Exportar**: Descarga el lote completo en formato Excel

## Estructura del Proyecto

```
RMA RECEPCION/
├── manage.py                 # Script de gestión de Django
├── requirements.txt          # Dependencias del proyecto
├── rma_recepcion/           # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   ├── wsgi.py              # Configuración WSGI
│   └── asgi.py              # Configuración ASGI
├── equipos/                 # Aplicación principal
│   ├── __init__.py
│   ├── admin.py             # Configuración del admin
│   ├── apps.py              # Configuración de la app
│   ├── forms.py             # Formularios Django
│   ├── models.py            # Modelos de datos
│   ├── urls.py              # URLs de la aplicación
│   └── views.py             # Vistas y lógica de negocio
├── templates/               # Plantillas HTML
│   ├── base.html            # Plantilla base
│   └── equipos/             # Plantillas específicas
│       ├── index.html
│       ├── crear_lote.html
│       ├── detalle_lote.html
│       ├── agregar_equipo.html
│       ├── ingresar_imeis.html
│       └── importar_excel.html
├── static/                  # Archivos estáticos (CSS, JS, imágenes)
├── media/                   # Archivos subidos por usuarios
└── db.sqlite3              # Base de datos SQLite
```

## Modelos de Datos

### Lote
- `numero_lote`: Identificador único del lote
- `fecha_creacion`: Fecha y hora de creación
- `descripcion`: Descripción opcional del lote

### LoteDetalle (Equipo)
- `lote`: Relación con el lote padre
- `marca`: Marca del equipo
- `modelo`: Modelo del equipo
- `imei`: IMEI único (15 dígitos)
- `estado`: Estado del equipo (Nuevo, Usado, Roto, Mezcla, Perdida)
- `caja_original`: Si tiene caja original
- `observaciones`: Observaciones adicionales
- `fecha_ingreso`: Fecha y hora de ingreso

## API REST

El sistema incluye endpoints API para integración:

- `GET /api/equipos/` - Listar equipos
- `POST /api/equipos/crear/` - Crear nuevo equipo
- `DELETE /api/equipos/{id}/eliminar/` - Eliminar equipo

### Ejemplo de uso de la API

```bash
# Listar equipos
curl http://127.0.0.1:8000/api/equipos/

# Crear equipo
curl -X POST http://127.0.0.1:8000/api/equipos/crear/ \
  -H "Content-Type: application/json" \
  -d '{
    "imei": "123456789012345",
    "marca": "Samsung",
    "modelo": "Galaxy S21",
    "estado": "Nuevo",
    "lote_id": 1
  }'
```

## Configuración para Producción

### Cambiar Base de Datos

Para usar PostgreSQL o MySQL en producción, modifica `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tu_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Configuración de Archivos Estáticos

```bash
python manage.py collectstatic
```

### Configuración de Seguridad

```python
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']
SECRET_KEY = 'tu-clave-secreta-muy-segura'
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas, contacta al equipo de desarrollo.

---

**Desarrollado con ❤️ usando Django** 