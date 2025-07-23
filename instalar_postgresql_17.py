#!/usr/bin/env python3
"""
Script para instalar y configurar PostgreSQL 17 para RMA Recepción
"""

import os
import sys
import subprocess
import webbrowser
import platform

def mostrar_banner():
    """Mostrar banner del script"""
    print("🐘 PostgreSQL 17 - Instalador para RMA Recepción")
    print("=" * 60)
    print("Este script te ayudará a instalar y configurar PostgreSQL 17")
    print("para tu sistema RMA Recepción.")
    print()

def verificar_sistema():
    """Verificar el sistema operativo"""
    sistema = platform.system()
    if sistema != "Windows":
        print("❌ Este script está diseñado para Windows")
        print("Para otros sistemas, consulta la documentación oficial")
        return False
    
    print(f"✅ Sistema detectado: {sistema}")
    return True

def abrir_descarga():
    """Abrir la página de descarga de PostgreSQL 17"""
    print("🌐 Abriendo página de descarga de PostgreSQL 17...")
    url = "https://www.postgresql.org/download/windows/"
    webbrowser.open(url)
    print("✅ Página abierta en tu navegador")
    print()

def mostrar_instrucciones_instalacion():
    """Mostrar instrucciones de instalación"""
    print("📋 INSTRUCCIONES DE INSTALACIÓN:")
    print("-" * 40)
    print("1. Descarga PostgreSQL 17 para Windows x64")
    print("2. Ejecuta el instalador como administrador")
    print("3. Usa estos valores durante la instalación:")
    print()
    print("   📁 Directorio: C:\\Program Files\\PostgreSQL\\17")
    print("   🔑 Contraseña: admin")
    print("   🌐 Puerto: 5432")
    print("   🌍 Locale: Default locale")
    print()
    print("4. Marca estas opciones:")
    print("   ✅ PostgreSQL Server")
    print("   ✅ pgAdmin 4")
    print("   ✅ Stack Builder")
    print("   ✅ Add PostgreSQL to the PATH")
    print()

def verificar_instalacion():
    """Verificar si PostgreSQL está instalado"""
    print("🔍 Verificando instalación de PostgreSQL...")
    
    try:
        # Verificar comando psql
        resultado = subprocess.run(['psql', '--version'], 
                                 capture_output=True, text=True, timeout=10)
        if resultado.returncode == 0:
            version = resultado.stdout.strip()
            print(f"✅ PostgreSQL detectado: {version}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ PostgreSQL no está instalado o no está en el PATH")
    return False

def verificar_servicio():
    """Verificar si el servicio de PostgreSQL está ejecutándose"""
    print("🔍 Verificando servicio de PostgreSQL...")
    
    try:
        resultado = subprocess.run(['sc', 'query', 'postgresql-x64-17'], 
                                 capture_output=True, text=True, timeout=10)
        if resultado.returncode == 0 and "RUNNING" in resultado.stdout:
            print("✅ Servicio PostgreSQL ejecutándose")
            return True
        else:
            print("⚠️ Servicio PostgreSQL no está ejecutándose")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ No se pudo verificar el servicio")
        return False

def iniciar_servicio():
    """Intentar iniciar el servicio de PostgreSQL"""
    print("🚀 Intentando iniciar el servicio PostgreSQL...")
    
    try:
        resultado = subprocess.run(['sc', 'start', 'postgresql-x64-17'], 
                                 capture_output=True, text=True, timeout=15)
        if resultado.returncode == 0:
            print("✅ Servicio iniciado exitosamente")
            return True
        else:
            print("❌ No se pudo iniciar el servicio")
            print("   Intenta iniciarlo manualmente desde Servicios")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Error al intentar iniciar el servicio")
        return False

def probar_conexion():
    """Probar conexión a PostgreSQL"""
    print("🔌 Probando conexión a PostgreSQL...")
    
    try:
        # Intentar conectar con psql
        comando = ['psql', '-U', 'postgres', '-h', 'localhost', '-p', '5432', '-c', 'SELECT version();']
        resultado = subprocess.run(comando, 
                                 capture_output=True, text=True, timeout=10,
                                 env=dict(os.environ, PGPASSWORD='admin'))
        
        if resultado.returncode == 0:
            print("✅ Conexión exitosa a PostgreSQL")
            return True
        else:
            print("❌ Error de conexión")
            print(f"   Error: {resultado.stderr}")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ No se pudo probar la conexión")
        return False

def crear_base_datos():
    """Crear la base de datos para RMA Recepción"""
    print("🗄️ Creando base de datos rma_recepcion_db...")
    
    try:
        comando = ['psql', '-U', 'postgres', '-h', 'localhost', '-p', '5432', 
                   '-c', 'CREATE DATABASE rma_recepcion_db;']
        resultado = subprocess.run(comando, 
                                 capture_output=True, text=True, timeout=10,
                                 env=dict(os.environ, PGPASSWORD='admin'))
        
        if resultado.returncode == 0:
            print("✅ Base de datos creada exitosamente")
            return True
        elif "already exists" in resultado.stderr:
            print("ℹ️ La base de datos ya existe")
            return True
        else:
            print("❌ Error al crear la base de datos")
            print(f"   Error: {resultado.stderr}")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ No se pudo crear la base de datos")
        return False

def mostrar_pasos_finales():
    """Mostrar pasos finales"""
    print("\n🎉 ¡PostgreSQL 17 configurado exitosamente!")
    print("=" * 50)
    print("Ahora puedes configurar Django:")
    print()
    print("1. Cambiar a PostgreSQL:")
    print("   python cambiar_db.py postgres")
    print()
    print("2. Ejecutar migraciones:")
    print("   python manage.py migrate")
    print()
    print("3. Crear superusuario:")
    print("   python manage.py createsuperuser")
    print()
    print("4. Iniciar el servidor:")
    print("   python manage.py runserver")
    print()
    print("🌐 Accede a tu aplicación en: http://127.0.0.1:8000/")

def main():
    """Función principal"""
    mostrar_banner()
    
    if not verificar_sistema():
        return
    
    print("¿Qué quieres hacer?")
    print("1. Abrir página de descarga")
    print("2. Ver instrucciones de instalación")
    print("3. Verificar instalación")
    print("4. Configurar base de datos")
    print("5. Proceso completo")
    print("6. Salir")
    
    while True:
        try:
            opcion = input("\nSelecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                abrir_descarga()
                
            elif opcion == "2":
                mostrar_instrucciones_instalacion()
                
            elif opcion == "3":
                if verificar_instalacion():
                    if verificar_servicio():
                        probar_conexion()
                    else:
                        print("\n¿Quieres intentar iniciar el servicio? (s/n): ")
                        if input().lower().startswith('s'):
                            iniciar_servicio()
                            
            elif opcion == "4":
                if verificar_instalacion():
                    if verificar_servicio() or iniciar_servicio():
                        if probar_conexion():
                            crear_base_datos()
                            mostrar_pasos_finales()
                            
            elif opcion == "5":
                print("\n🚀 Iniciando proceso completo...")
                abrir_descarga()
                mostrar_instrucciones_instalacion()
                print("\nPresiona Enter cuando hayas completado la instalación...")
                input()
                
                if verificar_instalacion():
                    if verificar_servicio() or iniciar_servicio():
                        if probar_conexion():
                            crear_base_datos()
                            mostrar_pasos_finales()
                            
            elif opcion == "6":
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción inválida. Selecciona 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 