# Mujib Basin Digital Twin - Validation Report

**Project root:** `C:\Users\proch\Desktop\THESIS\MUJIB_ALL_DATA\Digital_Twin\MUJIB_DT`  
**HTML:** `C:\Users\proch\Desktop\THESIS\MUJIB_ALL_DATA\Digital_Twin\MUJIB_DT\Cesium_71\Working_71.html`  
**Output:** `C:\Users\proch\Desktop\THESIS\MUJIB_ALL_DATA\Digital_Twin\MUJIB_DT\Cesium_71\validation_outputs`

## File contract
- OK: 35
- Required missing: 0
- Optional missing: 1
- Context only: 0

- Active HTML scenario file: `scenarios_USED_BY_CESIUM_FINAL_71_CMIP6_PROXY.json`

## Join diagnostics
| dataset          |   count |   matched_to_429 |   missing_vs_429 |   extra_vs_429 | first_missing_ids                                                  | first_extra_ids   |
|:-----------------|--------:|-----------------:|-----------------:|---------------:|:-------------------------------------------------------------------|:------------------|
| geojson_429      |     429 |              429 |                0 |              0 |                                                                    |                   |
| scenario_runtime |      71 |               66 |              363 |              5 | 73,74,75,77,78,79,80,82,83,84,85,86,87,88,89,90,91,92,93,94        | 1,2,5,6,35        |
| planner_profile  |     429 |              429 |                0 |              0 |                                                                    |                   |
| planner_master   |     429 |              429 |                0 |              0 |                                                                    |                   |
| era5_climate     |     411 |              411 |               18 |              0 | 9,21,53,70,104,203,219,227,243,277,282,304,354,364,377,406,425,449 |                   |

## Baseline reproduction summary
- **groundwater**: n=71, MAE=0.3254, RMSE=0.5349, R2=0.9985, MAPE=1.82%
- **runoff**: n=71, MAE=1.6902, RMSE=1.7273, R2=0.9977, MAPE=1.52%
- **sediment**: n=71, MAE=1.7488, RMSE=1.8533, R2=0.9659, MAPE=17.68%
- **vegetation**: n=71, MAE=1.5152, RMSE=1.5242, R2=0.9848, MAPE=0.87%

## Monotonicity tests
- Total: 140, Passed: 140, Failed: 0

## ERA5 summary
- Subbasins with ERA5 rows: 411  
- Records per subbasin: 1-1

## Suitability benchmark comparison
| label     |   mean |   benchmark_mean_mujib |   area_gte80_km2 |   benchmark_area80_mujib |   benchmark_area80_jordan |   extent_interpretation |
|:----------|-------:|-----------------------:|-----------------:|-------------------------:|--------------------------:|------------------------:|
| marab     |  75.83 |                   75.8 |             1258 |                     1258 |                      7583 |                     nan |
| vallerani |  80.64 |                   79   |             3265 |                     3265 |                     23316 |                     nan |


## Dashboard HTML sniff tests
| check                       | present   |
|:----------------------------|:----------|
| profile_json_ref            | True      |
| master_json_ref             | True      |
| scenario_json_ref           | True      |
| soil_csv_ref                | True      |
| ndvi_meta_ref               | True      |
| candidate_manifest_ref      | True      |
| compare_mode_ui             | True      |
| data_completeness_toggle    | True      |
| percent_toggle              | True      |
| heatmap_state_declared      | True      |
| heatmap_default_off         | True      |
| heatmap_auto_activation     | True      |
| screening_layer_id_declared | True      |
| swat71_guard_message        | True      |
| active_scenario_cmip6_proxy | True      |
| active_scenario_legacy71    | False     |

## Runtime notes

## Outputs
Tables: `C:\Users\proch\Desktop\THESIS\MUJIB_ALL_DATA\Digital_Twin\MUJIB_DT\Cesium_71\validation_outputs\tables`  
Figures: `C:\Users\proch\Desktop\THESIS\MUJIB_ALL_DATA\Digital_Twin\MUJIB_DT\Cesium_71\validation_outputs\figures`