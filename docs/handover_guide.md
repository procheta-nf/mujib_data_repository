# Handover Guide: Mujib Basin Digital Twin Framework

This document provides instructions for running, maintaining, and extending the Mujib Basin Digital Twin prototype. It is intended for ICARDA collaborators, thesis supervisors, and any future researcher continuing this work.

## 1. System overview

The framework has two components hosted in separate repositories:

| Component | Repository | Purpose |
|-----------|-----------|---------|
| Data repository | [procheta-nf/mujib_data_repository](https://github.com/procheta-nf/mujib_data_repository) | Processing notebooks, runtime data, validation outputs |
| Dashboard | [procheta-nf/mujib-dt-dashboard](https://github.com/procheta-nf/mujib-dt-dashboard) | CesiumJS 3D decision-support interface |

The dashboard reads files from `runtime-data/` at load time. There is no backend server or database. All data is pre-computed and served as static JSON, GeoJSON, CSV, and PNG files.

## 2. Running the dashboard locally

Prerequisites: a web browser and a local HTTP server (e.g., VS Code Live Server, Python `http.server`, or Node `http-server`).

Steps:

1. Clone the dashboard repository:
   ```
   git clone https://github.com/procheta-nf/mujib-dt-dashboard.git
   ```

2. Clone the data repository into the same parent folder:
   ```
   git clone https://github.com/procheta-nf/mujib_data_repository.git
   ```

3. Copy the `runtime-data/` contents into the dashboard folder structure. The dashboard expects files at specific relative paths (see the path constants at the top of `Working_71.html`):
   - `basin_OFFICIAL.geojson` in the root
   - `ERA5_SOIL/` for soil moisture files
   - `NDVI_CESIUM_PREVIEW_4326/` for NDVI PNGs
   - `Suitability/SUITABILITY_CESIUM_4326/` for suitability PNGs
   - `planner/` for sub-basin profiles
   - Scenario and vector files in the root

4. Start a local HTTP server from the dashboard folder:
   ```
   cd mujib-digital-twin
   python -m http.server 8080
   ```

5. Open `http://localhost:8080/Working_71.html` in your browser.

Note: The dashboard requires a Cesium Ion access token for 3D terrain and imagery. The token is embedded in the HTML file. If it expires, register at https://ion.cesium.com and replace the token value.

## 3. Data pipeline overview

The data flows through 8 processing stages (one notebook each):

```
output.sub (raw SWAT) --> [NB01] --> Parquet
ERA5 (via GEE)        --> [NB02] --> Precipitation JSON
ERA5-Land (via GEE)   --> [NB03] --> Soil moisture CSV/JSON
Sentinel-2 (via GEE)  --> [NB04] --> NDVI PNGs
ICARDA rasters        --> [NB05] --> Suitability PNGs
Parquet + multipliers --> [NB06] --> Scenario JSON
All layers            --> [NB07] --> Planner profiles + screening map
All outputs           --> [NB08] --> Validation tables + figures
```

Notebooks 02, 03, and 04 require Google Earth Engine authentication. All others run locally.

## 4. How to update each data layer

### 4.1 SWAT outputs (if a new model run becomes available)

1. Place the new `output.sub` file in `swat-prepared/raw/`.
2. Run notebook 01 to parse and export as Parquet.
3. Run notebook 06 to rebuild the scenario JSON with the new baseline.
4. Run notebook 07 to re-enrich the planner profiles.
5. Run notebook 08 to regenerate validation outputs.
6. Copy updated files from `runtime-data/` to the dashboard folder.

### 4.2 ERA5 precipitation

1. Run notebook 02 with updated date range in the GEE extraction cell.
2. The output `era5_precip_monthly_ALL429_compact.json` replaces the existing file in `runtime-data/era5/`.

### 4.3 ERA5-Land soil moisture

1. Run notebook 03 with updated date range.
2. Replace `soil_moisture_simple.csv` and `soil_moisture_summary_Mujib.json` in `runtime-data/era5/`.

### 4.4 Sentinel-2 NDVI

1. Run notebook 04 with updated baseline/recent period definitions.
2. Replace the 6 PNG files and `s2_bounds_scales.json` in `runtime-data/ndvi/`.

### 4.5 Suitability rasters

1. If new suitability rasters become available from ICARDA, place the raw TIFs in `runtime-data/suitability/raw/`.
2. Run notebook 05 to clip, threshold, and export dashboard PNGs.
3. Replace files in `runtime-data/suitability/`.

### 4.6 Scenario engine

1. If intervention multipliers change (new field data), update the multiplier values in notebook 06.
2. If CMIP6 projections are revised, update the proxy delta-P and delta-T values.
3. Re-run notebook 06 to regenerate `scenarios_USED_BY_CESIUM_FINAL_71_CMIP6_PROXY.json`.

## 5. Folder-to-dashboard path mapping

The dashboard HTML references files using relative paths. The mapping between the data repository structure and the dashboard's expected paths is:

| Data repo path | Dashboard expected path |
|----------------|----------------------|
| `runtime-data/boundaries/basin_OFFICIAL.geojson` | `basin_OFFICIAL.geojson` |
| `runtime-data/boundaries/subbasins_FULL429_with_runoff_sed_proxy.geojson` | `subbasins_FULL429_with_runoff_sed_proxy.geojson` |
| `runtime-data/era5/era5_precip_monthly_ALL429_compact.json` | `era5_precip_monthly_ALL429_compact.json` |
| `runtime-data/era5/soil_moisture_simple.csv` | `ERA5_SOIL/soil_moisture_simple.csv` |
| `runtime-data/era5/soil_moisture_summary_Mujib.json` | `ERA5_SOIL/soil_moisture_summary_Mujib.json` |
| `runtime-data/ndvi/*.png` | `NDVI_CESIUM_PREVIEW_4326/*.png` |
| `runtime-data/suitability/*.png` | `Suitability/SUITABILITY_CESIUM_4326/*.png` |
| `runtime-data/scenarios/*.json` | Root folder |
| `runtime-data/planner/*` | `planner/*` |
| `runtime-data/vectors/*` | Root folder |

## 6. Known limitations

1. The dashboard is a prototype, not an operational system. There is no backend, no database, no automated data refresh.
2. Percolation multipliers (+8%, +10%, +15%) are exploratory estimates, not field-derived values. They should be replaced when field measurements become available.
3. CMIP6 proxy cases use single delta-P and delta-T values from Al-Salal et al. (2024). They are near-term approximations, not full downscaled projections.
4. The suitability rasters from Haddad et al. (2024) are at approximately 1 km resolution. Sub-basin-level suitability percentages are area-weighted means and should not be interpreted at pixel level.
5. Sentinel-2 NDVI composites use cloud-masked median composites. Individual pixel values in persistently cloudy areas may be unreliable.
6. The 429 planning sub-basins do not align 1:1 with the 71 SWAT sub-basins. SWAT values are spatially joined using centroid-in-polygon assignment, which introduces approximation at sub-basin boundaries.
7. The ERA5 precipitation data covers 411 of 429 sub-basins (18 sub-basins fall outside ERA5 grid coverage at the basin margins).
8. No formal stakeholder evaluation was conducted. The dashboard was assessed through preliminary expert sense-checking only.

## 7. Future development priorities

If this framework is continued, the following additions would strengthen it most:

1. Connect to a backend database (e.g., PostGIS) for dynamic data queries instead of static file loading.
2. Add an API layer (e.g., Flask/FastAPI) to enable on-demand scenario computation rather than pre-computed JSON.
3. Integrate near-real-time satellite data feeds (Sentinel-2, ERA5T) for automated NDVI and climate updates.
4. Replace exploratory percolation multipliers with field-calibrated values from ongoing ICARDA monitoring.
5. Add uncertainty visualization (confidence bands, sensitivity indicators) to the dashboard panels.
6. Conduct a structured stakeholder evaluation with ICARDA field staff and Jordanian water planners.

## 8. Contact

- Nawwar Procheta (developer): procheta@gmail.com
- Dr. Augusto Getirana (first supervisor), ITC, University of Twente
- Dr. Javier Marcos Garcimartin (second supervisor), ITC, University of Twente

## 9. File inventory

As of June 2026, the data repository contains:

- 8 Jupyter notebooks (data pipeline)
- 4 Python figure-generation scripts
- 102+ data files across runtime-data/, swat-prepared/, and validation/
- README, LICENSE, data dictionary, requirements.txt, and this handover guide

Total repository size: approximately 102 MB. No file exceeds 50 MB. The largest file is the LoD1 building footprints GeoJSON at 32 MB.
