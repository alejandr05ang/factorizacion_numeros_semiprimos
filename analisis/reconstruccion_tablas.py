"""
RECONSTRUCCIÓN de los cálculos del artículo desde el CSV publicado.

Genera (por defecto en analisis/tablas_reconstruidas/):
  tabla_V_VI_por_bits.csv          Tablas V y VI (proporciones, Wilson 95 %, umbrales k, qubits)
  tabla_VII_por_shots.csv          Tabla VII (resultados agregados por presupuesto de shots)
  tabla_VIII_rangos_k.csv          Tabla VIII (rangos de k propagados desde el intervalo de Wilson)
  correlaciones.csv                Matriz de correlación de Pearson (Fig. 6)
  lista_semiprimos.csv             Lista realizada de los 107 semiprimos
  resumen_semiprimo_shots.csv      Resumen por semiprimo x shots (749 filas)

y compara los resultados con los valores publicados en el artículo (ver VERIFICACION).

AVISO: este NO es el script original del artículo (no se conserva). Es una reconstrucción
hecha a partir del CSV. No repite el experimento ni usa Qiskit. Es determinista.

Uso:
    python analisis/reconstruccion_tablas.py [--csv RUTA] [--salida CARPETA]

Por defecto escribe en analisis/tablas_reconstruidas/, sea cual sea el directorio actual.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from comun import (CSV_POR_DEFECTO, SALIDA_TABLAS, cargar_csv, correlaciones, lista_semiprimos,
                   resumen_por_bits, resumen_por_semiprimo_shots, resumen_por_shots)

# ---------------------------------------------------------------------------------------
# VERIFICACION: valores publicados en el artículo (se copiaron a mano de las Tablas V-VIII
# y del texto de la Sección V-E). Solo se usan para comprobar la reconstrucción.
# ---------------------------------------------------------------------------------------
# bits: (exitos, p, wilson_inf, wilson_sup, k095, k099, qubits)   -> Tablas V y VI
PUBLICADO_V_VI = {
    4: (210, 1.0000, 0.9820, 1.0000, 1, 1, 12),
    5: (103, 0.4905, 0.4236, 0.5577, 5, 7, 15),
    6: (479, 0.3802, 0.3538, 0.4073, 7, 10, 18),
    7: (760, 0.4021, 0.3802, 0.4244, 6, 9, 19),
    8: (858, 0.4086, 0.3877, 0.4297, 6, 9, 20),
    9: (1073, 0.5110, 0.4896, 0.5323, 5, 7, 21),
    10: (1040, 0.4952, 0.4739, 0.5166, 5, 7, 22),
    11: (1102, 0.5248, 0.5034, 0.5461, 5, 7, 23),
    12: (699, 0.3329, 0.3130, 0.3533, 8, 12, 24),
    13: (59, 0.0281, 0.0218, 0.0361, 106, 162, 25),
    14: (118, 0.0562, 0.0471, 0.0669, 52, 80, 26),
    15: (26, 0.0124, 0.0085, 0.0181, 241, 370, 27),
    16: (4, 0.0019, 0.0007, 0.0049, 1572, 2416, 28),
}
# shots: (exitos, p, tiempo_medio, tiempo_mediana)   -> Tabla VII
PUBLICADO_VII = {
    50: (364, 0.1134, 0.2534, 0.2775), 100: (502, 0.1564, 0.2517, 0.2751),
    500: (815, 0.2539, 0.4829, 0.2916), 1024: (996, 0.3103, 0.2628, 0.3119),
    2048: (1137, 0.3542, 0.2858, 0.3432), 4096: (1294, 0.4031, 0.3321, 0.3990),
    8192: (1423, 0.4433, 0.4253, 0.5116),
}
# bits: (k095_min, k095_max, k099_min, k099_max)   -> Tabla VIII
PUBLICADO_VIII = {
    4: (1, 1, 1, 2), 5: (4, 6, 6, 9), 6: (6, 7, 9, 11), 7: (6, 7, 9, 10), 8: (6, 7, 9, 10),
    9: (4, 5, 7, 7), 10: (5, 5, 7, 8), 11: (4, 5, 6, 7), 12: (7, 8, 11, 13),
    13: (82, 136, 126, 209), 14: (44, 63, 67, 96), 15: (165, 353, 253, 542),
    16: (612, 4042, 940, 6213),
}
# (columna_a, columna_b): coeficiente citado en el texto de la Sección V-E
PUBLICADO_CORR = {("n_bits", "success"): -0.393, ("M_shots", "success"): 0.209,
                  ("n_bits", "time_sec"): 0.007, ("n_bits", "qubits"): 0.992,
                  ("attempts", "success"): -0.856}


def verificar(bits, shots, corr) -> int:
    """Compara con lo publicado. Devuelve el número de diferencias."""
    dif = 0

    def chequea(nombre, obtenido, publicado):
        nonlocal dif
        if obtenido != publicado:
            dif += 1
            print(f"  DIFIERE  {nombre}: reconstruido={obtenido} publicado={publicado}")

    rd = lambda x, d: float(round(float(x), d))
    b = bits.set_index("bits")
    for n, (s, p, lo, hi, k95, k99, q) in PUBLICADO_V_VI.items():
        r = b.loc[n]
        chequea(f"V/VI {n} bits", (int(r.exitos), rd(r.p, 4), rd(r.wilson_inf, 4),
                                   rd(r.wilson_sup, 4), int(r.k095), int(r.k099), int(r.qubits)),
                (s, p, lo, hi, k95, k99, q))
    for n, rango in PUBLICADO_VIII.items():
        r = b.loc[n]
        chequea(f"VIII {n} bits", (int(r.k095_min), int(r.k095_max), int(r.k099_min), int(r.k099_max)), rango)
    t = shots.set_index("M_shots")
    for m, (s, p, mt, md) in PUBLICADO_VII.items():
        r = t.loc[m]
        chequea(f"VII {m} shots", (int(r.exitos), rd(r.p, 4), rd(r.tiempo_medio, 4),
                                   rd(r.tiempo_mediana, 4)), (s, p, mt, md))
    for (a, c), v in PUBLICADO_CORR.items():
        chequea(f"corr({a},{c})", rd(corr.loc[a, c], 3), v)
    return dif


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=str(CSV_POR_DEFECTO), help="CSV de referencia (solo lectura)")
    ap.add_argument("--salida", default=str(SALIDA_TABLAS), help="carpeta de salida")
    a = ap.parse_args()

    df = cargar_csv(a.csv)
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)

    bits, shots = resumen_por_bits(df), resumen_por_shots(df)
    corr = correlaciones(df)
    bits.drop(columns=[c for c in bits.columns if c.endswith(("_min", "_max"))]).round(6) \
        .to_csv(salida / "tabla_V_VI_por_bits.csv", index=False)
    shots.round(6).to_csv(salida / "tabla_VII_por_shots.csv", index=False)
    bits[["bits", "k095", "k095_min", "k095_max", "k099", "k099_min", "k099_max"]] \
        .to_csv(salida / "tabla_VIII_rangos_k.csv", index=False)
    corr.round(6).to_csv(salida / "correlaciones.csv")
    lista_semiprimos(df).round(6).to_csv(salida / "lista_semiprimos.csv", index=False)
    resumen_por_semiprimo_shots(df).round(6).to_csv(salida / "resumen_semiprimo_shots.csv", index=False)

    print(f"Filas: {len(df)} | éxitos: {int(df.success.sum())} | semiprimos: {df.N.nunique()}")
    print(f"Archivos escritos en: {salida.resolve()}")
    print("Verificación contra los valores publicados (Tablas V-VIII y correlaciones):")
    dif = verificar(bits, shots, corr)
    print("  Todo coincide." if dif == 0 else f"  {dif} diferencias.")
    return 0 if dif == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
