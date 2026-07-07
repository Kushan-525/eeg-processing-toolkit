# EEG Data Pipeline & Processing Toolkit 🧠📊

Este repositorio contiene un pipeline modular, optimizado y de alto rendimiento desarrollado en **Python** para la gestión de datos de **Electroencefalografía (EEG)**. Está diseñado específicamente para automatizar el flujo de trabajo en estudios clínicos de **sueño y epilepsia**, facilitando la transición desde datos crudos o binarios hasta formatos de almacenamiento científico de última generación.

## 🚀 Características Principales

- **Organización Universal:** Clasificación automatizada de archivos de entrada ordenándolos por carpetas estructuradas de pacientes basados en nomenclatura clínica (`SZ` para crisis y patrones estructurados para sueño).
- **Procesamiento de Alto Rendimiento:** Uso de **Polars** para lecturas y transformaciones masivas a velocidades significativamente superiores a las librerías tradicionales de manipulación de datos.
- **Ingeniería de Características:** Inserción dinámica de frecuencias de muestreo (128Hz, 200Hz y 250Hz) según el registro del sujeto y cálculo de vectores de tiempo de alta precisión.
- **Optimización de Almacenamiento:** Serialización directa a formatos **Apache Parquet** (comprimido con Snappy) y **JSON**, reduciendo drásticamente el espacio en disco y acelerando las lecturas posteriores.
- **Visualización Avanzada:** Integración con **MNE-Python** para el mapeo topográfico espacial de 19 canales según el **Sistema Internacional 10-20** con visualizadores de ondas interactivos.

## 📁 Estructura del Proyecto

```text
├── organizar_datasets.py      # Script 1: Clasificación de archivos crudos
├── procesar_eeg.py            # Script 2: Pipeline de Polars a Parquet/JSON
├── visualizar_eeg.py          # Script 3: Visor interactivo con MNE
├── 1_organizar_datos.bat      # Automatizador de organización (Windows)
├── 2_procesar_y_comprimir.bat # Automatizador de procesamiento individual (Windows)
├── ejecutar_completo.bat      # Automatizador del pipeline completo (Windows)
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación del sistema
```
