"""
Utilidades compartidas por los scripts de reconstrucción del análisis.

RECONSTRUCCIÓN. Este código NO es el script original con el que se calcularon las
tablas y figuras del artículo (ese script no se conserva). Se reescribió después, solo
a partir del CSV publicado, para que cualquiera pueda recalcular los mismos números.
No ejecuta el experimento, no usa Qiskit y es determinista: el CSV es de solo lectura.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DIR_ANALISIS = Path(__file__).resolve().parent
SALIDA_TABLAS = DIR_ANALISIS / "tablas_reconstruidas"
SALIDA_IMAGENES = DIR_ANALISIS / "imagenes_reconstruidas"
CSV_POR_DEFECTO = RAIZ / "datasets" / "5.aislar_cuantico_de_parte_clasica" / "shor_experiment_v2.csv"

Z95 = 1.96  # cuantil normal para el intervalo de Wilson del 95 %


def cargar_csv(ruta: Path | str | None = None) -> pd.DataFrame:
    """Lee el CSV de referencia y comprueba su estructura básica."""
    ruta = Path(ruta) if ruta else CSV_POR_DEFECTO
    df = pd.read_csv(ruta)
    esperadas = ["n_bits", "N", "p_true", "q_true", "M_shots", "rep", "success",
                 "is_quantum", "method", "attempts", "time_sec", "qubits"]
    if list(df.columns) != esperadas:
        raise ValueError(f"Columnas inesperadas en {ruta}: {list(df.columns)}")
    return df


def wilson(exitos: int, n: int, z: float = Z95) -> tuple[float, float]:
    """Intervalo de Wilson para una proporción (Ec. de Wilson, sin corrección de continuidad)."""
    p = exitos / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    mitad = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centro - mitad, min(centro + mitad, 1.0)


def k_tau(p: float, tau: float) -> int:
    """Ec. (6): mínimo de ejecuciones externas para alcanzar probabilidad acumulada tau."""
    if p >= 1.0:
        return 1
    if p <= 0.0:
        raise ValueError("p = 0: k no está definido")
    return math.ceil(math.log(1 - tau) / math.log(1 - p))


def prob_acumulada(p: float, k):
    """Ec. (5): P(al menos un éxito en k ejecuciones externas) = 1 - (1 - p)^k."""
    return 1 - (1 - p) ** np.asarray(k, dtype=float)


def resumen_por_bits(df: pd.DataFrame) -> pd.DataFrame:
    """Tablas V y VI: conteos, proporción, Wilson, umbrales k y qubits por nivel de bits."""
    filas = []
    for bits, g in df.groupby("n_bits"):
        n, s = len(g), int(g.success.sum())
        p = s / n
        lo, hi = wilson(s, n)
        filas.append({
            "bits": bits, "N_unicos": g.N.nunique(), "ejecuciones": n, "exitos": s,
            "p": p, "wilson_inf": lo, "wilson_sup": hi,
            "k095": k_tau(p, 0.95), "k099": k_tau(p, 0.99),
            # Tabla VIII: k es decreciente en p, así que el límite superior de p da el k mínimo
            "k095_min": k_tau(hi, 0.95), "k095_max": k_tau(lo, 0.95),
            "k099_min": k_tau(hi, 0.99), "k099_max": k_tau(lo, 0.99),
            "qubits": int(g.qubits.max()),
        })
    return pd.DataFrame(filas)


def resumen_por_shots(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla VII: resultados agregados por presupuesto de shots."""
    g = df.groupby("M_shots")
    t = g.agg(ejecuciones=("success", "size"), exitos=("success", "sum"),
              tiempo_medio=("time_sec", "mean"), tiempo_mediana=("time_sec", "median"))
    t["p"] = t.exitos / t.ejecuciones
    return t.reset_index()


def resumen_por_semiprimo_shots(df: pd.DataFrame) -> pd.DataFrame:
    """Resumen por (N, shots): 107 semiprimos x 7 presupuestos = 749 filas de 30 repeticiones."""
    t = (df.groupby(["n_bits", "N", "p_true", "q_true", "M_shots"])
           .success.agg(repeticiones="size", exitos="sum", p="mean").reset_index())
    return t


def lista_semiprimos(df: pd.DataFrame) -> pd.DataFrame:
    """Lista realizada de semiprimos (la selección usó barajado sin semilla; no es regenerable)."""
    base = df[["n_bits", "N", "p_true", "q_true"]].drop_duplicates().sort_values(["n_bits", "N"])
    tasa = df.groupby("N").success.agg(ejecuciones="size", exitos="sum", p="mean").reset_index()
    return base.merge(tasa, on="N").reset_index(drop=True)


def proporcion_por_semiprimo(df: pd.DataFrame) -> pd.DataFrame:
    """Proporción de éxito de cada semiprimo (todas sus ejecuciones), base de la Fig. 3."""
    return df.groupby(["n_bits", "N"]).success.mean().rename("p").reset_index()


def correlaciones(df: pd.DataFrame) -> pd.DataFrame:
    """Fig. 6: Pearson por filas. `is_quantum` se omite porque es idéntica a `success`."""
    cols = ["n_bits", "M_shots", "time_sec", "qubits", "attempts", "success"]
    return df[cols].corr()
