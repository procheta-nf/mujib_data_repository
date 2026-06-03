# Mujib Basin Digital Twin: Data Repository

Data processing, scenario analysis, and validation notebooks for the MSc thesis:

**A Scenario-Based Geospatial-Hydrological Digital Twin Framework for Watershed Restoration Analysis in the Mujib Basin, Jordan**

Nawwar Procheta (s3442462), MSc Spatial Engineering, ITC, University of Twente, 2026.

Supervisors: Dr. Augusto Getirana (first), Dr. Javier Marcos Garcimartin (second).

---

## Repository structure

```
mujib_data_repository/
├── notebooks/                  # 8 analysis and processing notebooks
│   ├── 01_swat_output_preparation.ipynb
│   ├── 02_era5_precipitation.ipynb
│   ├── 03_era5land_soil_moisture.ipynb
│   ├── 04_ndvi_processing.ipynb
│   ├── 05_suitability_processing.ipynb
│   ├── 06_scenario_engine.ipynb
│   ├── 07_planner_enrichment.ipynb
│   └── 08_validation_and_verification.ipynb
├── runtime-data/               # Dashboard-ready files consumed by CesiumJS
│   ├── boundaries/             # Basin and sub-basin GeoJSON
│   ├── era5/                   # ERA5 precipitation, ERA5-Land soil moisture (CSV + rasters)
│   ├── ndvi/                   # Sentinel-2 NDVI composites (baseline, recent, delta)
│   ├── planner/                # Sub-basin profiles, master enrichment, screening map
│   ├── scenarios/              # Scenario JSON (71 SWAT + CMIP6 proxy) and interventions
│   ├── suitability/            # Marab and Vallerani suitability PNGs, raw TIFs, clipped TIFs
│   └── vectors/                # Dams, flood stations, rivers, LoD1 building footprints
├── swat-prepared/              # Cleaned SWAT outputs as Parquet (sub-basin, HRU, reach)
├── validation/                 # V&V outputs
│   ├── figures/                # Baseline reproduction scatter, Monte Carlo, soil moisture
│   ├── tables/                 # CSV tables for all 8 V&V checks
│   ├── monte_carlo/            # Monte Carlo simulation outputs and variance decomposition
│   ├── ndvi_precip_validation/ # NDVI-precipitation cross-validation scatter plots
│   ├── soil_moisture_validation/ # Soil moisture baseline vs. recent analysis
│   ├── suitability_benchmarking/ # Suitability threshold benchmarking outputs
│   ├── SWAT_charts/            # Exploratory SWAT-related charts
│   └── validation_summary_report.md
├── docs/                       # Data dictionary (see below)
├── .gitignore
├── requirements.txt
└── README.md
```

## Notebooks

Each notebook corresponds to one processing stage in the Digital Twin data pipeline. They are numbered in execution order.

| # | Notebook | Purpose | Key outputs |
|---|----------|---------|-------------|
| 01 | SWAT output preparation | Parse fixed-width output.sub from ArcSWAT, QC, export to Parquet | `swat-prepared/output_sub_FULL.parquet` |
| 02 | ERA5 precipitation | Extract ERA5 monthly precipitation, zonal statistics to 429 sub-basins | `runtime-data/era5/era5_precip_monthly_ALL429_compact.json` |
| 03 | ERA5-Land soil moisture | GEE extraction, basin-mean soil moisture, baseline vs. recent comparison | `runtime-data/era5/soil_moisture_*.csv/json` |
| 04 | NDVI processing | GEE Sentinel-2 NDVI extraction, local raster preparation, change detection | `runtime-data/ndvi/s2_*.png` |
| 05 | Suitability processing | Clip ICARDA Haddad et al. (2024) rasters, threshold at 80%, export PNGs | `runtime-data/suitability/*.png` |
| 06 | Scenario engine | Ridge regression emulator, perturbation grid, CMIP6 proxy cases, JSON assembly | `runtime-data/scenarios/*.json` |
| 07 | Planner enrichment | Sub-basin indicator profiles, SWAT merge to 429 planning units, screening map | `runtime-data/planner/*.json/geojson` |
| 08 | Validation and verification | 8 V&V checks: baseline reproduction, monotonicity, multiplier coherence, ERA5, NDVI, soil moisture, suitability benchmarking, Monte Carlo variance decomposition | `validation/tables/*.csv`, `validation/figures/*.png` |

## Data sources

| Dataset | Source | Access |
|---------|--------|--------|
| SWAT sub-basin outputs (SURQ, SYLD, PERC, ET, WYLD) | ArcSWAT model run, ICARDA collaboration (2024) | Restricted |
| ERA5 monthly precipitation | ECMWF via Google Earth Engine | Open |
| ERA5-Land soil moisture | ECMWF via Google Earth Engine | Open |
| Sentinel-2 NDVI | Copernicus via Google Earth Engine | Open |
| Marab and Vallerani suitability | Haddad et al. (2024), ICARDA | Restricted |
| Basin and sub-basin boundaries | Ministry of Water and Irrigation, Jordan | Restricted |
| Dam locations | Ministry of Water and Irrigation, Jordan | Restricted |
| LoD1 building footprints | TUM SO2Sat Global LoD1 via WFS | Open |
| DEM (ALOS 30 m) | Alaska Satellite Facility DAAC | Open |

## Key technical parameters

- Dual sub-basin architecture: 71 SWAT sub-basins + 429 planning sub-basins
- Ridge regression emulator: Tikhonov regularisation, alpha = 1e-6
- Sediment model: log-log relationship log(SURQ) to log(SYLD)
- Intervention multipliers (from Haddad et al., 2022 RHEM simulations):
  - Marab: -10% runoff
  - Vallerani: -19% runoff
  - Combined: -27% runoff
- Percolation multipliers (exploratory, not field-derived): +8%, +10%, +15%
- CMIP6 proxy cases: SSP2-4.5 (delta P approx. -3%, delta T approx. +1.4 C), SSP5-8.5 (delta P approx. +2%, delta T approx. +1.6 C)
- Baseline reproduction: R-squared = 0.998 (runoff), 0.966 (sediment), 0.999 (recharge)
- Monotonicity: 140/140 checks passed

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Notebooks 02, 03, and 04 require Google Earth Engine authentication (`earthengine-api`, `geemap`). Other notebooks run locally with the data files already present in this repository.

## Dashboard

The CesiumJS decision-support dashboard that consumes the `runtime-data/` files is hosted at:

https://nawwarprocheta.github.io/mujib-digital-twin/

Source code: https://github.com/NawwarProcheta/mujib-digital-twin

## License

See LICENSE file. Restricted datasets (SWAT outputs, suitability rasters, basin boundaries) are shared under ICARDA research collaboration terms and may not be redistributed without permission.

## Citation

If you use this repository, please cite the thesis:

Procheta, N. (2026). *A Scenario-Based Geospatial-Hydrological Digital Twin Framework for Watershed Restoration Analysis in the Mujib Basin, Jordan* [MSc thesis, University of Twente, Faculty ITC].
