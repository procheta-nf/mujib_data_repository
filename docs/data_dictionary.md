# Data Dictionary

This document describes the key data files produced and consumed by the Mujib Basin Digital Twin framework.

## 1. SWAT prepared outputs (`swat-prepared/`)

### output_sub_FULL.parquet

Cleaned and parsed SWAT output.sub file, covering 71 sub-basins from 1988 to 2020 (monthly).

| Column | Type | Unit | Description |
|--------|------|------|-------------|
| SUB | int | - | SWAT sub-basin ID (1 to 71) |
| YEAR | int | - | Calendar year |
| MON | int | - | Month (1 to 12) or annual summary |
| AREAkm2 | float | km2 | Sub-basin area |
| PRECIPmm | float | mm | Precipitation |
| SNOMELTmm | float | mm | Snowmelt |
| PETmm | float | mm | Potential evapotranspiration |
| ETmm | float | mm | Actual evapotranspiration |
| SW_INITmm | float | mm | Initial soil water content |
| SW_ENDmm | float | mm | Final soil water content |
| PERCmm | float | mm | Deep percolation (groundwater recharge proxy) |
| GW_Qmm | float | mm | Groundwater contribution to streamflow |
| DA_Qmm | float | mm | Deep aquifer contribution |
| SURQmm | float | mm | Surface runoff |
| GW_Q_Dmm | float | mm | Groundwater to deep aquifer |
| WYLDmm | float | mm | Water yield |
| DAILYCN | float | - | Daily curve number |
| TMP_AVdgC | float | deg C | Average temperature |
| TMP_MXdgC | float | deg C | Maximum temperature |
| TMP_MNdgC | float | deg C | Minimum temperature |
| SOL_TMPdgC | float | deg C | Soil temperature |
| SOLARmj_m2 | float | MJ/m2 | Solar radiation |
| SYLDt_ha | float | t/ha | Sediment yield |
| USLE | float | t/ha | USLE soil loss |
| N_APPkg_ha | float | kg/ha | Nitrogen applied |
| P_APPkg_ha | float | kg/ha | Phosphorus applied |
| NAUTOkg_ha | float | kg/ha | Auto-nitrogen |
| PAUTOkg_ha | float | kg/ha | Auto-phosphorus |
| NGRZkg_ha | float | kg/ha | Grazing nitrogen |
| PGRZkg_ha | float | kg/ha | Grazing phosphorus |
| NCFRTkg_ha | float | kg/ha | Continuous fertiliser nitrogen |
| PCFRTkg_ha | float | kg/ha | Continuous fertiliser phosphorus |
| NRAINkg_ha | float | kg/ha | Nitrogen in rainfall |
| NFIXkg_ha | float | kg/ha | Nitrogen fixation |
| F_MNkg_ha | float | kg/ha | Fresh mineral nitrogen |
| A_MNkg_ha | float | kg/ha | Active mineral nitrogen |
| A_SNkg_ha | float | kg/ha | Active stable nitrogen |
| F_MPkg_ha | float | kg/ha | Fresh mineral phosphorus |
| AO_LPkg_ha | float | kg/ha | Active organic labile phosphorus |
| L_APkg_ha | float | kg/ha | Labile active phosphorus |
| A_SPkg_ha | float | kg/ha | Active stable phosphorus |
| DNITkg_ha | float | kg/ha | Denitrification |
| NUPkg_ha | float | kg/ha | Nitrogen uptake |
| PUPkg_ha | float | kg/ha | Phosphorus uptake |
| ORGNkg_ha | float | kg/ha | Organic nitrogen in surface runoff |
| ORGPkg_ha | float | kg/ha | Organic phosphorus in surface runoff |
| SEDPkg_ha | float | kg/ha | Sediment-associated phosphorus |
| NSURQkg_ha | float | kg/ha | Nitrate in surface runoff |
| NLATQkg_ha | float | kg/ha | Nitrate in lateral flow |
| NO3Lkg_ha | float | kg/ha | Nitrate leached |
| NO3GWkg_ha | float | kg/ha | Nitrate in groundwater |
| SOLPkg_ha | float | kg/ha | Soluble phosphorus |
| P_GWkg_ha | float | kg/ha | Phosphorus in groundwater |
| W_STRS | float | - | Water stress days |
| TMP_STRS | float | - | Temperature stress days |
| N_STRS | float | - | Nitrogen stress days |
| P_STRS | float | - | Phosphorus stress days |
| BIOMt_ha | float | t/ha | Biomass |
| LAI | float | - | Leaf area index |
| YLDt_ha | float | t/ha | Crop yield |
| BACTPct | float | #/100ml | Persistent bacteria |
| BACTLPct | float | #/100ml | Less persistent bacteria |
| WTAB_CLIm | float | m | Water table climatology |
| WTAB_SOLm | float | m | Water table soil |
| SNO_HRUmm | float | mm | Snow water content |
| CMUPkg_ha | float | kg/ha | Metal uptake |
| CMTOTkg_ha | float | kg/ha | Total metal |
| QTILEmm | float | mm | Tile drain flow |
| TNO3kg_ha | float | kg/ha | Tile drain NO3 |
| LNO3kg_ha | float | kg/ha | Lateral NO3 |
| GW_Q_Dmmm | float | mm | Deep GW outflow |
| LATQGENmm | float | mm | Lateral flow generated |

