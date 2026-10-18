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
    ruta_entrada = DIR_RAW / f"{nombre_activo}.csv"
    ruta_salida = DIR_PROCESSED / f"{nombre_activo}_procesado.csv"
    
    if not ruta_entrada.exists():
        print(f"❌ Error: No se encontró el archivo para '{nombre_activo}' en {ruta_entrada}")
        return
        
    print(f"\n🔄 Procesando análisis para: {nombre_activo}...")
    
    # 1. Leer el CSV limpio que genera el nuevo download_data
    df = pd.read_csv(ruta_entrada)
    
    # 2. Convertir directamente a datetime (ya no hay texto basura que lo rompa)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 3. Ordenar cronológicamente y limpiar el índice numérico
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    # 4. Guardar en la carpeta de procesados
    df.to_csv(ruta_salida, index=False)
    print(f"✅ {nombre_activo} analizado y guardado en {ruta_salida}")
