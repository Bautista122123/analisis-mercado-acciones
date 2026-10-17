# IMPORTAMOS LIBRERIAS   

import pandas as pd 
import yfinance as yf
from pathlib import Path

# Carpeta donde se guardarán los datos
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Activos a descargar
TICKERS = {
    "SP500": "^GSPC",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Bitcoin": "BTC-USD",
    "Gold": "GC=F"
}


def descargar_activo(nombre: str, ticker: str) -> None:
    """
    Descarga un activo desde Yahoo Finance y lo guarda como CSV.
    """

    print(f"Descargando {nombre} ({ticker})...")

    try:
        
        df = yf.download(
            ticker,
            start="2020-01-01",
            progress=False
        )

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.index.name = 'Date'

        archivo = DATA_DIR / f"{nombre}.csv"
        df.to_csv(archivo)
    
        print(f"✅ {nombre} guardado en {archivo}")
    except Exception as es:
                # Captura el error en 'e' y lo muestra en consola sin detener el programa
        print(f"❌ Error al descargar {nombre}: {e}")

def ejecutar_descarga() -> None:
    """
    Función principal del programa.
    """

    for nombre, ticker in TICKERS.items():
        descargar_activo(nombre, ticker)

    print("\n Descarga finalizada.")
