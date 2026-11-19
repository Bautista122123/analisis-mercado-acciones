# IMPORTACIONES
import matplotlib
import pandas as pd

# Modo sin interfaz gráfica: los gráficos se guardan como PNG
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import DIR_FIGURES, DIR_PROCESSED, DIR_REPORTS

plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False})


def _cargar_procesados(columnas: list[str]) -> dict[str, pd.DataFrame]:
    """Lee los CSV procesados y devuelve {NOMBRE: DataFrame con Date}."""
    datos = {}
    for archivo in sorted(DIR_PROCESSED.glob("*_procesado.csv")):
        nombre = archivo.stem.replace("_procesado", "").upper()
        df = pd.read_csv(archivo, usecols=["Date", *columnas])
        df["Date"] = pd.to_datetime(df["Date"])
        datos[nombre] = df
    return datos


def _guardar(fig, nombre_archivo: str) -> None:
    fig.tight_layout()
    ruta = DIR_FIGURES / nombre_archivo
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    print(f"[OK] Gráfico guardado en: figures/{nombre_archivo}")


# GRÁFICO 1: MAPA DE RIESGO VS. RETORNO ANUALIZADO
def graficar_riesgo_retorno() -> None:
    ruta_resumen = DIR_REPORTS / "resumen_comparativo.csv"
    if not ruta_resumen.exists():
        print(f"[ALERTA] No se encontró {ruta_resumen} para graficar.")
        return

    df = pd.read_csv(ruta_resumen)
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        df["Volatilidad_Anual_%"], df["Retorno_Anualizado_%"],
        s=120, color="#1f77b4", edgecolors="black", alpha=0.85, zorder=3,
    )
    for _, fila in df.iterrows():
        ax.annotate(
            fila["Activo"],
            (fila["Volatilidad_Anual_%"], fila["Retorno_Anualizado_%"]),
            textcoords="offset points", xytext=(0, 10),
            ha="center", fontsize=9, fontweight="bold",
        )

    ax.axhline(df["Retorno_Anualizado_%"].mean(), color="gray", linestyle="--",
               linewidth=1, alpha=0.7, label="Retorno promedio")
    ax.axvline(df["Volatilidad_Anual_%"].mean(), color="red", linestyle="--",
               linewidth=1, alpha=0.7, label="Volatilidad promedio")

    ax.set_title("Riesgo vs. retorno anualizado (2020 - 2026)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Volatilidad anualizada (%)")
    ax.set_ylabel("Retorno anualizado - CAGR (%)")
    ax.grid(True, linestyle=":", alpha=0.6, zorder=0)
    ax.legend()
    _guardar(fig, "mapa_riesgo_retorno.png")


# GRÁFICO 2: EVOLUCIÓN DE USD 100 INVERTIDOS (escala logarítmica)
def graficar_evolucion_retornos() -> None:
    datos = _cargar_procesados(["Retorno_Acumulado"])
    if not datos:
        print(f"[ALERTA] No se encontraron archivos en {DIR_PROCESSED}")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    for nombre, df in datos.items():
        valor = 100 * (1 + df["Retorno_Acumulado"].fillna(0))
        ax.plot(df["Date"], valor, label=nombre, linewidth=1.4)

    # Escala log: sin ella, NVIDIA (+3.000%) aplasta al resto de los activos
    ax.set_yscale("log")
    ax.set_title("Evolución de USD 100 invertidos en enero 2020 (escala log)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Valor de la inversión (USD)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", ncols=2)
    _guardar(fig, "evolucion_retornos_acumulados.png")


# GRÁFICO 3: MÁXIMA CAÍDA (MAX DRAWDOWN) POR ACTIVO
def graficar_drawdown() -> None:
    ruta_resumen = DIR_REPORTS / "resumen_comparativo.csv"
    if not ruta_resumen.exists():
        print(f"[ALERTA] No se encontró {ruta_resumen} para graficar.")
        return

    df = pd.read_csv(ruta_resumen).sort_values("Max_Drawdown_%")
    fig, ax = plt.subplots(figsize=(10, 5.5))
    barras = ax.barh(df["Activo"], df["Max_Drawdown_%"], color="#d62728", alpha=0.8)
    ax.bar_label(barras, fmt="%.1f%%", padding=4, fontsize=9)

    ax.set_title("Peor caída desde un máximo (max drawdown, 2020 - 2026)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Max drawdown (%)")
    ax.set_xlim(df["Max_Drawdown_%"].min() * 1.15, 0)
    ax.grid(True, axis="x", linestyle=":", alpha=0.6)
    _guardar(fig, "drawdown.png")


# GRÁFICO 4: MAPA DE CALOR DE CORRELACIONES
def graficar_correlacion() -> None:
    ruta = DIR_REPORTS / "matriz_correlacion.csv"
    if not ruta.exists():
        print(f"[ALERTA] No se encontró {ruta} para graficar.")
        return

    corr = pd.read_csv(ruta, index_col=0)
    fig, ax = plt.subplots(figsize=(8, 7))
    imagen = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)

    ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr.index)), corr.index)
    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            valor = corr.iat[i, j]
            ax.text(j, i, f"{valor:.2f}", ha="center", va="center", fontsize=8,
                    color="white" if abs(valor) > 0.6 else "black")

    ax.set_title("Correlación de retornos diarios", fontsize=13, fontweight="bold")
    fig.colorbar(imagen, ax=ax, shrink=0.8)
    _guardar(fig, "matriz_correlacion.png")


# FUNCIÓN PRINCIPAL DEL MÓDULO
def generar_visualizaciones() -> None:
    print("\n[PROCESANDO] Generando visualizaciones en reports/figures...")
    graficar_riesgo_retorno()
    graficar_evolucion_retornos()
    graficar_drawdown()
    graficar_correlacion()
