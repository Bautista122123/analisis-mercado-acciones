# IMPORTACIONES
import pandas as pd

from config import DIR_RAW


def explorar_activo(nombre_activo: str) -> None:
    """EDA inicial: dimensiones, rango de fechas y valores nulos."""
    ruta = DIR_RAW / f"{nombre_activo}.csv"
    if not ruta.exists():
        print(f"[ERROR] No se puede explorar: no existe {ruta}")
        return

    df = pd.read_csv(ruta)

    print(f"\n--- EDA INICIAL: {nombre_activo.upper()} ---")
    print("Dimensiones:", df.shape)
    print("Columnas:", df.columns.tolist())
    print(f"Rango de fechas: {df['Date'].min()} -> {df['Date'].max()}")
    print("Valores nulos:", int(df.isna().sum().sum()))
    print(df.head(2))
