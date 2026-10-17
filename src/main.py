# ================================================================
# IMPORTACIONES
# ================================================================

from pathlib import Path

#Funciones de modulos 'scr'
from download_data import ejecutar_descarga
from explore_data import explorar_activo
from analisis_activo import analizar_activo

#Ruta de la carpeta que queremos escanear
DIR_RAW = Path("data/raw")

def main():
    # Verificamos si la carpeta NO existe, o si existe pero está vacía (no hay .csv)
    if not DIR_RAW.exists() or not list(DIR_RAW.glob("*.csv")):
        print(f"⚠️ No se detectaron archivos .csv en '{DIR_RAW}'. Iniciando descarga automática...")
        ejecutar_descarga()

    #Buscamos todos los archivos .csv y extraemos su nombres limpios
    lista_activos= [archivo.stem for archivo in DIR_RAW.glob("*.csv")]

    #Control por si la carpeta esta vacia
    if not lista_activos:
        print(f"⚠️ Alerta: No se encontraron archivos .csv en la carpeta {DIR_RAW}")
        return

    print(f" Se detectaron{len(lista_activos)} para analizar:{lista_activos}\n")

    for activo in lista_activos:
        print(f"--- Iniciando procesamiento para:{activo.upper()} --- ")
        # Etapa 1: Exploración inicial (EDA)
        explorar_activo(activo)

        # Etapa 2
        analizar_activo(activo)
        print(f"Procesamiento completo para {activo}\n")

if __name__== "__main__":
    main()