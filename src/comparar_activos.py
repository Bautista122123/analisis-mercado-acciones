# IMPORTACIONES
import numpy as np
import pandas as pd

from config import DIR_PROCESSED, DIR_REPORTS, dias_anuales


def calcular_resumen_activo(nombre_activo: str, df: pd.DataFrame) -> dict:
    """Calcula las métricas de resumen de un activo ya procesado."""
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    base_anual = dias_anuales(nombre_activo)

    # 1. Retorno total acumulado en todo el período (%)
    retorno_final = df["Retorno_Acumulado"].iloc[-1]

    # 2. Retorno anualizado compuesto (CAGR). Se usan años calendario reales
    #    para que bolsa (252 ruedas) y cripto (365 días) sean comparables.
    anios = (df["Date"].iloc[-1] - df["Date"].iloc[0]).days / 365.25
    cagr = (1 + retorno_final) ** (1 / anios) - 1

    # 3. Volatilidad anualizada
    volatilidad = df["Retorno_Diario"].std() * np.sqrt(base_anual)

    # 4. Máxima caída desde un pico (max drawdown)
    drawdown = df["Close"] / df["Close"].cummax() - 1
    max_drawdown = drawdown.min()

    # 5. Ratio Retorno / Riesgo
    ratio = cagr / volatilidad if volatilidad != 0 else 0

    return {
        "Activo": nombre_activo.upper(),
        "Desde": df["Date"].iloc[0].date(),
        "Hasta": df["Date"].iloc[-1].date(),
        "Dias_Operados": len(df),
        "Retorno_Total_%": round(retorno_final * 100, 2),
        "Retorno_Anualizado_%": round(cagr * 100, 2),
        "Volatilidad_Anual_%": round(volatilidad * 100, 2),
        "Max_Drawdown_%": round(max_drawdown * 100, 2),
        "Ratio_Retorno_Riesgo": round(ratio, 2),
    }


def generar_resumen_comparativo() -> pd.DataFrame | None:
    archivos = sorted(DIR_PROCESSED.glob("*_procesado.csv"))

    if not archivos:
        print(f"[ALERTA] No se encontraron archivos procesados en {DIR_PROCESSED}")
        return None

    print(f"\n[PROCESANDO] Tabla comparativa de {len(archivos)} activos...")
    resultados = []

    for archivo in archivos:
        nombre_activo = archivo.stem.replace("_procesado", "")
        df = pd.read_csv(archivo)

        if df.empty or "Retorno_Diario" not in df.columns:
            continue

        resultados.append(calcular_resumen_activo(nombre_activo, df))

    # Ordenamos por Ratio Retorno/Riesgo y agregamos ranking
    df_resumen = pd.DataFrame(resultados)
    df_resumen = df_resumen.sort_values(
        by="Ratio_Retorno_Riesgo", ascending=False
    ).reset_index(drop=True)
    df_resumen.insert(0, "Ranking", df_resumen.index + 1)

    ruta_reporte = DIR_REPORTS / "resumen_comparativo.csv"
    df_resumen.to_csv(ruta_reporte, index=False)

    print("\n" + "=" * 60)
    print("            RANKING COMPARATIVO DE ACTIVOS")
    print("=" * 60)
    print(df_resumen.drop(columns=["Desde", "Hasta"]).to_string(index=False))
    print("=" * 60)
    print(f"[OK] Tabla comparativa guardada en: {ruta_reporte.name}\n")

    return df_resumen


def generar_matriz_correlacion() -> pd.DataFrame | None:
    """Correlación de retornos diarios entre activos (solo fechas comunes)."""
    archivos = sorted(DIR_PROCESSED.glob("*_procesado.csv"))
    if not archivos:
        return None

    precios = {}
    for archivo in archivos:
        nombre = archivo.stem.replace("_procesado", "").upper()
        df = pd.read_csv(archivo, usecols=["Date", "Close"])
        df["Date"] = pd.to_datetime(df["Date"])
        precios[nombre] = df.set_index("Date")["Close"]

    # Nos quedamos con los días en que operaron todos los activos y recién
    # ahí calculamos retornos (así el movimiento de fin de semana de Bitcoin
    # queda incluido en el retorno del lunes, en vez de perderse)
    df_retornos = pd.DataFrame(precios).dropna().pct_change().dropna()
    correlacion = df_retornos.corr().round(2)

    ruta = DIR_REPORTS / "matriz_correlacion.csv"
    correlacion.to_csv(ruta)
    print(f"[OK] Matriz de correlación guardada en: {ruta.name}")
    return correlacion
