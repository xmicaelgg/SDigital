# 🐘 Guía de Instalación de PostgreSQL para RMA Recepción

## 📥 Paso 1: Descargar PostgreSQL

1. **Ve al sitio oficial:** https://www.postgresql.org/download/windows/
2. **Descarga PostgreSQL 17** (versión más reciente y recomendada)
3. **Ejecuta el instalador** como administrador

## ⚙️ Paso 2: Configurar la Instalación

### Durante la instalación, usa estos valores:

- **Directorio de instalación:** `C:\Program Files\PostgreSQL\17` (por defecto)
- **Contraseña para el usuario postgres:** `admin`
- **Puerto:** `5432` (por defecto)
- **Locale:** `Default locale`

### ✅ Opciones importantes a marcar:

- ✅ **PostgreSQL Server**
- ✅ **pgAdmin 4** (interfaz gráfica)
- ✅ **Stack Builder**
- ✅ **Add PostgreSQL to the PATH**

## 🔧 Paso 3: Verificar la Instalación

Después de instalar, abre una nueva terminal y ejecuta:

```bash
psql --version
```

Deberías ver algo como: `psql (PostgreSQL) 17.x`

## 🗄️ Paso 4: Configurar la Base de Datos

Una vez instalado PostgreSQL, ejecuta:

```bash
python setup_postgresql.py
```

## 🔄 Paso 5: Cambiar a PostgreSQL

Después de que PostgreSQL esté funcionando, cambia la configuración en `rma_recepcion/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rma_recepcion_db',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Paso 6: Migrar y Crear Superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🛠️ Solución de Problemas

### Si psql no se reconoce:
1. Reinicia la terminal
2. Verifica que PostgreSQL esté en el PATH
3. Busca en: `C:\Program Files\PostgreSQL\17\bin`

### Si el servicio no inicia:
1. Abre "Servicios" (services.msc)
2. Busca "postgresql-x64-17"
3. Inicia el servicio manualmente

### Si hay problemas de conexión:
1. Verifica que el puerto 5432 esté libre
2. Revisa el firewall de Windows
3. Asegúrate de que el servicio esté ejecutándose

## 📋 Comandos Útiles

```bash
# Verificar si PostgreSQL está ejecutándose
netstat -an | findstr 5432

# Conectar a PostgreSQL
psql -U postgres

# Listar bases de datos
\l

# Crear base de datos
CREATE DATABASE rma_recepcion_db;

# Salir de psql
\q
```

## 🎯 Configuración Final

Una vez que todo esté funcionando:

- **Base de datos:** rma_recepcion_db
- **Usuario:** postgres
- **Contraseña:** admin
- **Host:** localhost
- **Puerto:** 5432

¡Listo! Tu sistema RMA Recepción estará usando PostgreSQL. 🎉 