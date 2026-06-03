"""
clip_NDVI_recent_to_basin.py
============================

Clips the recent (2023-2025) Sentinel-2 NDVI raster to the official Mujib
Basin boundary and writes a new, basin-restricted GeoTIFF suitable for
downstream analysis in QGIS.

Operation
---------
1. Read the basin polygon (basin_OFFICIAL.geojson, EPSG:4326) and reproject
   it to the raster CRS (EPSG:32636, UTM 36N) so the geometric mask aligns
   with the raster grid.
2. Apply a geometry mask with crop=True, which both nulls pixels outside
   the polygon and trims the output extent to the polygon's bounding box.
3. Preserve NoData (-9999) and write a tiled, LZW-compressed GeoTIFF.

Input
-----
- NDVI_PROCESSED/Aligned_S2_Recent_NDVI_2023_2025.tif   (EPSG:32636, 10 m)
- basin_OFFICIAL.geojson                                (EPSG:4326)

Output
------
- NDVI_PROCESSED/Aligned_S2_Recent_NDVI_2023_2025_basin_clip.tif
  (EPSG:32636, 10 m, NoData = -9999, LZW-compressed, tiled)

Notes
-----
- The basin vector is reprojected on the fly; the source GeoJSON is not
  modified.
- crop=True trims the output to the polygon bounding box. To retain the
  original raster extent (with pixels outside the basin set to NoData)
  set CROP_TO_BASIN = False below.
- all_touched=False is the conservative default: a pixel is included only
  when its centre lies inside the polygon. Set ALL_TOUCHED = True to
  include any pixel that intersects the polygon edge.

Reproducibility
---------------
- Deterministic; no random operations.
- Tested with rasterio 1.3.x and geopandas 0.14.x.

Author : Nawwar Procheta, MSc Spatial Engineering, ITC, University of Twente
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.mask import mask as rio_mask

# ---------------------------------------------------------------------------
# 1. CONFIGURATION
# ---------------------------------------------------------------------------

BASE_DIR = Path(
    r"C:\Users\proch\OneDrive - University of Twente\Desktop\MUJIB_DT\Cesium_71"
)

NDVI_RECENT_TIF = (
    BASE_DIR / "NDVI_PROCESSED" / "Aligned_S2_Recent_NDVI_2023_2025.tif"
)
BASIN_VECTOR = BASE_DIR / "basin_OFFICIAL.geojson"

OUT_TIF = (
    BASE_DIR
    / "NDVI_PROCESSED"
    / "Aligned_S2_Recent_NDVI_2023_2025_basin_clip.tif"
)

NODATA_VALUE = -9999.0
CROP_TO_BASIN = True       # True: trim extent. False: keep original extent.
ALL_TOUCHED = False        # True: include edge-intersecting pixels.

# ---------------------------------------------------------------------------
# 2. CLIP FUNCTION
# ---------------------------------------------------------------------------

def clip_raster_to_polygon(
    raster_path: Path,
    polygon_path: Path,
    output_path: Path,
    nodata: float = NODATA_VALUE,
    crop: bool = CROP_TO_BASIN,
    all_touched: bool = ALL_TOUCHED,
) -> None:
    """Clip a raster by a polygon vector and write a new GeoTIFF."""

    if not raster_path.exists():
        raise FileNotFoundError(f"Raster not found: {raster_path}")
    if not polygon_path.exists():
        raise FileNotFoundError(f"Polygon not found: {polygon_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # --- Read polygon and align CRS to the raster ---
    gdf = gpd.read_file(polygon_path)
    if gdf.crs is None:
        gdf = gdf.set_crs(4326)

    with rasterio.open(raster_path) as src:
        if gdf.crs != src.crs:
            gdf = gdf.to_crs(src.crs)

        # Dissolve in case the basin is delivered as multiple features.
        # union_all() was introduced in geopandas 0.14; fall back for older.
        try:
            dissolved = gdf.union_all()
        except AttributeError:
            dissolved = gdf.unary_union
        geometries = [dissolved]

        # --- Apply mask ---
        clipped, transform = rio_mask(
            src,
            geometries,
            crop=crop,
            all_touched=all_touched,
            nodata=nodata,
            filled=True,
        )

        # --- Build output profile ---
        profile = src.profile.copy()
        profile.update(
            driver="GTiff",
            height=clipped.shape[1],
            width=clipped.shape[2],
            transform=transform,
            nodata=nodata,
            compress="LZW",
            predictor=3,           # float-optimised LZW predictor
            tiled=True,
            blockxsize=256,
            blockysize=256,
            BIGTIFF="IF_SAFER",
        )

        # --- Write ---
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(clipped)
            dst.update_tags(
                source_raster=raster_path.name,
                clip_polygon=polygon_path.name,
                nodata_value=str(nodata),
                crop_to_polygon=str(crop),
                all_touched=str(all_touched),
                processing_step=(
                    "Clipped to Mujib Basin boundary "
                    "(basin_OFFICIAL.geojson, reprojected to EPSG:32636)."
                ),
            )

    # --- Quick sanity report ---
    with rasterio.open(output_path) as out:
        arr = out.read(1, masked=True)
        valid = int(arr.count())
        total = int(arr.size)
        pct = 100.0 * valid / total if total else 0.0
        print("[OK] Clip written:")
        print(f"  Path     : {output_path}")
        print(f"  CRS      : {out.crs}")
        print(f"  Size     : {out.width} x {out.height} px")
        print(f"  Bounds   : {out.bounds}")
        print(f"  NoData   : {out.nodata}")
        print(f"  Valid px : {valid:,} / {total:,} ({pct:.1f}%)")
        if valid > 0:
            print(
                f"  NDVI min/mean/max : "
                f"{float(arr.min()):.3f} / "
                f"{float(arr.mean()):.3f} / "
                f"{float(arr.max()):.3f}"
            )


# ---------------------------------------------------------------------------
# 3. ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clip_raster_to_polygon(
        raster_path=NDVI_RECENT_TIF,
        polygon_path=BASIN_VECTOR,
        output_path=OUT_TIF,
    )
