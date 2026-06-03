"""
plot_NDVI_baseline_vs_recent.py
================================

Generates a publication-quality two-panel NDVI map (Baseline vs Recent)
for the Mujib Basin, Jordan. Used in the methodology chapter of the MSc
thesis: scenario-based geospatial-hydrological Digital Twin framework.

Inputs
------
1. Aligned_S2_Clipped_Baseline_NDVI_2015_2017_FIXED_NODATA.tif
2. Aligned_S2_Recent_NDVI_2023_2025.tif
3. basin_OFFICIAL.geojson (basin outline overlay)

Both NDVI rasters are derived from cloud-screened, monthly-median
Sentinel-2 surface-reflectance composites in Google Earth Engine, then
clipped and aligned to a common 10 m grid in EPSG:32636 (UTM 36N).
NoData = -9999.

Classification
--------------
Discrete NDVI classes follow conventions for arid- and semi-arid
rangeland NDVI mapping (e.g., Pettorelli et al., 2005; Rouse et al.,
1974). The legend is rendered as a QGIS-style classified legend with
seven thematic classes calibrated to the dynamic range of the Mujib
Basin (predominantly bare and sparsely vegetated).

Output
------
NDVI_Baseline_vs_Recent_Methodology.png  (300 dpi, A4 landscape)
NDVI_Baseline_vs_Recent_Methodology.pdf  (vector copy)

Reproducibility
---------------
- Deterministic: no random seeds, no stochastic operations.
- All paths, class breaks, colours, and CRS are explicit constants.
- Tested with: rasterio 1.3.x, geopandas 0.14.x, matplotlib 3.8.x.

Author : Nawwar Procheta, MSc Spatial Engineering, ITC, University of Twente
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.ticker import FuncFormatter

import rasterio
from rasterio.plot import plotting_extent
import geopandas as gpd

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ---------------------------------------------------------------------------
# 1. CONFIGURATION
# ---------------------------------------------------------------------------

BASE_DIR = Path(
    r"C:\Users\proch\OneDrive - University of Twente\Desktop\MUJIB_DT\Cesium_71"
)

NDVI_BASELINE_TIF = (
    BASE_DIR
    / "NDVI_PROCESSED"
    / "Aligned_S2_Clipped_Baseline_NDVI_2015_2017_FIXED_NODATA.tif"
)
NDVI_RECENT_TIF = (
    BASE_DIR / "NDVI_PROCESSED" / "Aligned_S2_Recent_NDVI_2023_2025.tif"
)
BASIN_VECTOR = BASE_DIR / "basin_OFFICIAL.geojson"

OUT_DIR = BASE_DIR / "figures_methodology_NDVI"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PNG = OUT_DIR / "NDVI_Baseline_vs_Recent_Methodology.png"
OUT_PDF = OUT_DIR / "NDVI_Baseline_vs_Recent_Methodology.pdf"

NODATA_SENTINEL = -9999.0
VALID_NDVI_RANGE = (-1.0, 1.0)

LABEL_BASELINE = "Baseline NDVI (2015–2017)"
LABEL_RECENT = "Recent NDVI (2023–2025)"

# ---------------------------------------------------------------------------
# 2. CLASSIFICATION SCHEME (QGIS-style discrete classes)
# ---------------------------------------------------------------------------
# Class breaks are chosen for arid and semi-arid rangelands, where most
# pixels lie between 0.05 and 0.25. Seven classes provide resolvable
# contrast without over-fragmenting the legend.

NDVI_BREAKS = [-1.0, 0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 1.0]

NDVI_CLASS_LABELS = [
    "≤ 0.00  Non-vegetation (water, rock, built-up)",
    "0.00 – 0.10  Bare soil / very sparse",
    "0.10 – 0.20  Sparse vegetation",
    "0.20 – 0.30  Low vegetation",
    "0.30 – 0.40  Moderate vegetation",
    "0.40 – 0.50  Dense vegetation",
    "> 0.50  Very dense vegetation",
]

# Colour-blind-safe vegetation ramp (tan to green), tuned for print.
NDVI_COLOURS = [
    "#cfcfcf",  # <= 0.00 - neutral grey (non-vegetated)
    "#d9c2a0",  # 0.00 - 0.10 - tan / bare soil
    "#e7e3a2",  # 0.10 - 0.20 - pale yellow-green
    "#c4d97e",  # 0.20 - 0.30 - yellow-green
    "#8ec46d",  # 0.30 - 0.40 - light green
    "#4ea15c",  # 0.40 - 0.50 - mid green
    "#1d6b3a",  # > 0.50 - dark green
]

assert len(NDVI_COLOURS) == len(NDVI_CLASS_LABELS) == len(NDVI_BREAKS) - 1

NDVI_CMAP = ListedColormap(NDVI_COLOURS, name="ndvi_qgis_classified")
NDVI_CMAP.set_bad(color="white", alpha=0.0)
NDVI_NORM = BoundaryNorm(NDVI_BREAKS, NDVI_CMAP.N, clip=False)

# ---------------------------------------------------------------------------
# 3. I/O HELPERS
# ---------------------------------------------------------------------------

def read_ndvi_raster(path: Path):
    """Read NDVI raster, return masked array, plotting extent and CRS."""
    with rasterio.open(path) as src:
        arr = src.read(1).astype("float32")
        crs = src.crs
        extent = plotting_extent(src)
    nodata_mask = (
        (arr == NODATA_SENTINEL)
        | np.isnan(arr)
        | (arr < VALID_NDVI_RANGE[0])
        | (arr > VALID_NDVI_RANGE[1])
    )
    return np.ma.masked_array(arr, mask=nodata_mask), extent, crs


def load_basin_outline(target_crs):
    """Load basin polygon and reproject to raster CRS for overlay."""
    gdf = gpd.read_file(BASIN_VECTOR)
    if gdf.crs is None:
        gdf = gdf.set_crs(4326)
    return gdf.to_crs(target_crs)

# ---------------------------------------------------------------------------
# 4. CARTOGRAPHIC ELEMENTS
# ---------------------------------------------------------------------------

def add_scale_bar(ax, length_km=10, location=(0.06, 0.05),
                  linewidth=3, fontsize=8):
    """Draw a horizontal scale bar in projected metres (UTM)."""
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    bar_len_m = length_km * 1000
    x_start = x0 + (x1 - x0) * location[0]
    y_start = y0 + (y1 - y0) * location[1]
    ax.plot(
        [x_start, x_start + bar_len_m],
        [y_start, y_start],
        color="black", lw=linewidth, solid_capstyle="butt", zorder=5,
    )
    ax.text(
        x_start + bar_len_m / 2,
        y_start + (y1 - y0) * 0.012,
        f"{length_km} km",
        ha="center", va="bottom",
        fontsize=fontsize, color="black", zorder=5,
    )


def add_north_arrow(ax, location=(0.94, 0.92), size=0.06, fontsize=10):
    """Draw a minimal north arrow."""
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    cx = x0 + (x1 - x0) * location[0]
    cy = y0 + (y1 - y0) * location[1]
    arrow_h = (y1 - y0) * size
    ax.annotate(
        "N",
        xy=(cx, cy + arrow_h * 0.55),
        xytext=(cx, cy - arrow_h * 0.45),
        ha="center", va="center",
        fontsize=fontsize, fontweight="bold",
        arrowprops=dict(facecolor="black", edgecolor="black",
                        width=3.5, headwidth=10, headlength=10),
        zorder=5,
    )


def km_formatter(value, _pos):
    """Format UTM metres as kilometres for cleaner axis labels."""
    return f"{value/1000:.0f}"

# ---------------------------------------------------------------------------
# 5. PLOTTING
# ---------------------------------------------------------------------------

def plot_panel(ax, ndvi, extent, basin_gdf, title):
    """Render one classified NDVI panel with basin outline."""
    ax.imshow(
        ndvi,
        extent=extent,
        cmap=NDVI_CMAP,
        norm=NDVI_NORM,
        interpolation="nearest",
        origin="upper",
    )
    basin_gdf.boundary.plot(
        ax=ax, edgecolor="black", linewidth=0.9, zorder=4,
    )

    minx, miny, maxx, maxy = basin_gdf.total_bounds
    pad_x = (maxx - minx) * 0.02
    pad_y = (maxy - miny) * 0.02
    ax.set_xlim(minx - pad_x, maxx + pad_x)
    ax.set_ylim(miny - pad_y, maxy + pad_y)

    ax.set_title(title, fontsize=11, pad=8, fontweight="bold")
    ax.set_xlabel("Easting (km, UTM 36N)", fontsize=9)
    ax.set_ylabel("Northing (km, UTM 36N)", fontsize=9)
    ax.xaxis.set_major_formatter(FuncFormatter(km_formatter))
    ax.yaxis.set_major_formatter(FuncFormatter(km_formatter))
    ax.tick_params(axis="both", labelsize=8)
    ax.set_aspect("equal")
    ax.grid(True, linestyle=":", linewidth=0.4, color="grey", alpha=0.6)
    for spine in ax.spines.values():
        spine.set_linewidth(0.7)

    add_scale_bar(ax, length_km=10)
    add_north_arrow(ax)


def build_figure():
    ndvi_b, ext_b, crs_b = read_ndvi_raster(NDVI_BASELINE_TIF)
    ndvi_r, ext_r, crs_r = read_ndvi_raster(NDVI_RECENT_TIF)
    if crs_b != crs_r:
        raise ValueError(
            f"CRS mismatch between baseline ({crs_b}) and recent ({crs_r}). "
            "Re-align rasters before plotting."
        )
    basin = load_basin_outline(crs_b)

    fig, axes = plt.subplots(1, 2, figsize=(11.7, 6.8))

    plot_panel(axes[0], ndvi_b, ext_b, basin, LABEL_BASELINE)
    plot_panel(axes[1], ndvi_r, ext_r, basin, LABEL_RECENT)

    legend_handles = [
        mpatches.Patch(facecolor=c, edgecolor="black", linewidth=0.4, label=lbl)
        for c, lbl in zip(NDVI_COLOURS, NDVI_CLASS_LABELS)
    ]
    legend_handles.append(
        mpatches.Patch(facecolor="none", edgecolor="black",
                       linewidth=0.9, label="Mujib Basin boundary")
    )
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.075),
        ncol=4,
        frameon=True,
        fontsize=8.2,
        title="NDVI classes (Sentinel-2, 10 m)",
        title_fontsize=9,
    )

    fig.suptitle(
        "Sentinel-2 NDVI condition over the Mujib Basin: "
        "baseline (2015–2017) and recent (2023–2025) periods",
        fontsize=12, fontweight="bold", y=0.985,
    )

    metadata_line1 = (
        "Source: Sentinel-2 Level-2A surface reflectance, monthly median "
        "composites (Google Earth Engine, cloud probability < 20%)."
    )
    metadata_line2 = (
        "Projection: WGS 84 / UTM 36N (EPSG:32636).   "
        "Spatial resolution: 10 m.   "
        "Classification: equal interval (Δ = 0.10) within the [0, 0.5] range."
    )
    fig.text(0.5, 0.045, metadata_line1, ha="center", va="bottom",
             fontsize=7.5, style="italic", color="#333333")
    fig.text(0.5, 0.020, metadata_line2, ha="center", va="bottom",
             fontsize=7.5, style="italic", color="#333333")

    plt.subplots_adjust(left=0.07, right=0.97, top=0.91,
                        bottom=0.22, wspace=0.18)

    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT_PDF, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] Figure written to:\n  {OUT_PNG}\n  {OUT_PDF}")


# ---------------------------------------------------------------------------
# 6. ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    for required in (NDVI_BASELINE_TIF, NDVI_RECENT_TIF, BASIN_VECTOR):
        if not required.exists():
            raise FileNotFoundError(f"Missing input: {required}")
    build_figure()
