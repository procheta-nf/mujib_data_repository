"""
plot_SM_dry_month_count.py
==========================

Regenerates the "annual count of dry months" panel as a standalone figure,
styled to match Fig E (sm_monthly_series), Fig F (sm_annual_cycle), and
Fig G (sm_annual_trend) in /figures_methodology_ERA5.

Used as panel (d) of the composite soil-moisture results figure
(Figure 4.2 in the thesis Results chapter).

A dry month is defined here as a month whose basin-mean ERA5-Land
volumetric soil moisture (0-28 cm) is at or below the 20th-percentile
climatological threshold (p20) computed over the full 2015-2025 record.
The threshold value used is p20 = 0.054 m^3/m^3 (from summary_stats_sm.json).

Input
-----
- ERA5_SOIL/Mujib_ERA5Land_SM028_monthly_2015_01_to_2026_01.csv
- figures_methodology_ERA5/summary_stats_sm.json  (for p20 threshold)

Output
------
- figures_methodology_ERA5/fig_H2_sm_dry_month_count.png  (300 dpi)

Author : Nawwar Procheta, MSc Spatial Engineering, ITC, University of Twente
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

BASE_DIR = Path(
    r"C:\Users\proch\OneDrive - University of Twente\Desktop\MUJIB_DT\Cesium_71"
)

CSV_PATH = (
    BASE_DIR
    / "ERA5_SOIL"
    / "Mujib_ERA5Land_SM028_monthly_2015_01_to_2026_01.csv"
)
STATS_JSON = BASE_DIR / "figures_methodology_ERA5" / "summary_stats_sm.json"

OUT_DIR = BASE_DIR / "figures_methodology_ERA5"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PNG = OUT_DIR / "fig_H2_sm_dry_month_count.png"

# Reference windows
BASELINE_YEARS = {2015, 2016, 2017}
RECENT_YEARS = {2023, 2024, 2025}

# Period colours, matched to Figs E / F / G of the methodology folder
COLOUR_BASELINE = "#1f77b4"      # matplotlib tab:blue
COLOUR_RECENT = "#ff7f0e"        # matplotlib tab:orange
COLOUR_INTERMEDIATE = "#9e9e9e"  # neutral grey

# ---------------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------------

def load_monthly_sm() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df = df[(df["year"] >= 2015) & (df["year"] <= 2025)].copy()
    df = df[["date", "year", "sm_0_28_mean"]].reset_index(drop=True)
    return df


def load_p20_threshold() -> float:
    with open(STATS_JSON, "r", encoding="utf-8") as f:
        stats = json.load(f)
    return float(stats["p20_dry_threshold_m3m3"])


def compute_dry_month_count(df: pd.DataFrame, p20: float) -> pd.DataFrame:
    """Return a year-indexed dataframe with the count of dry months per year."""
    df = df.copy()
    df["is_dry"] = (df["sm_0_28_mean"] <= p20).astype(int)
    yearly = (
        df.groupby("year", as_index=False)["is_dry"]
        .sum()
        .rename(columns={"is_dry": "dry_months"})
    )
    years = pd.DataFrame({"year": np.arange(2015, 2026)})
    yearly = years.merge(yearly, on="year", how="left").fillna({"dry_months": 0})
    yearly["dry_months"] = yearly["dry_months"].astype(int)
    return yearly


# ---------------------------------------------------------------------------
# PLOT
# ---------------------------------------------------------------------------

def classify_year(year: int) -> str:
    if year in BASELINE_YEARS:
        return "baseline"
    if year in RECENT_YEARS:
        return "recent"
    return "intermediate"


def plot_dry_month_count(yearly: pd.DataFrame, p20: float) -> None:
    # Match Figs E/F/G typography: matplotlib defaults are DejaVu Sans 10 pt;
    # the existing figures look closer to 11 pt for axis labels, 12-13 pt for
    # the title, and 10 pt for tick labels. Mirror that here.
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
        }
    )

    colours = [
        COLOUR_BASELINE if classify_year(y) == "baseline"
        else COLOUR_RECENT if classify_year(y) == "recent"
        else COLOUR_INTERMEDIATE
        for y in yearly["year"]
    ]

    # Figure size chosen to match the aspect ratio of fig_G (~ 7.8 x 4.0 in
    # at 300 dpi -> 2348 x 1210 px).
    fig, ax = plt.subplots(figsize=(7.8, 4.0))

    bars = ax.bar(
        yearly["year"].astype(int),
        yearly["dry_months"],
        color=colours,
        edgecolor="black",
        linewidth=0.6,
        zorder=3,
    )

    # Value annotations on top of bars
    ymax = max(int(yearly["dry_months"].max()), 1)
    for rect, val in zip(bars, yearly["dry_months"]):
        ax.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height() + ymax * 0.03,
            f"{int(val)}",
            ha="center", va="bottom", fontsize=9, color="black",
        )

    # Axes
    ax.set_title(
        f"Annual count of dry months (p$_{{20}}$ = {p20:.3f} m$^{{3}}$ m$^{{-3}}$)",
        pad=8, fontweight="bold",
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of dry months (SM ≤ p$_{20}$)")
    ax.set_xticks(yearly["year"].astype(int))
    ax.set_xticklabels(yearly["year"].astype(int), rotation=0)

    # Y axis: integer ticks, headroom for annotations
    ax.set_ylim(0, ymax + max(1.5, ymax * 0.25))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Horizontal gridlines only, light grey, behind bars
    ax.yaxis.grid(True, linestyle=":", linewidth=0.5, color="#bbbbbb", zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    # Legend (same labels and order as Figs G and H)
    from matplotlib.patches import Patch

    handles = [
        Patch(facecolor=COLOUR_BASELINE, edgecolor="black",
              linewidth=0.6, label="Baseline year"),
        Patch(facecolor=COLOUR_RECENT, edgecolor="black",
              linewidth=0.6, label="Recent year"),
        Patch(facecolor=COLOUR_INTERMEDIATE, edgecolor="black",
              linewidth=0.6, label="Intermediate year"),
    ]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        ncol=3,
        frameon=False,
    )

    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] Figure written to: {OUT_PNG}")


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    for required in (CSV_PATH, STATS_JSON):
        if not required.exists():
            raise FileNotFoundError(f"Missing input: {required}")
    df = load_monthly_sm()
    p20 = load_p20_threshold()
    yearly = compute_dry_month_count(df, p20)
    print("Annual dry-month count:")
    print(yearly.to_string(index=False))
    plot_dry_month_count(yearly, p20)
