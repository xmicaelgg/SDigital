#!/usr/bin/env python3
"""
Script para configurar PostgreSQL para el proyecto RMA Recepción
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completado exitosamente")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ Error en {description}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False
    return True

def main():
    print("🐘 Configurando PostgreSQL para RMA Recepción")
    print("=" * 50)
    
    # Verificar si PostgreSQL está instalado
    print("\n🔍 Verificando instalación de PostgreSQL...")
    
    # Intentar conectar a PostgreSQL
    psql_check = run_command("psql --version", "Verificando PostgreSQL")
    
    if not psql_check:
        print("\n❌ PostgreSQL no está instalado o no está en el PATH")
        print("\n📥 Para instalar PostgreSQL en Windows:")
        print("1. Descarga PostgreSQL desde: https://www.postgresql.org/download/windows/")
        print("2. Ejecuta el instalador")
        print("3. Usa la contraseña: admin")
        print("4. Puerto: 5432")
        print("5. Reinicia este script después de la instalación")
        return
    
    # Crear la base de datos
    print("\n🗄️ Configurando la base de datos...")
    
    # Crear base de datos
    create_db = run_command(
        'psql -U postgres -c "CREATE DATABASE rma_recepcion_db;"',
        "Creando base de datos rma_recepcion_db"
    )
    
    if not create_db:
        print("\n⚠️ La base de datos ya existe o hay un error de conexión")
        print("Continuando con la configuración...")
    
    # Verificar conexión
    test_connection = run_command(
        'psql -U postgres -d rma_recepcion_db -c "SELECT version();"',
        "Probando conexión a la base de datos"
    )
    
    if test_connection:
        print("\n✅ PostgreSQL configurado correctamente!")
        print("\n📋 Configuración de la base de datos:")
        print("   - Nombre: rma_recepcion_db")
        print("   - Usuario: postgres")
        print("   - Contraseña: admin")
        print("   - Host: localhost")
        print("   - Puerto: 5432")
        
        print("\n🚀 Ahora puedes ejecutar:")
        print("   python manage.py migrate")
        print("   python manage.py createsuperuser")
        print("   python manage.py runserver")
    else:
        print("\n❌ Error en la configuración de PostgreSQL")
        print("Verifica que PostgreSQL esté ejecutándose y las credenciales sean correctas")

if __name__ == "__main__":
    main() 