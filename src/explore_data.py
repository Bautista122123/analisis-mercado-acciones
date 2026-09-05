import pandas as pd
from pathlib import Path

# Ruta del archivo que queremos analizar
archivo = Path("data/raw/Apple.csv")

# Leer el archivo
df = pd.read_csv(archivo)

# Mostrar las primeras filas
print("=== Primeras 5 filas ===")
print(df.head())

print("\n=== Información del DataFrame ===")
print(df.info())

print("\n=== Dimensiones ===")
print(df.shape)

print("\n=== Columnas ===")
print(df.columns)