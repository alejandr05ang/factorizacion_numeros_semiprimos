# Factorización de semiprimos: pipeline inspirado en Shor y dataset

Código y datos del artículo **"Empirical Success and Cumulative Repetition Risk in a Shor-Inspired Factorization Simulation"** (Bravo-Quezada, Sáenz-Arias, Espinoza-Narváez, Angamarca-Avendaño; GIHP4C, Universidad Politécnica Salesiana, Cuenca, Ecuador).

El repositorio contiene un análisis estadístico auditable de un pipeline *inspirado en Shor*, ejecutado con **Qiskit Aer en simulación local ideal** (sin `NoiseModel`): **22.470 ejecuciones externas**, semiprimos de **4 a 16 bits**, 7 presupuestos de shots (50–8192) y 30 repeticiones por configuración.

> **Alcance.** Los porcentajes caracterizan *este* pipeline y *este* dataset. No son una probabilidad intrínseca del algoritmo de Shor, no miden decoherencia, ruido ni error de hardware, y no se extrapolan a tamaños criptográficos (RSA). El artículo no compara contra métodos clásicos. Para N ≠ 15 el circuito inyecta una fase calculada clásicamente; no hay exponenciación modular coherente.

## Qué respalda al artículo

| Elemento | Ubicación |
|----------|-----------|
| Notebook del experimento | [`ComputacionCuantica.ipynb`](ComputacionCuantica.ipynb) |
| Dataset de referencia (22.470 filas, 12 columnas) | [`datasets/5.aislar_cuantico_de_parte_clasica/shor_experiment_v2.csv`](datasets/5.aislar_cuantico_de_parte_clasica/shor_experiment_v2.csv) |
| Diccionario de datos | [`datasets/README.md`](datasets/README.md) |
| Recálculo de tablas y figuras desde el CSV (reconstrucción) | [`analisis/`](analisis/) |

Todo lo que está en `archive/` es material histórico: **no se usa para ningún resultado del artículo**.

> La ruta del CSV y el notebook están citados en el artículo (*Data and Code Availability*). No se renombran ni se mueven.

## Estructura

```
.
├── ComputacionCuantica.ipynb      # Notebook del experimento final (se conserva tal como se ejecutó)
├── LICENSE                        # MIT (código y documentación)
├── requirements.txt               # Dependencias (versiones reconstruidas, ver Reproducibilidad)
├── analisis/                      # Reconstrucción de Wilson, Tablas V–VIII y Figuras 1–6 desde el CSV
├── datasets/
│   ├── README.md                  # Diccionario de datos del dataset final
│   ├── 5.aislar_cuantico_de_parte_clasica/   # Dataset del artículo (CSV + figuras del notebook)
│   └── archive/                   # Etapas previas y datos de IBM (no usados en el artículo)
├── notebooks/archive/             # Notebooks de iteraciones previas
└── docs/archive/ibm_quantum/      # Guía y configuración de IBM Quantum (no usadas en el artículo)
```

## Instalación

```bash
git clone https://github.com/Alejandr05ang/factorizacion_numeros_semiprimos.git
cd factorizacion_numeros_semiprimos
python -m venv .venv
.\.venv\Scripts\activate        # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
```

## Reproducibilidad

- **Reanálisis:** el CSV publicado es la referencia; los números del artículo salen de él.
- **Regeneración:** ejecutar las celdas de `ComputacionCuantica.ipynb` en orden. **No se fijó ninguna semilla** (ni NumPy, ni el barajado de semiprimos, ni el simulador), así que una nueva corrida reproduce los patrones agregados pero no los valores fila a fila, e incluso la lista de semiprimos puede cambiar desde los 8 bits.
- El notebook escribe su salida en `datasets/` (`DATA_DIR = "datasets"`), no en la carpeta del dataset publicado. Por tanto, una nueva corrida no sobrescribe el CSV de referencia, y el CSV publicado se ubicó en `5.aislar_cuantico_de_parte_clasica/` después de la ejecución.
- **Versiones:** el notebook registra Python 3.12.8. Las versiones de `requirements.txt` (Qiskit 2.3.0, Aer 0.17.2, NumPy 2.4.1, pandas 3.0.0, SciPy 1.17.0, Matplotlib 3.10.8, tqdm 4.67.1) se **reconstruyeron del entorno virtual archivado en git** (commit b2121766). No existe un `pip freeze` del experimento original.

## Notas sobre el notebook

El notebook se conserva sin modificar, tal como se ejecutó. Algunos textos heredados no coinciden con la terminología del artículo:

- **"Real".** En "rendimiento cuántico REAL" y "éxito cuántico real", *real* significa que se descartan los éxitos por gcd clásico (`FORCE_QUANTUM = True`). La ejecución es simulación ideal, no hardware.
- **"Ruido".** Etiquetas como "Fracaso (Timeout/Ruido)", "Fallo (Ruido/Shots)" o "limitado por ruido/decoherencia simulada" son incorrectas: **no hay ruido simulado**. Los fallos son ejecuciones que agotaron los 10 intentos sin recuperar un factor.
- **"Intentos".** `attempts` es el número de intentos internos consumidos (máximo 10). En la fórmula de riesgo acumulado, "k intentos" equivale a *k ejecuciones externas* (filas del CSV) del artículo. La fórmula 1 − (1 − p̂)^k estima la probabilidad de **al menos un éxito** en k ejecuciones.
- **Rango de bits.** El comentario "4 a 17 bits" es erróneo: `range(4, 17)` llega a 16.
- **Motivos de fallo.** Se calculan en el código (`fail_no_period`, `fail_r_odd`, `fail_trivial_root`) pero no se guardan en el CSV.

## Tablas y figuras del artículo

El notebook no calcula los intervalos de Wilson, la Tabla VIII ni las figuras del artículo, y el script original con el que se hicieron no se conserva. [`analisis/`](analisis/) los **reconstruye** desde el CSV y comprueba que coinciden con los valores publicados. Las figuras que el notebook guardó en la carpeta del dataset son otras (ver `datasets/README.md`).

## Cómo citar

> E. A. Angamarca-Avendaño, J. G. Sáenz-Arias, and J. A. Espinoza-Narváez, "Factorización de números semiprimos: Shor-inspired simulation pipeline and dataset," GitHub repository, 2026. [Online]. Available: https://github.com/alejandr05ang/factorizacion_numeros_semiprimos

## Licencia

- **Código y documentación** (notebooks, `analisis/` y textos): [MIT](LICENSE).
- **Datos** (carpeta `datasets/`, incluido el CSV de referencia y las figuras que contiene): [CC BY 4.0](datasets/LICENSE). Al reutilizarlos, cite a los autores y este repositorio (sección anterior).

Copyright (c) 2026 Edwin A. Angamarca-Avendaño, Josué G. Sáenz-Arias, Jordy A. Espinoza-Narváez y Omar G. Bravo-Quezada.
