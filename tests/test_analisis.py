from pathlib import Path
import sys
import unittest
import pandas as pd

# Agregamos la carpeta 'src' al path para poder importar los módulos
RUTA_SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.append(str(RUTA_SRC))

from analisis_activo import calcular_metricas


class TestAnalisisActivo(unittest.TestCase):

    def setUp(self):
        # Creamos un DataFrame pequeño y controlado de 3 días para probar
        self.datos_prueba = pd.DataFrame({
            "Date": ("2026-01-01", "2026-01-02", "2026-01-03"),
            "Close": (100.0, 110.0, 99.0),
            "High": (105.0, 112.0, 102.0),
            "Low": (98.0, 108.0, 95.0),
            "Open": (99.0, 100.0, 110.0),
            "Volume": (1000, 1500, 1200),
        })

    def test_calculo_retornos(self):
        resultado = calcular_metricas(self.datos_prueba)
        retornos_diarios = tuple(resultado["Retorno_Diario"])
        retornos_acumulados = tuple(resultado["Retorno_Acumulado"])

        # Día 1: No hay día anterior, debe ser nulo (NaN)
        self.assertTrue(pd.isna(retornos_diarios[0]))

        # Día 2: De 100 a 110 es +10% (0.10)
        self.assertAlmostEqual(retornos_diarios[1], 0.10, places=4)

        # Día 3: De 110 a 99 es -10% (-0.10)
        self.assertAlmostEqual(retornos_diarios[2], -0.10, places=4)

        # Retorno acumulado final: De 100 a 99 es -1% (-0.01)
        self.assertAlmostEqual(retornos_acumulados[2], -0.01, places=4)

    def test_limpieza_duplicados_y_orden(self):
        # Agregamos una fila desordenada y otra con fecha duplicada
        datos_sucios = pd.DataFrame({
            "Date": ("2026-01-03", "2026-01-01", "2026-01-01"),
            "Close": (99.0, 100.0, 999.0),
        })

        resultado = calcular_metricas(datos_sucios)
        cierres = tuple(resultado["Close"])

        # Debe quedar con 2 filas únicas y ordenadas por fecha
        self.assertEqual(len(resultado), 2)
        self.assertEqual(cierres[0], 100.0)
        self.assertEqual(cierres[1], 99.0)

    def test_columnas_generadas(self):
        resultado = calcular_metricas(self.datos_prueba)
        columnas_esperadas = (
            "Retorno_Diario",
            "Retorno_Acumulado",
            "Media_Movil_20",
            "Media_Movil_50",
            "Volatilidad_20d",
            "Drawdown",
        )
        for col in columnas_esperadas:
            self.assertIn(col, resultado.columns)

    def test_drawdown(self):
        # Precio sube a 110 y cae a 99: la caída desde el máximo es -10%
        resultado = calcular_metricas(self.datos_prueba)
        drawdowns = tuple(resultado["Drawdown"])
        self.assertAlmostEqual(drawdowns[0], 0.0, places=4)
        self.assertAlmostEqual(drawdowns[1], 0.0, places=4)
        self.assertAlmostEqual(drawdowns[2], -0.10, places=4)
        # El drawdown nunca puede ser positivo
        self.assertTrue((resultado["Drawdown"] <= 0).all())


if __name__ == "__main__":
    unittest.main()