### output_sub_FULL_FIXED2020.parquet

Same schema as above. Year 2020 rows have been QC-corrected (monthly values verified against annual totals).

## 2. Scenario data (`runtime-data/scenarios/`)

### scenarios_USED_BY_CESIUM_FINAL_71_CMIP6_PROXY.json

JSON object consumed by the CesiumJS dashboard. Structure:

```
{
  "Subbasin_1": {
    "baseline": { ... annual means ... },
    "whatifs": {
      "dP0_dT0": {
        "baseline": { "runoff": ..., "sediment": ..., "recharge": ... },
        "marab": { ... },
        "vallerani": { ... },
        "combined": { ... }
      },
      "dP-3_dT1": { ... },   // SSP2-4.5 proxy
      "dP2_dT2": { ... },    // SSP5-8.5 proxy
      ...
    }
  },
  "Subbasin_2": { ... },
  ...
}
```

Each scenario node contains annual mean values for three indicators: runoff (mm), sediment (t/ha), and recharge/percolation (mm).

### interventions.json

Metadata describing the four restoration scenarios and their multiplier assumptions.

## 3. ERA5 climate data (`runtime-data/era5/`)

### era5_precip_monthly_ALL429_compact.json

Monthly ERA5 precipitation aggregated to 429 planning sub-basins.

```
{
  "SUB_001": {
    "2007-01": 45.2,
    "2007-02": 38.1,
    ...
  },
  ...
}
```

Values in mm/month.

### soil_moisture_simple.csv

Basin-mean monthly soil moisture from ERA5-Land.

| Column | Type | Unit | Description |
|--------|------|------|-------------|
| date | string | YYYY-MM | Month |
| swvl1_mean | float | m3/m3 | Layer 1 volumetric soil moisture (0-7 cm) |
| swvl2_mean | float | m3/m3 | Layer 2 volumetric soil moisture (7-28 cm) |
| swvl3_mean | float | m3/m3 | Layer 3 volumetric soil moisture (28-100 cm) |
| swvl4_mean | float | m3/m3 | Layer 4 volumetric soil moisture (100-289 cm) |

Period: January 2015 to December 2025.

### soil_moisture_summary_Mujib.json

Summary statistics (baseline 2015-2017 vs. recent 2023-2025 means per layer).

## 4. NDVI data (`runtime-data/ndvi/`)

