# BIOMED

## Descripción
Proyecto académico de gestión de versiones y configuraciones de parámetros clínicos simulados para BIOMED S.A.C.

## Objetivo
Implementar control de versiones y procesos de integración y entrega continua (CI/CD) mediante GitHub Actions.

## Tecnologías
- Git y GitHub
- GitHub Actions
- JSON y XML
- Python 3 (biblioteca estándar)

## Estructura del repositorio

```text
BIOMED/
├── .github/workflows/
│   ├── ci-json.yml       # Valida la sintaxis JSON
│   ├── ci-xml.yml        # Valida la sintaxis XML
│   ├── cd-entrega.yml    # Genera un ZIP descargable
│   └── qa-python.yml     # Ejecuta el programa y pruebas automáticas
├── config/
│   ├── rangos_diagnostico_molecular.json
│   └── plantilla_evaluacion_ocupacional.xml
├── src/
│   └── validador_configuraciones.py
├── test/
│   └── test_validador.py
├── .gitignore
└── README.md
```

## Ejecución local

Desde la carpeta raíz del repositorio, con Python 3 instalado:

```bash
python src/validador_configuraciones.py
python -m unittest discover -s test -p "test_*.py" -v
```

En Windows, también puede usarse `py` en lugar de `python`, si el lanzador está instalado.

## Automatización
- **CI JSON**: verifica la sintaxis de los archivos JSON.
- **CI XML**: verifica la sintaxis de los archivos XML.
- **QA Python**: ejecuta el validador y las pruebas unitarias.
- **CD**: genera el paquete descargable de configuraciones del proyecto.

## Alcance
El proyecto utiliza configuraciones académicas y datos ficticios. La validación es técnica: comprueba estructura y coherencia básica de archivos, **no** la validez de parámetros médicos ni diagnósticos. No está destinado al uso clínico real.
