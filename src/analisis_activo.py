#IMPORTACIONES
import pandas as pd
from pathlib import Path

#CONFIGURACIÓN DE ENTORNO
DIR_RAW= Path("data/raw")
DIR_PROCESSED= Path("data/processed")

#Aseguramos que la carpeta de destino exista
DIR_PROCESSED.mkdir(parents=True, exist_ok=True)

#FUNCIÓN DE ANÁLISIS DATA WRANGLING
def analizar_activo(nombre_activo: str) -> None:
    """
    Carga el archivo CSV de un activo, calcula sus rendimientos diarios, muestra un reporte en consola
    """
    ruta_entrada= DIR_RAW / f"{nombre_activo}.csv"
    ruta_salida= DIR_PROCESSED / f"{nombre_activo}_procesado.csv"

    if not ruta_entrada.exists():
        print(f"❌ Error: No se encontró el archivo para '{nombre_activo}' en {ruta_entrada}")
        return

    print(f"\n🔄 Procesando análisis para: {nombre_activo}...")

    #Carga y preparación
    df= pd.read_csv(ruta_entrada) #.read_csv
    df['date']=pd.to_datetime(df['date'])
    df= df.sort_values(by='date').reset_index(drop=True)
    
    #Guardado de datos 
    df.to_csv(ruta_salida, index=False)
    print(f"💾 Archivo ordenado guardado con éxito en: {ruta_salida}")
