#================================================================
#IMPORTACIONES
#================================================================
import pandas as pd
from pathlib import Path

# Ruta del archivo que queremos analizar
DIR_RAW = Path("data/raw")

def explorar_activo(nombre_activo: str) -> None: 
    ruta=DIR_RAW / f"{nombre_activo}.csv"
    if not ruta.exists():
        print(f"❌ No se puede explorar: No existe {ruta}")
        return
    # Muestra activo en consola
    print(f"\n--- EDA INICIAL: {nombre_activo.upper()} ---") 
    # Leer el archivo
    df = pd.read_csv(ruta)

    print("Dimensiones:", df.shape)
    print("Columnas:", df.columns.tolist())
    print(df.head(2))