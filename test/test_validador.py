"""Pruebas automáticas del validador de BIOMED (unittest)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROYECTO))
from src.validador_configuraciones import validar_configuraciones


class TestValidadorConfiguraciones(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.carpeta = Path(temporal.name)
        self.json_path = self.carpeta / "rangos_diagnostico_molecular.json"
        self.xml_path = self.carpeta / "plantilla_evaluacion_ocupacional.xml"
        self.datos = {
            "sistema": "BIOMED",
            "version": "1.1.0",
            "parametros": [{
                "codigo": "MOL-001",
                "rango_referencia": {
                    "minimo": 0,
                    "maximo": 100,
                    "unidad": "indice",
                },
            }],
        }
        self.guardar_json()
        self.xml_path.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<plantillaEvaluacionOcupacional>'
            '<sistema>BIOMED</sistema>'
            '</plantillaEvaluacionOcupacional>',
            encoding="utf-8",
        )

    def guardar_json(self):
        self.json_path.write_text(
            json.dumps(self.datos, ensure_ascii=False), encoding="utf-8"
        )

    def test_configuracion_valida(self):
        self.assertTrue(validar_configuraciones(self.carpeta))

    def test_codigo_duplicado(self):
        self.datos["parametros"].append({
            "codigo": "MOL-001",
            "rango_referencia": {
                "minimo": 1,
                "maximo": 2,
                "unidad": "indice",
            },
        })
        self.guardar_json()
        with self.assertRaisesRegex(ValueError, "codigo duplicado"):
            validar_configuraciones(self.carpeta)

    def test_rango_invertido(self):
        rango = self.datos["parametros"][0]["rango_referencia"]
        rango["minimo"] = 200
        self.guardar_json()
        with self.assertRaises(ValueError):
            validar_configuraciones(self.carpeta)

    def test_limite_no_numerico(self):
        rango = self.datos["parametros"][0]["rango_referencia"]
        rango["maximo"] = "cien"
        self.guardar_json()
        with self.assertRaises(ValueError):
            validar_configuraciones(self.carpeta)

    def test_parametros_vacios(self):
        self.datos["parametros"] = []
        self.guardar_json()
        with self.assertRaises(ValueError):
            validar_configuraciones(self.carpeta)

    def test_xml_incorrecto(self):
        self.xml_path.write_text(
            "<plantilla><sin-cierre>", encoding="utf-8"
        )
        with self.assertRaises(Exception):
            validar_configuraciones(self.carpeta)

    def test_archivo_faltante(self):
        self.xml_path.unlink()
        with self.assertRaises(FileNotFoundError):
            validar_configuraciones(self.carpeta)

    def test_archivos_actuales_del_repositorio(self):
        self.assertTrue(validar_configuraciones(RAIZ_PROYECTO / "config"))


if __name__ == "__main__":
    unittest.main()