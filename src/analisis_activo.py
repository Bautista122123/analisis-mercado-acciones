# IMPORTACIONES
import pandas as pd

from config import DIR_PROCESSED, DIR_RAW


def calcular_metricas(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia el DataFrame y agrega métricas de retorno, tendencia y riesgo."""
    df_limpio = df.copy()
    df_limpio["Date"] = pd.to_datetime(df_limpio["Date"])
    df_limpio = df_limpio.drop_duplicates(subset=("Date",), keep="first")
    df_limpio = df_limpio.sort_values(by="Date").reset_index(drop=True)

    # Retornos
    df_limpio["Retorno_Diario"] = df_limpio["Close"].pct_change()
    df_limpio["Retorno_Acumulado"] = (
        1 + df_limpio["Retorno_Diario"]
    ).cumprod() - 1

    # Tendencia
    df_limpio["Media_Movil_20"] = df_limpio["Close"].rolling(window=20).mean()
    df_limpio["Media_Movil_50"] = df_limpio["Close"].rolling(window=50).mean()

    # Riesgo
    df_limpio["Volatilidad_20d"] = (
        df_limpio["Retorno_Diario"].rolling(window=20).std()
    )
    # Drawdown: caída porcentual desde el máximo histórico alcanzado
    maximo_historico = df_limpio["Close"].cummax()
    df_limpio["Drawdown"] = df_limpio["Close"] / maximo_historico - 1

    return df_limpio


def analizar_activo(nombre_activo: str) -> None:
    ruta_entrada = DIR_RAW / f"{nombre_activo}.csv"
    ruta_salida = DIR_PROCESSED / f"{nombre_activo}_procesado.csv"

    if not ruta_entrada.exists():
        print(
            f"[ERROR] No se encontró el archivo para '{nombre_activo}' en"
            f" {ruta_entrada}"
        )
        return

    print(f"[PROCESANDO] Análisis para: {nombre_activo}...")
    df = pd.read_csv(ruta_entrada)
    df_procesado = calcular_metricas(df)
    df_procesado.to_csv(ruta_salida, index=False)
    print(f"[OK] {nombre_activo} analizado y guardado en {ruta_salida.name}")
