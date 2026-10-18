# IMPORTAMOS LIBRERIAS   
import pandas as pd  #Libreria para la utilización de tablas y funcionalidades para manejar datos
import yfinance as yf #Importamos la libreria de yahoo finance de la cual descargamos los datos de las acciones
from pathlib import Path #Libreria para manejo de rutas

DATA_DIR = Path("data/raw") # Ruta donde se guardarán los datos crudos
DATA_DIR.mkdir(parents=True, exist_ok=True) #Crea la carpeta

def descargar_activo(nombre: str, ticker: str) -> None:
    """
    Descarga un activo desde Yahoo Finance y lo guarda como CSV en data/raw.
    """
    nombre_limpio = nombre.lower().strip()
    print(f"\nConectando con Yahoo Finance para descargar {nombre_limpio} ({ticker})...")

    try:
        # Descarga directa usando tus parámetros analizados
        df = yf.download(ticker, start="2020-01-01", progress=False)

        # Validación por si el operador escribe mal el ticker o no hay internet
        if df.empty:
            print(f"⚠️ No se encontraron datos para el ticker '{ticker}'. Verificá si está bien escrito.")
            return

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.index.name = 'Date'

        # El archivo se guarda directamente en la carpeta compartida data/raw
        archivo = DATA_DIR / f"{nombre_limpio}.csv"
        df.to_csv(archivo)
    
        print(f"✅ ¡{nombre_limpio} guardado con éxito en: {archivo}!")
        
    except Exception as e: # CORREGIDO: el bug de la 'e' solucionado
        print(f"❌ Error al descargar {nombre_limpio}: {e}")

if __name__ == "__main__":
    print("--- INICIANDO PRUEBA DE FUNCIONAMIENTO ---")
    
    # 1. Pedimos los datos interactivamente por consola
    ticker_test = input("Ingresá un ticker para probar (ej: AAPL o BTC-USD): ").strip()
    nombre_test = input("Ingresá el nombre del archivo (ej: apple o bitcoin): ").strip()
    
    # 2. Ejecutamos la función
    descargar_activo(nombre=nombre_test, ticker=ticker_test)