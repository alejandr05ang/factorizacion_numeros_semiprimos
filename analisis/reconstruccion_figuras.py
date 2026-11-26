"""
RECONSTRUCCIÓN de las seis figuras del artículo desde el CSV publicado.
Se escriben por defecto en analisis/imagenes_reconstruidas/.

  fig1_almacenamiento_teorico.png   Fig. 1  almacenamiento teórico mínimo del vector de estado
  fig2_exito_por_bits_wilson.png    Fig. 2  proporción de éxito por tamaño, con Wilson 95 %
  fig3_variabilidad_semiprimos.png  Fig. 3  proporciones por semiprimo dentro de cada nivel
  fig4_presupuesto_de_shots.png     Fig. 4  éxito frente a presupuesto de shots, por régimen
  fig5_probabilidad_acumulada.png   Fig. 5  probabilidad acumulada 1-(1-p)^k
  fig6_correlaciones.png            Fig. 6  matriz de correlación de Pearson

AVISO: NO son las figuras originales ni se generaron con el script original (no se conserva).
Reproducen los mismos datos con las mismas definiciones, pero el estilo puede diferir
ligeramente (versión de Matplotlib, tamaños, márgenes). Las etiquetas están en inglés para
coincidir con el artículo. No repite el experimento ni usa Qiskit.

Uso:
    python analisis/reconstruccion_figuras.py [--csv RUTA] [--salida CARPETA]

Por defecto escribe en analisis/imagenes_reconstruidas/, sea cual sea el directorio actual.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # sin ventana: solo escribe archivos
import matplotlib.pyplot as plt
import numpy as np

from comun import (CSV_POR_DEFECTO, SALIDA_IMAGENES, cargar_csv, correlaciones, prob_acumulada,
                   proporcion_por_semiprimo, resumen_por_bits)

DPI = 150


def guardar(fig, carpeta: Path, nombre: str) -> None:
    fig.tight_layout()
    fig.savefig(carpeta / nombre, dpi=DPI)
    plt.close(fig)
    print("  escrita", carpeta / nombre)


def fig1(df, carpeta):
    q = df.groupby("n_bits").qubits.max()
    gib = (2.0 ** q) * 16 / 2 ** 30  # Ec. (2): 2^q amplitudes x 16 bytes
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.semilogy(q.index, gib.values, "o-", markersize=4)
    ax.set_title("Theoretical minimum storage using the circuit qubit counts recorded in the CSV")
    ax.set_xlabel("Semiprime size (bits)")
    ax.set_ylabel("Minimum state-vector storage (GiB, 16 bytes/amplitude)")
    ax.set_xticks(list(q.index))
    ax.grid(True, which="both", alpha=0.3)
    guardar(fig, carpeta, "fig1_almacenamiento_teorico.png")


def fig2(bits, carpeta):
    p = bits.p.values
    err = np.vstack([p - bits.wilson_inf.values, bits.wilson_sup.values - p])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.errorbar(bits.bits, p, yerr=err, fmt="o-", capsize=3, markersize=4)
    ax.annotate("N=15 specialized validation case", xy=(4, 1.0), xytext=(5.2, 0.93),
                arrowprops=dict(arrowstyle="-", color="black"), fontsize=8)
    ax.set_title("Empirical success by problem size with 95% Wilson intervals")
    ax.set_xlabel("Semiprime size (bits)")
    ax.set_ylabel("Empirical success proportion")
    ax.set_xticks(list(bits.bits))
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    guardar(fig, carpeta, "fig2_exito_por_bits_wilson.png")


def fig3(df, carpeta):
    por_n = proporcion_por_semiprimo(df)
    niveles = sorted(por_n.n_bits.unique())
    datos = [por_n[por_n.n_bits == b].p.values for b in niveles]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    # Mediana naranja y media como triángulo verde: valores por defecto de Matplotlib
    ax.boxplot(datos, positions=niveles, widths=0.6, showmeans=True)
    ax.set_title("Within-bit variability across semiprime instances")
    ax.set_xlabel("Semiprime size (bits)")
    ax.set_ylabel("Per-semiprime empirical success proportion")
    ax.set_xticks(niveles)
    ax.set_xticklabels(niveles)
    ax.grid(True, alpha=0.3)
    guardar(fig, carpeta, "fig3_variabilidad_semiprimos.png")


def fig4(df, carpeta):
    series = {
        "All observations": df,
        "5-12 bits (excludes N=15)": df[(df.n_bits >= 5) & (df.n_bits <= 12)],
        "13-16 bits": df[df.n_bits >= 13],
    }
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for nombre, sub in series.items():
        t = sub.groupby("M_shots").success.mean()
        ax.plot(t.index, t.values, "o-", label=nombre, markersize=4)
    ax.set_xscale("log")
    ax.set_title("Measurement budget effect by experimental regime")
    ax.set_xlabel("Measurement shots (log scale)")
    ax.set_ylabel("Empirical success proportion")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    guardar(fig, carpeta, "fig4_presupuesto_de_shots.png")


def fig5(bits, carpeta):
    b = bits.set_index("bits")
    k = np.logspace(0, 3.5, 400)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for n in (5, 8, 12, 13, 15, 16):
        p = b.loc[n, "p"]
        ax.plot(k, prob_acumulada(p, k), label=f"{n} bits (p={p:.4f})")
    ax.axhline(0.95, color="tab:blue", linestyle="--", linewidth=1, label="Target 0.95")
    ax.axhline(0.99, color="gray", linestyle=":", linewidth=1, label="Target 0.99")
    ax.set_xscale("log")
    ax.set_title("Cumulative success probability from empirical per-execution rates")
    ax.set_xlabel("Independent external executions, k (log scale)")
    ax.set_ylabel("Estimated probability of at least one success")
    ax.set_ylim(0, 1.02)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7, ncol=2, loc="lower right")
    guardar(fig, carpeta, "fig5_probabilidad_acumulada.png")


def fig6(df, carpeta):
    c = correlaciones(df)
    etiquetas = list(c.columns)
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(c.values, cmap="viridis", vmin=-1, vmax=1)
    ax.set_xticks(range(len(etiquetas)))
    ax.set_yticks(range(len(etiquetas)))
    ax.set_xticklabels(etiquetas, rotation=45, ha="right")
    ax.set_yticklabels(etiquetas)
    for i in range(len(etiquetas)):
        for j in range(len(etiquetas)):
            v = c.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                    color="white" if (v + 1) / 2 < 0.35 else "black")
    fig.colorbar(im, ax=ax, label="Pearson correlation")
    ax.set_title("Descriptive correlation matrix of recorded variables")
    guardar(fig, carpeta, "fig6_correlaciones.png")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=str(CSV_POR_DEFECTO), help="CSV de referencia (solo lectura)")
    ap.add_argument("--salida", default=str(SALIDA_IMAGENES), help="carpeta de salida de las imágenes")
    a = ap.parse_args()

    df = cargar_csv(a.csv)
    carpeta = Path(a.salida)
    carpeta.mkdir(parents=True, exist_ok=True)
    bits = resumen_por_bits(df)
    print(f"Escribiendo figuras en {carpeta.resolve()}")
    fig1(df, carpeta)
    fig2(bits, carpeta)
    fig3(df, carpeta)
    fig4(df, carpeta)
    fig5(bits, carpeta)
    fig6(df, carpeta)


if __name__ == "__main__":
    main()
