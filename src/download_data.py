# IMPORTACIONES
import pandas as pd
import yfinance as yf

from config import DIR_RAW

# DICCIONARIO DE ACTIVOS (nombre -> ticker de Yahoo Finance)
TICKERS = {
    "SP500": "^GSPC",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Bitcoin": "BTC-USD",
    "Gold": "GC=F",
    "MercadoLibre": "MELI",
}

FECHA_INICIO = "2020-01-01"


def descargar_activo(nombre: str, ticker: str) -> None:
    """Descarga un activo desde Yahoo Finance y lo guarda como CSV."""
    nombre_limpio = nombre.lower().strip()
    print(f"\nDescargando {nombre_limpio} ({ticker})...")

    try:
        df = yf.download(ticker, start=FECHA_INICIO, progress=False)

        if df.empty:
            print(f"[ALERTA] No se encontraron datos para el ticker '{ticker}'.")
            return

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.columns.name = None
        df.index.name = "Date"
        df = df.reset_index()

        archivo = DIR_RAW / f"{nombre_limpio}.csv"
        df.to_csv(archivo, index=False)
        print(f"[OK] {nombre_limpio} guardado en {archivo.name}")

    except Exception as e:
        print(f"[ERROR] Al descargar {nombre_limpio}: {e}")


def ejecutar_descarga() -> None:
    """Recorre el diccionario TICKERS e invoca las descargas."""
    print("Iniciando la descarga automatizada del portafolio...")
    for nombre, ticker in TICKERS.items():
        descargar_activo(nombre, ticker)
    print("\nDescarga de datos finalizada.")


if __name__ == "__main__":
    ejecutar_descarga()
