#!/usr/bin/env python3
"""
Script para cambiar fácilmente entre SQLite y PostgreSQL
"""

import os
import sys

def cambiar_a_sqlite():
    """Cambiar configuración a SQLite"""
    settings_file = 'rma_recepcion/settings.py'
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar configuración de PostgreSQL por SQLite
    sqlite_config = '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}'''
    
    # Buscar y reemplazar la configuración de base de datos
    if 'django.db.backends.postgresql' in content:
        # Extraer la sección DATABASES
        start = content.find('DATABASES = {')
        if start != -1:
            # Encontrar el final de la configuración
            brace_count = 0
            end = start
            for i, char in enumerate(content[start:], start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i + 1
                        break
            
            # Reemplazar la configuración
            new_content = content[:start] + sqlite_config + content[end:]
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Cambiado a SQLite exitosamente")
            return True
    else:
        print("ℹ️ Ya estás usando SQLite")
        return True

def cambiar_a_postgresql():
    """Cambiar configuración a PostgreSQL"""
    settings_file = 'rma_recepcion/settings.py'
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar configuración de SQLite por PostgreSQL
    postgres_config = '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rma_recepcion_db',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}'''
    
    # Buscar y reemplazar la configuración de base de datos
    if 'django.db.backends.sqlite3' in content:
        # Extraer la sección DATABASES
        start = content.find('DATABASES = {')
        if start != -1:
            # Encontrar el final de la configuración
            brace_count = 0
            end = start
            for i, char in enumerate(content[start:], start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i + 1
                        break
            
            # Reemplazar la configuración
            new_content = content[:start] + postgres_config + content[end:]
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Cambiado a PostgreSQL exitosamente")
            return True
    else:
        print("ℹ️ Ya estás usando PostgreSQL")
        return True

def mostrar_estado():
    """Mostrar el estado actual de la base de datos"""
    settings_file = 'rma_recepcion/settings.py'
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'django.db.backends.sqlite3' in content:
        print("📊 Estado actual: SQLite")
    elif 'django.db.backends.postgresql' in content:
        print("🐘 Estado actual: PostgreSQL")
    else:
        print("❓ Estado desconocido")

def main():
    print("🗄️ Gestor de Base de Datos - RMA Recepción")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("\n📋 Uso:")
        print("  python cambiar_db.py sqlite    - Cambiar a SQLite")
        print("  python cambiar_db.py postgres  - Cambiar a PostgreSQL")
        print("  python cambiar_db.py status    - Ver estado actual")
        return
    
    comando = sys.argv[1].lower()
    
    if comando == 'sqlite':
        print("\n🔄 Cambiando a SQLite...")
        cambiar_a_sqlite()
        print("\n🚀 Ahora puedes ejecutar:")
        print("   python manage.py runserver")
        
    elif comando == 'postgres':
        print("\n🔄 Cambiando a PostgreSQL...")
        cambiar_a_postgresql()
        print("\n⚠️ Asegúrate de que PostgreSQL esté instalado y ejecutándose")
        print("\n🚀 Luego ejecuta:")
        print("   python manage.py migrate")
        print("   python manage.py createsuperuser")
        print("   python manage.py runserver")
        
    elif comando == 'status':
        mostrar_estado()
        
    else:
        print(f"❌ Comando desconocido: {comando}")
        print("Comandos válidos: sqlite, postgres, status")

if __name__ == "__main__":
    main() 