| File | Description |
|------|-------------|
| s2_baseline.png | Sentinel-2 NDVI composite, baseline period (2015-2017 median) |
| s2_baseline_color.png | Colour-mapped version of baseline NDVI |
| s2_recent.png | Sentinel-2 NDVI composite, recent period (2023-2025 median) |
| s2_recent_color.png | Colour-mapped version of recent NDVI |
| s2_delta.png | NDVI change (recent minus baseline) |
| s2_delta_color.png | Colour-mapped version of NDVI change |
| s2_bounds_scales.json | Geographic bounds and colour scale metadata for overlay alignment |

All PNGs are in EPSG:4326 and georeferenced via the bounds in the JSON metadata file.

## 5. Suitability layers (`runtime-data/suitability/`)

| File | Description |
|------|-------------|
| marab_suitability_color_4326.png | Marab-barley suitability (continuous, 0-100 scale) |
| marab_candidate_gt80_4326.png | Marab candidate areas (suitability > 80 threshold) |
| vallerani_suitability_color_4326.png | Vallerani-saltbush suitability (continuous, 0-100 scale) |
| vallerani_candidate_gt80_4326.png | Vallerani candidate areas (suitability > 80 threshold) |
| combined_candidate_gt80_4326.png | Union of Marab and Vallerani candidate areas |
| candidate_overlay_bounds_all_thresholds.json | Geographic bounds and overlay metadata |

Source: Haddad et al. (2024), AHP-based national-scale suitability mapping (ICARDA).

## 6. Planner sub-basins (`runtime-data/planner/`)

### subbasin_master_enriched_clean.json

Master file with per-sub-basin attributes used by the dashboard decision panel.

```
{
  "1": {
    "SUB": "1",
    "area_km2": 12.4,
    "ndvi_baseline": 0.18,
    "ndvi_recent": 0.21,
    "ndvi_delta": 0.03,
    "marab_pct": 45.2,
    "vallerani_pct": 62.1,
    "era5_precip_annual_mm": 185.3,
    "swat_runoff_mm": 12.5,
    "swat_sediment_t_ha": 3.2,
    "swat_percolation_mm": 8.1,
    ...
  },
  ...
}
```

### subbasin_indicator_profiles_clean.json

Indicator time series for each planning sub-basin (NDVI, precipitation, soil moisture).

### subbasin_locations_ALL429.json

Centroid coordinates for 429 planning sub-basins (used for label placement in CesiumJS).

### subbasin_screening_map.geojson

GeoJSON with screening attributes for rapid spatial filtering of candidate intervention areas.

## 7. Boundaries (`runtime-data/boundaries/`)

| File | Description |
|------|-------------|
| basin_OFFICIAL.geojson | Official Mujib Basin boundary polygon (MoWI, Jordan) |
| subbasins_FULL429_with_runoff_sed_proxy.geojson | 429 planning sub-basins with proxy runoff and sediment attributes |

## 8. Vectors (`runtime-data/vectors/`)

| File | Description |
|------|-------------|
| dams.geojson | Dam locations and attributes in the Mujib Basin |
| flood_stations.geojson | Streamflow and meteorological station locations |
| mujib_lod1_simplified_CLIPPED.geojson | LoD1 building footprints (TUM SO2Sat) clipped to basin extent |

## 9. Validation outputs (`validation/`)

### Tables (`validation/tables/`)

