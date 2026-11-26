# Archivo histórico de datasets

> **Nada de esta carpeta se usa en el artículo.** Se conserva como registro de etapas previas. Los resultados reportados salen únicamente de [`../5.aislar_cuantico_de_parte_clasica/`](../5.aislar_cuantico_de_parte_clasica/). Los esquemas de columnas difieren entre etapas.

> **Datos de IBM (`0.1_ibm_algoritmo/`).** No se utilizan en el artículo y **sus resultados no son verificables desde este repositorio**: no se conserva el código ni los registros que los generaron. Se mantienen solo como archivo, sin que esto implique que sean correctos o incorrectos.

Este directorio contiene los resultados experimentales de etapas previas del proyecto: desde simulación local hasta ejecuciones etiquetadas como hardware IBM Quantum.

**Registros archivados:** 26 archivos CSV, ~54,900 filas (el dataset final, de 22,470 filas, está fuera de esta carpeta).

---

## Índice de carpetas

| Carpeta | Etapa | Tipo | Registros | Estado |
|---------|-------|------|-----------|---------------|
| [`0.0_beta.algoritmo_simulado/`](#00_beta) | Beta — validación inicial | Simulado (clásico) | ~24,200 | Histórico |
| [`0.1_ibm_algoritmo/`](#01_ibm) | IBM Hardware Real | Etiquetado como QPU IBM | ~900 | Histórico, no verificable |
| [`1.gdc_luck_algoritmo_uno/`](#1_gcd) | Iteración 1 — GCD Luck | Simulado | 5,500 | Histórico |
| [`2.algorirmo_dos/`](#2_v2) | Iteración 2 | Simulado + cuántico | 10,250 | Histórico |
| [`3.primer_exito_algoritmo_tres/`](#3_exito) | Iteración 3 — Primer éxito | Simulado + cuántico | 3,120 | Histórico |
| [`4.algoritmo_optimizado_4-17 bits/`](#4_opt) | Iteración 4 — Optimizado | Simulado + cuántico | 10,200 | Histórico |

---

## Descripción detallada por carpeta

---

### `0.0_beta.algoritmo_simulado/` {#00_beta}

**Etapa:** Beta — primera validación del pipeline de datos  
**Tipo:** Simulación clásica (sin circuitos cuánticos reales)  
**Recomendación:** Histórico — muestra el punto de partida del proyecto

**Archivos:**

| Archivo | Filas | Descripción |
|---------|-------|-------------|
| `batch_01.csv` … `batch_09.csv` | 2,200 c/u | Batches independientes de experimentos beta |
| `batch_09_all.csv` | 2,200 | Concatenación completa del batch 9 |
| `batch_09_classical.csv` | 200 | Filtrado: solo ejecuciones clásicas del batch 9 |
| `batch_09_quantum.csv` | 2,000 | Filtrado: solo ejecuciones cuánticas del batch 9 |

**Esquema de columnas:**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `batch_id` | int | Identificador del batch |
| `run_id` | int | Identificador único del experimento |
| `algo` | str | Algoritmo usado: `classical` |
| `N` | int | Número semiprimo a factorizar |
| `N_bits` | int | Tamaño en bits de N |
| `M` | int | Número de shots del circuito |
| `rep` | int | Índice de repetición |
| `success` | bool | `True` si se factorizó correctamente |
| `time_sec` | float | Tiempo de ejecución (segundos) |
| `factors` | str | Factores encontrados (ej: `[3, 5]`) |
| `status` | str | Estado del experimento |
| `seed` | int | Semilla aleatoria para reproducibilidad |

> **Nota:** Esta versión beta **no incluye columnas de hardware IBM** (`hw_backend`, `job_id`). Es la versión preliminar antes de integrar el backend IBM.

---

### `0.1_ibm_algoritmo/` {#01_ibm}

> No utilizado en el artículo; no verificable desde este repositorio.

**Etapa:** Ejecuciones etiquetadas por sus autores como hardware IBM Quantum  
**Tipo:** Etiquetado como backend `ibm_fez`  
**Estado:** histórico; no utilizado en el artículo y no verificable desde este repositorio (el código y los registros que lo generaron no se conservan)

**Archivos:**

| Archivo | Filas | Descripción |
|---------|-------|-------------|
| `batch_01_all.csv` | 260 | Batch 1 completo (clásico + cuántico) |
| `batch_01_classical.csv` | 200 | Batch 1 — solo ejecuciones clásicas (Pollard's Rho, según la documentación anterior; no verificable) |
| `batch_01_quantum.csv` | 60 | Batch 1 — solo ejecuciones en IBM QPU |
| `batch_04_all.csv` | 260 | Batch 4 completo |
| `batch_04_classical.csv` | 200 | Batch 4 — clásico |
| `batch_04_quantum.csv` | 60 | Batch 4 — IBM QPU |
| `batch_05_all.csv` | 260 | Batch 5 completo |
| `batch_05_classical.csv` | 200 | Batch 5 — clásico |
| `batch_05_quantum.csv` | 60 | Batch 5 — IBM QPU |
| `batch_09_quantum.csv` | 60 | Batch 9 — IBM QPU |

**Esquema de columnas (extiende el esquema beta con columnas de hardware):**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `batch_id` | int | Identificador del batch |
| `run_id` | int | ID único del experimento |
| `algo` | str | `classical` o `quantum` |
| `N` | int | Número semiprimo a factorizar |
| `N_bits` | int | Tamaño en bits de N |
| `M` | int | Shots del circuito cuántico |
| `rep` | int | Repetición del experimento |
| `success` | bool | `True` si factorización exitosa |
| `time_sec` | float | Tiempo total incluyendo cola IBM |
| `factors` | str | Factores encontrados |
| `status` | str | `OK_QUANTUM_HARDWARE` / `INSUFFICIENT_COHERENCE` |
| `seed` | float | Semilla aleatoria |
| `hw_backend` | str | Backend IBM declarado (ej: `ibm_fez`) |
| `hw_qubits` | float | Vale 156 en las 240 filas cuánticas: coincide con el tamaño del procesador, no con los qubits del circuito |
| `quantum_seconds` | float | Tiempo de ejecución en QPU declarado (sin cola ni compilación) |
| `job_id` | str | ID de job declarado (su verificación requiere acceso a la cuenta IBM original) |

**Muestra de datos:**
```
N=2773 (12 bits) | backend=ibm_fez | qubits=156 | quantum_sec=4.72 | job_id=d5ltp69h2mqc739a8dig
```

> **Observación:** en los cuatro lotes `*_quantum.csv` (240 filas) todas las filas registran `success = 1` y `status = OK_QUANTUM_HARDWARE`. Estas ejecuciones no se analizaron en el artículo.

---

### `1.gdc_luck_algoritmo_uno/` {#1_gcd}

**Etapa:** Iteración 1 — primera implementación con método GCD Luck  
**Tipo:** Simulado local (Qiskit Aer)  
**Recomendación:** Histórico — sirve como baseline de comparación

**Archivos:**

| Archivo | Filas | Descripción |
|---------|-------|-------------|
| `shor_experiment.csv` | 5,500 | Experimentos con método `gcd_luck` |
| `analysis_plots.png` | — | Visualización de distribuciones |
| `cumulative_probability.png` | — | Probabilidad acumulada de éxito |

**Esquema de columnas:**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `n_bits` | int | Tamaño en bits del número N |
| `N` | int | Número semiprimo |
| `p_true` | int | Factor primo real p (ground truth) |
| `q_true` | int | Factor primo real q (ground truth) |
| `M_shots` | int | Shots del circuito |
| `rep` | int | Repetición |
| `success` | int | 1=éxito, 0=fallo |
| `attempts` | int | Intentos necesarios para factorizar |
| `time_sec` | float | Tiempo de ejecución |
| `qubits_used` | int | Qubits utilizados |
| `method` | str | `gcd_luck` |
| `factors_found` | str | Factores encontrados |

> **Diferencia con versiones posteriores:** Este esquema tiene `qubits_used` y `factors_found` en lugar de `qubits` y sin columna `is_quantum`.

---

### `2.algorirmo_dos/` {#2_v2}

**Etapa:** Iteración 2 — introducción del campo `is_quantum`  
**Tipo:** Simulado local — comienza a distinguir rutas clásica vs cuántica  
**Recomendación:** Histórico

**Archivos:**

| Archivo | Filas | Descripción |
|---------|-------|-------------|
| `shor_experiment_v2.csv` | 10,250 | Experimentos con distinción clásico/cuántico |
| `cumulative_quantum.png` | — | Probabilidad acumulada cuántica |
| `distributions_v2.png` | — | Distribuciones por n_bits |

**Esquema:** Ver **Esquema A** (sección final de este documento).

---

### `3.primer_exito_algoritmo_tres/` {#3_exito}

**Etapa:** Iteración 3 — primer experimento con separación exitosa cuántico/clásico  
**Tipo:** Simulado local  
**Recomendación:** Histórico — hito investigativo relevante

**Archivos:**

| Archivo | Filas | Descripción |
|---------|-------|-------------|
| `shor_experiment_v2.csv` | 3,120 | Dataset reducido del hito de éxito |
| `cumulative_quantum.png` | — | Probabilidad acumulada |
| `distributions_v2.png` | — | Distribuciones |

**Esquema:** Ver **Esquema A**.

---

### `4.algoritmo_optimizado_4-17 bits/` {#4_opt}

**Etapa:** Iteración 4 — algoritmo optimizado con rango ampliado (4–17 bits)  
**Tipo:** Simulado local  
**Recomendación:** Histórico — muestra la progresión del rango experimental

**Archivos:**

| Archivo | Filas | Descripción |
|---------|-------|-------------|
| `shor_experiment_v2.csv` | 10,200 | Cobertura 4–17 bits |
| `cumulative_quantum.png` | — | Probabilidad acumulada |
| `distributions_v2.png` | — | Distribuciones por n_bits |
| `quantum_analysis.png` | — | Análisis cuántico detallado |

**Esquema:** Ver **Esquema A**.

---

### Dataset final

Vive fuera del archivo: ver [`../README.md`](../README.md).

---

## Esquemas de columnas de referencia

### Esquema A — `shor_experiment_v2.csv`
Usado en carpetas: `2.algorirmo_dos`, `3.primer_exito_algoritmo_tres`, `4.algoritmo_optimizado_4-17 bits`, `5.aislar_cuantico_de_parte_clasica`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `n_bits` | int | Tamaño en bits del número N |
| `N` | int | Número semiprimo a factorizar |
| `p_true` | int | Factor primo real p (ground truth) |
| `q_true` | int | Factor primo real q (ground truth) |
| `M_shots` | int | Número de shots del circuito cuántico |
| `rep` | int | Índice de repetición del experimento |
| `success` | int | 1=factorización exitosa, 0=fallo |
| `is_quantum` | int | 1=circuito cuántico, 0=ruta clásica (en el dataset final es idéntico a `success`) |
| `method` | str | `quantum_success`, `gcd_luck`, `failed` |
| `attempts` | int | Intentos necesarios para factorizar |
| `time_sec` | float | Tiempo total de ejecución (segundos) |
| `qubits` | int | Qubits utilizados en el circuito |

### Esquema B — `batch_*_quantum.csv` (IBM Hardware)
Usado en: `0.1_ibm_algoritmo/`

Ver tabla completa en la sección [`0.1_ibm_algoritmo/`](#01_ibm).

### Esquema C — `batch_*.csv` (Beta simulada)
Usado en: `0.0_beta.algoritmo_simulado/`

Ver tabla completa en la sección [`0.0_beta.algoritmo_simulado/`](#00_beta).

---

## Notas de reproducibilidad

- Todos los experimentos simulados usan **Qiskit Aer** como backend local.
- Los datos de IBM se atribuyen a `qiskit-ibm-runtime` (SamplerV2); su código de origen no se conserva en el repositorio.
- La columna `seed` solo existe en los lotes beta e IBM. El dataset final **no tiene `seed`** y no se fijó semilla global, por lo que no es reproducible fila a fila.
- Guía de IBM Quantum (histórica): [`../../docs/archive/ibm_quantum/guia_ibm_quantum.md`](../../docs/archive/ibm_quantum/guia_ibm_quantum.md).

---

*Reorganizado en noviembre de 2026.*
