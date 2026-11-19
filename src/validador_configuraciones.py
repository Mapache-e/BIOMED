"""Validaciones tecnicas de las configuraciones academicas de BIOMED.

No realiza diagnosticos ni verifica validez clinica de los parametros.
"""

import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET


def validar_configuraciones(carpeta):
    """Comprueba estructura JSON, rangos numericos y estructura XML."""
    carpeta = Path(carpeta)
    ruta_json = carpeta / "rangos_diagnostico_molecular.json"
    ruta_xml = carpeta / "plantilla_evaluacion_ocupacional.xml"

    with ruta_json.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if not isinstance(datos, dict) or datos.get("sistema") != "BIOMED":
        raise ValueError("El JSON debe pertenecer al sistema BIOMED")

    parametros = datos.get("parametros")
    if not isinstance(parametros, list) or not parametros:
        raise ValueError("El JSON debe contener parametros")

    codigos = set()

    for indice, parametro in enumerate(parametros, start=1):
        if not isinstance(parametro, dict):
            raise ValueError(f"Parametro {indice}: estructura incorrecta")

        codigo = parametro.get("codigo")
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError(f"Parametro {indice}: codigo obligatorio")

        codigo_normalizado = codigo.strip().upper()
        if codigo_normalizado in codigos:
            raise ValueError(f"Parametro {indice}: codigo duplicado")

        codigos.add(codigo_normalizado)

        rango = parametro.get("rango_referencia")
        if not isinstance(rango, dict):
            raise ValueError(f"Parametro {indice}: falta rango_referencia")

        minimo = rango.get("minimo")
        maximo = rango.get("maximo")
        for valor in (minimo, maximo):
            if (
                not isinstance(valor, (int, float))
                or isinstance(valor, bool)
                or not math.isfinite(valor)
            ):
                raise ValueError(f"Parametro {indice}: limites no numericos")

        if minimo > maximo:
            raise ValueError(f"Parametro {indice}: minimo mayor que maximo")

    raiz = ET.parse(ruta_xml).getroot()
    if raiz.tag != "plantillaEvaluacionOcupacional":
        raise ValueError("La raiz del XML no es la esperada")
    if raiz.findtext("sistema") != "BIOMED":
        raise ValueError("El XML debe pertenecer al sistema BIOMED")

    return True


if __name__ == "__main__":
    ruta_config = Path(__file__).resolve().parent.parent / "config"
    validar_configuraciones(ruta_config)
    print("Configuraciones BIOMED validadas correctamente")