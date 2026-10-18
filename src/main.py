# IMPORTACIONES
from pathlib import Path
# Funciones de modulos 'src'
from download_data import ejecutar_descarga
from explore_data import explorar_activo
from analisis_activo import analizar_activo

# Ruta de las carpetas de datos
DIR_RAW = Path("data/raw")
DIR_PROCESSED = Path("data/processed")

def main():
    print("==================================================")
    print("   SISTEMA CENTRALIZADO DE ANÁLISIS FINANCIERO   ")
    print("==================================================")
    
    # ETAPA 0: Descarga automatizada y limpieza inicial desde el origen
    ejecutar_descarga()
    print("\n==================================================")
    print("   INICIANDO PIPELINE DE EXPLORACIÓN Y ANÁLISIS  ")
    print("==================================================")

    # Buscamos todos los archivos .csv y extraemos sus nombres limpios
    lista_activos = [archivo.stem for archivo in DIR_RAW.glob("*.csv")]

    # Control por si la carpeta esta vacia
    if not lista_activos:
        print(f"⚠️ Alerta: No se encontraron archivos .csv en la carpeta {DIR_RAW}")
        return

    print(f"Se detectaron {len(lista_activos)} activos para analizar: {lista_activos}\n")

    for activo in lista_activos:
        print(f"--- Iniciando procesamiento para: {activo.upper()} --- ")
        
        # Etapa 1: Exploración inicial (EDA)
        explorar_activo(activo)
        
        # Etapa 2: Análisis y transformación de datos
        analizar_activo(activo)
        
        print(f"✅ Procesamiento completo para {activo}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()
