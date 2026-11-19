# CONFIGURACIÓN CENTRAL DE RUTAS
# Las rutas se calculan desde la ubicación de este archivo, así el pipeline
# funciona igual si se ejecuta desde la raíz del proyecto o desde src/.
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DIR_RAW = BASE_DIR / "data" / "raw"
DIR_PROCESSED = BASE_DIR / "data" / "processed"
DIR_REPORTS = BASE_DIR / "reports"
DIR_FIGURES = DIR_REPORTS / "figures"

for carpeta in (DIR_RAW, DIR_PROCESSED, DIR_REPORTS, DIR_FIGURES):
    carpeta.mkdir(parents=True, exist_ok=True)

# Activos que operan los 365 días del año (mercado continuo)
ACTIVOS_365_DIAS = ["bitcoin", "ethereum", "btc", "eth"]


def dias_anuales(nombre_activo: str) -> int:
    """365 días para cripto, 252 ruedas hábiles para bolsa."""
    return 365 if nombre_activo.lower() in ACTIVOS_365_DIAS else 252