| File | V&V check |
|------|-----------|
| baseline_reproduction.csv | Check 1: Emulator vs. SWAT baseline comparison (R-squared, MAE, MAPE) |
| monotonicity_tests.csv | Check 2: 140 monotonicity tests (runoff decreases, percolation increases with intervention intensity) |
| intervention_multipliers_raw.csv | Check 3: Raw multiplier values per sub-basin per scenario |
| intervention_multiplier_summary.csv | Check 3: Summary statistics of multiplier coherence |
| era5_monthly_long.csv | Check 4: Full ERA5 monthly precipitation data for all 429 sub-basins |
| era5_monthly_counts.csv | Check 4: Record counts per sub-basin |
| era5_monthly_summary.csv | Check 4: Basin-wide precipitation statistics |
| era5_climate_summary.csv | Check 4: Climate summary table |
| ndvi_asset_check.csv | Check 5: NDVI file existence and metadata verification |
| suitability_benchmark_comparison.csv | Check 6: Suitability threshold benchmarking against Haddad et al. (2024) |
| spatial_integrity.csv | Check 7: Spatial alignment and CRS consistency |
| join_diagnostics.csv | Check 7: Join coverage diagnostics between SWAT and planning sub-basins |
| join_issue_examples.csv | Check 7: Examples of join mismatches |
| file_contract_audit.csv | Check 7: File contract audit (expected vs. actual runtime files) |
| dashboard_html_sniff_tests.csv | Check 7: HTML structure verification |
| source_to_screen_trace.csv | Check 7: Source-to-screen data traceability |
| expert_walkthrough_template.csv | Check 8: Expert walkthrough template for preliminary sense-checking |

### Figures (`validation/figures/`)

| File | Description |
|------|-------------|
| fig_baseline_reproduction_scatter.png / .pdf | Scatter plot of emulator vs. SWAT for runoff, sediment, recharge |
| fig_monte_carlo_variance_decomposition.png | Monte Carlo variance decomposition (multiplier vs. climate uncertainty) |
| fig_variance_decomposition_by_climate.png | Variance decomposition broken down by climate scenario |
| soil_baseline_vs_recent.png | ERA5-Land soil moisture baseline vs. recent comparison |

### NDVI-precipitation validation (`validation/ndvi_precip_validation/`)

| File | Description |
|------|-------------|
| fig_precip_vs_ndvi_baseline.png | Scatter: ERA5 precipitation vs. NDVI (baseline period) |
| fig_precip_vs_ndvi_recent.png | Scatter: ERA5 precipitation vs. NDVI (recent period) |
| fig_precip_vs_ndvi_delta.png | Scatter: precipitation change vs. NDVI change |
| ndvi_precip_input_table.csv | Input data table for the scatter analysis |
| ndvi_precip_metrics.csv | Correlation and regression metrics |

### Soil moisture validation (`validation/soil_moisture_validation/`)

| File | Description |
|------|-------------|
| fig_soil_moisture_baseline_recent_timeseries.png | Baseline vs. recent soil moisture time series |
| soil_moisture_summary.csv | Summary statistics for baseline and recent periods |

### Suitability benchmarking (`validation/suitability_benchmarking/`)

| File | Description |
|------|-------------|
| fig_suitability_benchmark_comparison.png | Comparison of computed vs. reported suitability statistics |
| hist_marab_mean_suitability.png | Histogram of Marab suitability scores across sub-basins |
| hist_vallerani_mean_suitability.png | Histogram of Vallerani suitability scores across sub-basins |
| suitability_benchmark_summary.csv | Benchmark comparison table |

### Monte Carlo analysis (`validation/monte_carlo/`)

| File | Description |
|------|-------------|
| fig_monte_carlo_present_climate.png | Monte Carlo results at present climate |
| fig_variance_decomposition_by_climate.png | Variance decomposition by climate scenario |
| monte_carlo_results.csv | Raw Monte Carlo simulation outputs |
| variance_decomposition_by_climate.csv | Variance partition table by indicator and climate case |

### SWAT exploratory charts (`validation/SWAT_charts/`)

| File | Description |
|------|-------------|
| 02_emulator_validation_scatter.png | Emulator validation scatter (early version) |
| 06_variance_decomposition.png | Variance decomposition (early version) |
| 08_soil_moisture_trend.png | Soil moisture trend plot |
| 09_suitability_distribution.png | Suitability score distribution |
| 10_ndvi_scatter.png | NDVI scatter plot |
| 11_tornado_scenarios.png | Tornado diagram of scenario sensitivity |
