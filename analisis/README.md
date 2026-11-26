# analisis/: reconstrucción de las tablas y figuras del artículo

**Reconstrucción de las tablas (V–VIII) y figuras (1–6) del artículo, recalculadas a partir del CSV de `datasets/5.aislar_cuantico_de_parte_clasica/`.** El script original no se conserva: estos scripts reemplazan el cálculo, no las imágenes originales.

> **Esto es una reconstrucción, no el script original.** El código con el que se calcularon originalmente los intervalos de Wilson, la Tabla VIII y las figuras del artículo no se conserva. Estos scripts se reescribieron después, solo a partir del CSV publicado, con las mismas definiciones (Ecs. 4–6 del artículo). No repiten el experimento, no usan Qiskit, no modifican el CSV y son deterministas.

## Qué calculan

| Script | Salida | Artículo |
|--------|--------|----------|
| `reconstruccion_tablas.py` | `tabla_V_VI_por_bits.csv` | Tablas V y VI: proporciones, Wilson 95 %, k₀.₉₅, k₀.₉₉, qubits |
| | `tabla_VII_por_shots.csv` | Tabla VII: resultados por presupuesto de shots |
| | `tabla_VIII_rangos_k.csv` | Tabla VIII: rangos de k propagados desde el intervalo de Wilson |
| | `correlaciones.csv` | Fig. 6: matriz de Pearson |
| | `lista_semiprimos.csv` | Lista realizada de los 107 semiprimos (la selección usó barajado sin semilla) |
| | `resumen_semiprimo_shots.csv` | Resumen por semiprimo × shots (749 filas, 30 repeticiones cada una) |
| `reconstruccion_figuras.py` | `fig1…fig6_*.png` | Figuras 1 a 6 |
| `comun.py` | (módulo compartido) | Lectura del CSV, Wilson, k, resúmenes |

`reconstruccion_tablas.py` **compara el resultado con los valores publicados** (Tablas V–VIII y los coeficientes de correlación citados en el texto) y devuelve un error si algo difiere. Con el CSV publicado, todo coincide.

## Uso

Desde la raíz del repositorio, con las dependencias de `requirements.txt` (solo se usan pandas, NumPy y Matplotlib):

```bash
python analisis/reconstruccion_tablas.py
python analisis/reconstruccion_figuras.py
```

Las tablas se escriben por defecto en `analisis/tablas_reconstruidas/` y las imágenes en `analisis/imagenes_reconstruidas/`, sea cual sea el directorio desde el que se ejecute. Opciones: `--csv RUTA` (por defecto el CSV de `datasets/5.aislar_cuantico_de_parte_clasica/`) y `--salida CARPETA`.

## Límites

- Las **figuras** reproducen los mismos datos y definiciones, pero no son las originales: el estilo puede diferir (versión de Matplotlib, tamaños y márgenes). Las etiquetas están en inglés para coincidir con el artículo.
- Los valores publicados que usa la verificación se copiaron a mano de las Tablas V–VIII del artículo.
- Los **números** salen del CSV y no dependen de la versión de las librerías; solo el aspecto de las figuras puede variar.
