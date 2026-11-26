# Datasets

| Ubicación | Uso | Descripción |
|-----------|-----|-------------|
| [`5.aislar_cuantico_de_parte_clasica/`](5.aislar_cuantico_de_parte_clasica/) | **Artículo** | Dataset final: 22.470 filas × 12 columnas. Única fuente de los resultados numéricos del artículo. |
| [`archive/`](archive/) | Histórico | Etapas previas y datos de IBM. **No se usan en el artículo.** Total archivado: 26 CSV, ~54.900 filas. |

## Dataset final: `5.aislar_cuantico_de_parte_clasica/shor_experiment_v2.csv`

Una fila por *ejecución externa* (hasta 10 intentos internos): 6.531 con `success = 1` (`method = quantum_success`) y 15.939 con `success = 0` (`method = failed`).

**Diseño.** 107 semiprimos únicos de 4 a 16 bits: 1 (4 bits), 1 (5), 6 (6), 9 (7) y 10 por nivel de 8 a 16 bits. El diseño **no está balanceado por nivel**. 7 presupuestos de shots (50, 100, 500, 1024, 2048, 4096, 8192) × 30 repeticiones: (1+1+6+9+9·10) × 7 × 30 = 22.470. Simulación ideal con `AerSimulator`, sin `NoiseModel` y sin semilla global.

| Columna | Descripción |
|---------|-------------|
| `n_bits`, `N` | Longitud en bits y valor del semiprimo |
| `p_true`, `q_true` | Factores primos reales (para validar) |
| `M_shots` | Presupuesto de shots por circuito |
| `rep` | Repetición 1–30 dentro de cada (N, shots) |
| `success` | 1 si se recuperó un factor no trivial; 0 en otro caso |
| `is_quantum` | **Idéntica a `success`** en este CSV; no es un indicador independiente de que se ejecutó un circuito |
| `method` | `quantum_success` o `failed` (no contiene `gcd_luck`) |
| `attempts` | Intentos internos **consumidos** (máximo 10; los fallos registran siempre 10) |
| `time_sec` | Duración registrada de la ejecución externa |
| `qubits` | Qubits **totales** del circuito (12 a 28); no es `n_bits` |

Los motivos intermedios de rechazo (periodo no recuperable, orden impar, raíz trivial) no se registraron.

**Figuras (`*.png` de esa carpeta).** Son las que generó el notebook en la corrida original (`cumulative_quantum`, `distributions_v2`, `quantum_analysis`, `force_quantum_analysis`, `risk_dashboard_final`, `shots_efficiency`). **No son las figuras del artículo**, y algunas conservan etiquetas heredadas con la palabra "ruido" que no corresponden a esta simulación ideal (ver el README raíz).
