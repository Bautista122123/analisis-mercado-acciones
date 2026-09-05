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

    print(f"Descargando {nombre}...")

    df = yf.download(
        ticker,
        start="2020-01-01",
        progress=False
    )

    archivo = DATA_DIR / f"{nombre}.csv"
    df.to_csv(archivo)

    print(f"✅ {nombre} guardado en {archivo}")


def main():
    """
    Función principal del programa.
    """

    for nombre, ticker in TICKERS.items():
        descargar_activo(nombre, ticker)

    print("\n Descarga finalizada.")


if __name__ == "__main__":
    main()