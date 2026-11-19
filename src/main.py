# IMPORTACIONES
import sys

from analisis_activo import analizar_activo
from comparar_activos import generar_matriz_correlacion, generar_resumen_comparativo
from config import DIR_RAW
from explore_data import explorar_activo
from visualizar_datos import generar_visualizaciones


def main() -> None:
    print("=" * 50)
    print("   SISTEMA CENTRALIZADO DE ANÁLISIS FINANCIERO")
    print("=" * 50)

    # ETAPA 0: Descarga opcional.
    #   python src/main.py --descargar   -> descarga sin preguntar
    #   python src/main.py --local       -> usa los CSV locales sin preguntar
    if "--descargar" in sys.argv:
        opcion = "s"
    elif "--local" in sys.argv:
        opcion = "n"
    else:
        opcion = input("¿Desea descargar o actualizar los datos? (s/n): ").strip().lower()

    if opcion == "s":
        from download_data import ejecutar_descarga  # requiere internet

        ejecutar_descarga()
    else:
        print("[INFO] Omitiendo descarga. Se utilizarán los archivos locales.")

    lista_activos = sorted(archivo.stem for archivo in DIR_RAW.glob("*.csv"))
    if not lista_activos:
        print(f"[ALERTA] No se encontraron archivos .csv en {DIR_RAW}")
        return

    print(f"\nSe detectaron {len(lista_activos)} activos: {lista_activos}")

    # ETAPAS 1 y 2: exploración y procesamiento de cada activo
    for activo in lista_activos:
        print("-" * 50)
        explorar_activo(activo)
        analizar_activo(activo)

    # ETAPAS 3 y 4: se ejecutan UNA sola vez, con todos los activos procesados
    generar_resumen_comparativo()
    generar_matriz_correlacion()
    generar_visualizaciones()

    print("Pipeline finalizado. Resultados en la carpeta reports/.")


if __name__ == "__main__":
    main()
