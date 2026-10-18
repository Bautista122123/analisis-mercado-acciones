# IMPORTAMOS LIBRERIAS   
import pandas as pd  
import yfinance as yf 
from pathlib import Path 

# CONFIGURACIÓN DE RUTAS
DATA_DIR = Path("data/raw") 
DATA_DIR.mkdir(parents=True, exist_ok=True) 

# DICCIONARIO DE ACTIVOS
TICKERS = {
    'SP500': '^GSPC',
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'Nvidia': 'NVDA',
    'Bitcoin': 'BTC-USD',
    'Gold': 'GC=F',
    'mercadolibre': 'MELI'
}

def descargar_activo(nombre: str, ticker: str) -> None:
    """Descarga un activo desde Yahoo Finance y lo guarda como CSV."""
    nombre_limpio = nombre.lower().strip()
    print(f"\nConectando con Yahoo Finance para descargar {nombre_limpio} ({ticker})...")

    try:
        df = yf.download(ticker, start="2020-01-01", progress=False)

        if df.empty:
            print(f"⚠️ No se encontraron datos para el ticker '{ticker}'.")
            return

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.columns.name = None
        df.index.name = 'Date'
        df = df.reset_index()

        archivo = DATA_DIR / f"{nombre_limpio}.csv"
        df.to_csv(archivo, index=False)
        print(f"✅ ¡{nombre_limpio} guardado con éxito en: {archivo}!")
        
    except Exception as e:
        print(f"❌ Error al descargar {nombre_limpio}: {e}")

def ejecutar_descarga() -> None:
    """Recorre el diccionario TICKERS e invoca las descargas."""
    print("🚀 Iniciando la descarga automatizada de portafolio...")
    for nombre, ticker in TICKERS.items():
        descargar_activo(nombre, ticker)
    print("\n🏁 Descarga de datos finalizada correctamente.")

# SI SE EJECUTA ESTE ARCHIVO DIRECTAMENTE, NO HACE NADA
if __name__ == "__main__":
    pass
