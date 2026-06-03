"""
plot_baseline_reproduction_scatter.py
======================================

Four-panel emulator-vs-SWAT scatter figure for the validation chapter.
One panel per hydrological indicator. Each panel plots the scenario-engine
output against the SWAT reference value across the 71 sub-basins, with the
1:1 line drawn and R-squared, MAPE, MAE, and RMSE annotated.

Indicator label mapping (matches Table 4.6):
    runoff      -> Runoff (SURQ)
    sediment    -> Sediment (SYLD)
    groundwater -> Recharge (PERC)
    vegetation  -> Evapotranspiration (ET)

Input
-----
- validation_outputs/tables/baseline_reproduction.csv

Output
------
- validation_outputs/figures/fig_baseline_reproduction_scatter.png  (300 dpi)
- validation_outputs/figures/fig_baseline_reproduction_scatter.pdf

Author : Nawwar Procheta, MSc Spatial Engineering, ITC, University of Twente
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(
    r"C:\Users\proch\OneDrive - University of Twente\Desktop\MUJIB_DT\Cesium_71"
)

CSV_PATH = BASE_DIR / "validation_outputs" / "tables" / "baseline_reproduction.csv"

OUT_DIR = BASE_DIR / "validation_outputs" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PNG = OUT_DIR / "fig_baseline_reproduction_scatter.png"
OUT_PDF = OUT_DIR / "fig_baseline_reproduction_scatter.pdf"

PANELS = [
    ("a", "runoff",      "Runoff (SURQ)",           "mm yr$^{-1}$"),
    ("b", "sediment",    "Sediment (SYLD)",         "t ha$^{-1}$ yr$^{-1}$"),
    ("c", "groundwater", "Recharge (PERC)",         "mm yr$^{-1}$"),
    ("d", "vegetation",  "Evapotranspiration (ET)", "mm yr$^{-1}$"),
]

POINT_COLOUR = "#1f77b4"
LINE_11_COLOUR = "#444444"


def compute_metrics(emul, ref):
    """Coefficient of determination is R2 = 1 - SSres/SStot (fit to 1:1)."""
    emul = np.asarray(emul, dtype=float)
    ref = np.asarray(ref, dtype=float)
    finite = np.isfinite(emul) & np.isfinite(ref)
    emul, ref = emul[finite], ref[finite]
    n = emul.size
    mae = float(np.mean(np.abs(emul - ref)))
    rmse = float(np.sqrt(np.mean((emul - ref) ** 2)))
    ss_res = float(np.sum((emul - ref) ** 2))
    ss_tot = float(np.sum((ref - np.mean(ref)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    nonzero = ref != 0
    if nonzero.any():
        mape = float(
            np.mean(np.abs((emul[nonzero] - ref[nonzero]) / ref[nonzero])) * 100.0
        )
    else:
        mape = float("nan")
    return {"n": int(n), "mae": mae, "rmse": rmse, "r2": r2, "mape": mape}


def plot_panel(ax, df_metric, label, units, panel_letter):
    emul = df_metric["scenario_value"].to_numpy()
    ref = df_metric["swat_reference"].to_numpy()
    m = compute_metrics(emul, ref)

    lo = float(min(np.nanmin(emul), np.nanmin(ref)))
    hi = float(max(np.nanmax(emul), np.nanmax(ref)))
    pad = 0.05 * (hi - lo) if hi > lo else 1.0

    line_x = np.array([lo - pad, hi + pad])
    ax.plot(
        line_x, line_x,
        color=LINE_11_COLOUR, lw=1.0, linestyle="--",
        zorder=2, label="1:1 line",
    )

    ax.scatter(
        emul, ref,
        s=22, color=POINT_COLOUR, edgecolor="white",
        linewidths=0.4, alpha=0.85, zorder=3,
    )

    ax.set_xlim(lo - pad, hi + pad)
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_aspect("equal", adjustable="box")

    ax.set_xlabel(f"Emulator value ({units})", fontsize=10)
    ax.set_ylabel(f"SWAT reference ({units})", fontsize=10)
    ax.tick_params(axis="both", labelsize=9)
    ax.grid(True, linestyle=":", linewidth=0.4, color="#bbbbbb", zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    ax.text(
        0.02, 0.97, f"({panel_letter})",
        transform=ax.transAxes, ha="left", va="top",
        fontsize=12, fontweight="bold",
    )
    ax.text(
        0.02, 0.90, label,
        transform=ax.transAxes, ha="left", va="top",
        fontsize=10, fontweight="bold",
    )

    metrics_text = (
        f"n = {m['n']}\n"
        f"R$^{{2}}$ = {m['r2']:.3f}\n"
        f"MAE = {m['mae']:.3f}\n"
        f"RMSE = {m['rmse']:.3f}\n"
        f"MAPE = {m['mape']:.2f} %"
    )
    ax.text(
        0.02, 0.82, metrics_text,
        transform=ax.transAxes, ha="left", va="top",
        fontsize=8.5, family="DejaVu Sans",
        bbox=dict(
            boxstyle="round,pad=0.35", facecolor="white",
            edgecolor="#cccccc", linewidth=0.6, alpha=0.9,
        ),
    )


def build_figure(df):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
    })

    fig, axes = plt.subplots(2, 2, figsize=(10.0, 9.5))
    axes = axes.flatten()

    for ax, (letter, key, label, units) in zip(axes, PANELS):
        df_metric = df[df["metric"] == key].copy()
        if df_metric.empty:
            ax.text(
                0.5, 0.5, "No data",
                transform=ax.transAxes, ha="center", va="center",
            )
            continue
        plot_panel(ax, df_metric, label, units, letter)

    fig.suptitle(
        "Baseline reproduction: scenario-engine emulator vs SWAT reference values",
        fontsize=12, fontweight="bold", y=0.995,
    )

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.005),
        ncol=2, frameon=False, fontsize=9,
    )

    plt.subplots_adjust(left=0.07, right=0.98, top=0.94,
                        bottom=0.07, wspace=0.22, hspace=0.22)
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT_PDF, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] Figure written to:\n  {OUT_PNG}\n  {OUT_PDF}")


if __name__ == "__main__":
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing input: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    required = {"sub_id", "metric", "scenario_value", "swat_reference"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"baseline_reproduction.csv missing columns: {missing}")
    for letter, key, label, _ in PANELS:
        sub = df[df["metric"] == key]
        if sub.empty:
            print(f"[WARN] No rows for metric={key}")
            continue
        m = compute_metrics(
            sub["scenario_value"].to_numpy(),
            sub["swat_reference"].to_numpy(),
        )
        print(
            f"{label:30s}  n={m['n']:3d}  R2={m['r2']:.4f}  "
            f"MAE={m['mae']:.3f}  RMSE={m['rmse']:.3f}  MAPE={m['mape']:.2f}%"
        )
    build_figure(df)
