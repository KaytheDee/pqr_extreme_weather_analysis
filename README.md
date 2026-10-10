# pqr_extreme_weather_analysis

This repository contains data-processing and analysis workflows used to investigate relationships between extreme weather, power outages, voltage quality, and community-level climate vulnerability in Greater Accra, Ghana (2022 - 2023).

The analysis combines power-quality measurements, weather observations, spatial data, and a custom climate vulnerability index.

## Research Overview

The project examines:

- The spatial and temporal distribution of power outages and voltage-quality events
- The occurrence of extreme-weather events and their associations with power outages & undervoltages
- Differences in grid outcomes across communities with different levels of climate vulnerability
- Same-day and multi-day relationships between weather events and outages

Analyses are primarily conducted at the enumeration-area (EA) level.

## Repository Structure

```text
.
├── files/                  # Input and intermediate datasets
│   ├── SAIDI_SAIFI/
│   ├── miscellaneous/
│   ├── processed_undervolt_data/
│   ├── processed_weather_data/
│   └── spatial docs_to_cluster/
├── notebooks/              # Data analysis and visualization workflows
│   ├── archived/           # Superseded and duplicate notebooks
│   └── supporting_analyses/ # Optional supporting analyses
├── outputs/
│   └── plots/              # Figures produced by the analyses
├── scripts/                # Raw voltage-processing scripts
├── LICENSE
└── README.md
```

## Data Access

The datasets used in this analysis are organized under `files/`.

| Dataset | Repository location | Description |
|---|---|---|
| Processed hourly undervoltage data | `files/processed_undervolt_data/` | Hourly voltage measurements derived from the raw two-minute PQR sensor data. |
| Processed TAHMO weather-station data | `files/processed_weather_data/` | Processed temperature, precipitation, wind, and lightning observations. |
| nLine-processed reliability metrics | `files/SAIDI_SAIFI/` | Daily reliability metrics processed by nLine. |
| Analysis and mapping data | `files/miscellaneous/` | CESI values, sensor-to-EA mappings, site lists, and other supporting files. |
| Spatial data and weather-comparison inputs | `files/spatial docs_to_cluster/` | EA and district boundaries and selected spatial inputs used by the mapping and weather-comparison notebooks. |

### External and Restricted Data

Some source datasets are too large to distribute through GitHub and/or only available through their original providers. These include the PQR sensor data, the weather data, and geographic shapefiles.

To reproduce the complete workflow from the raw data, obtain access to the required source datasets and update the input paths in the corresponding scripts or notebooks. The following provenance and access information should be added where applicable:

- PQR data: [nLine GridWatch public data](https://nline.io/public-data/gridwatch)
- TAHMO observations: [TAHMO climate data](https://tahmo.org/climate-data/)
- Study area shapefiles: can be shared with permission from the original source
- Copernicus product: [ERA5 hourly data on single levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels)
- CHIRPS precipitation product: [CHIRPS data access](https://www.chc.ucsb.edu/data/chirps)

The processed files currently included under `files/` can be used to reproduce the primary statistical analyses without rerunning the preparation steps.

## Setup

Clone the repository:

```bash
git clone https://github.com/KaytheDee/pqr_extreme_weather_analysis.git
cd pqr_extreme_weather_analysis
```

Create and activate a Python virtual environment, then install the required scientific Python and Jupyter packages. A pinned `requirements.txt` or `environment.yml` has not yet been added to this repository.

Start Jupyter from the `notebooks/` directory because the notebooks use relative paths such as `../files` and `../outputs`:

```bash
cd notebooks
jupyter lab
```

## Reproducing the Analysis

### Primary Workflow

#### 1. Prepare Hourly Voltage Measurements

Run:

- `scripts/Undervolt_process_rev5_22_hourly_averaging.py`
- `scripts/Undervolt_process_rev5_23_hourly_averaging.py`

These scripts convert the original two-minute PQR voltage measurements into hourly measurements using valid, non-zero voltage observations.

The resulting processed datasets are stored in:

- `files/processed_undervolt_data/undervolt_hourly_voltages_df_22.csv`
- `files/processed_undervolt_data/undervolt_hourly_voltages_df_23.csv`

The scripts currently contain absolute paths. Update the input and output paths before running them in a different computing environment. If using the processed hourly voltage files already included in the repository, you can skip this step. 

#### 2. Process the CESI Data

Run:

- `notebooks/new_durations_Spatial_Analysis_EAs.ipynb`

This notebook processes the custom CESI index for the each of the 214 EAs included in the study area. This index is used by the regression and spatial analyses. 
If using the processed CESI files already included under `files/miscellaneous/`, this step can be skipped.

#### 3. Summarize the Processed Undervoltage Data

Run:

- `notebooks/_pre_processing_undervolt_workflow_rev3_process_with_plotting.ipynb`

This notebook combines the processed 2022 and 2023 hourly voltage data with temperature, sensor, and CESI information. It summarizes the hourly voltages, characterizes undervoltage frequency and severity, and produces temporal voltage and temperature plots.

This workflow is distinct from `supporting_analyses/_pre_processing_undervolt_workflow_rev4_regression_weather_vars.ipynb`, which contains the optional comparison of voltage with all weather variables described below.

#### 4. Run the Voltage-Temperature Analyses

Run:

- `notebooks/_00_OLS_Undervoltage_Temperature_hrly_from_cluster.ipynb`
- `notebooks/_01_Logit_Undervoltage_Temperature.ipynb`
- `notebooks/_01_Logit_Undervoltage_Temperature_with_CESI_interaction.ipynb`

These notebooks contain:

1. OLS models of hourly voltage and temperature (study-wide and sensor-level)
2. Logistic models of undervoltage and heat spell (study-wide and sensor-level)
3. Logistic models of undervoltage and heat spell: study-wide and with CESI interactions

#### 5. Run the Outage and Extreme-Weather Analyses

Run the applicable `_Logit_Co_occurrence...` notebooks:

- `notebooks/_Logit_Co_occurrence_per_EA_overlapping_hours_full_model_same_day.ipynb`
- `notebooks/_Logit_Co_occurrence_per_EA_overlapping_hours_full_model_same_day_CESI.ipynb`
- `notebooks/_Logit_Co_occurrence_per_EA_overlapping_hours_full_model_3_day_rev1.ipynb`

These notebooks estimate associations between extreme-weather events and outages at the EA level. They cover same-day and multi-day relationships and include analyses with CESI interactions where indicated.

#### 6. Produce the Spatial Analyses

Run:

- `notebooks/_Logit_spatial_analysis_undervolt.ipynb`
- `notebooks/_Logit_spatial_analysis_outage_per_EA_rev2.ipynb`

`_Logit_spatial_analysis_undervolt.ipynb` maps sensors and sites according to their estimated temperature-voltage and heat-spell-undervoltage relationships.

`_Logit_spatial_analysis_outage_per_EA_rev2.ipynb` maps EAs with increased outage odds for each extreme-weather event, including results disaggregated by CESI.

#### 7. Produce Monthly Summaries and Reliability Comparisons

Run:

- `notebooks/Extreme_Weather_per_Month_rev1.ipynb`
- `notebooks/PQR_Metrics_per_Month_SAIDI_22_23.ipynb`
- `notebooks/PQR_Metrics_yearly.ipynb`

`Extreme_Weather_per_Month_rev1.ipynb` produces daily and monthly heatmaps showing the frequency & spatial extent of each extreme-weather event.

`PQR_Metrics_per_Month_SAIDI_22_23.ipynb` shows the monthly distributions of the PQR-derived SAIDI metrics for 2022 and 2023.

`PQR_Metrics_yearly.ipynb` compares the yearly distributions of sensor-estimated reliability metrics with the officially reported values.

### Optional Analyses

#### Produce Supplementary Study-Area Maps

Run:

- `notebooks/supporting_analyses/Spatial_Analysis_EAs_REV3.ipynb`

This notebook produces supplementary geospatial views of the study area, including the study-area boundaries, EAs of interest, weather stations, and PQR sites.

#### Compare Station and Satellite Weather Products

The following notebooks compare TAHMO weather-station observations with satellite or gridded weather products:

- `notebooks/supporting_analyses/Weather_Copernicus_Tahmo_reg_22.ipynb`
- `notebooks/supporting_analyses/Weather_CHIRPS_Tahmo_reg_22.ipynb`

The Copernicus notebook compares temperature observations, while the CHIRPS notebook compares precipitation observations. These supporting analyses examine disagreement between the station-based and satellite or gridded products and show why the satellite products were not suitable for the primary analysis.

To replicate these comparisons, download the source satellite-product files using the links in the Data Access section and update the notebooks' input paths as needed.

#### Compare Voltage with All Extreme-Weather Variables

Run:

- `notebooks/supporting_analyses/_pre_processing_undervolt_workflow_rev4_regression_weather_vars.ipynb`

This notebook compares the association between hourly voltage measurements and each weather variable. It is an optional supporting analysis used to show that voltage was more strongly associated with temperature than with the other weather variables.

#### Produce Supplementary Distributions

Run:

- `notebooks/supporting_analyses/__Supplementary_plots.ipynb`

This notebook produces distributions and cumulative distribution functions for the weather variables and extreme-weather hours. It is a supporting analysis and is not required to reproduce the primary models.

## Analysis Notebook Reference

| Research output | Primary notebook |
|---|---|
| Hourly voltage-temperature OLS | `_00_OLS_Undervoltage_Temperature_hrly_from_cluster.ipynb` |
| Undervoltage logistic model | `_01_Logit_Undervoltage_Temperature.ipynb` |
| Undervoltage model with CESI interaction | `_01_Logit_Undervoltage_Temperature_with_CESI_interaction.ipynb` |
| Hourly undervoltage summaries and temporal plots | `_pre_processing_undervolt_workflow_rev3_process_with_plotting.ipynb` |
| Same-day and multi-day outage/weather models | `_Logit_Co_occurrence...ipynb` |
| Sensor voltage-temperature sensitivity maps | `_Logit_spatial_analysis_undervolt.ipynb` |
| EA outage-risk maps by weather event and CESI | `_Logit_spatial_analysis_outage_per_EA_rev2.ipynb` |
| Daily and monthly extreme-weather heatmaps | `Extreme_Weather_per_Month_rev1.ipynb` |
| Monthly distributions of PQR-derived SAIDI metrics for 2022 and 2023 | `PQR_Metrics_per_Month_SAIDI_22_23.ipynb` |
| Yearly reliability-metric comparison (sensor-estimated versus official values) | `PQR_Metrics_yearly.ipynb` |
| CESI processing for 214 EAs | `new_durations_Spatial_Analysis_EAs.ipynb` |
| Supplementary study-area maps (optional) | `supporting_analyses/Spatial_Analysis_EAs_REV3.ipynb` |
| TAHMO versus Copernicus comparison (optional) | `supporting_analyses/Weather_Copernicus_Tahmo_reg_22.ipynb` |
| TAHMO versus CHIRPS comparison (optional) | `supporting_analyses/Weather_CHIRPS_Tahmo_reg_22.ipynb` |
| Voltage comparison across weather variables (optional) | `supporting_analyses/_pre_processing_undervolt_workflow_rev4_regression_weather_vars.ipynb` |
| Supplementary weather distributions/CDFs (optional) | `supporting_analyses/__Supplementary_plots.ipynb` |

## Outputs

Generated figures are written to:

```text
outputs/plots/
outputs/plots/supplementary/
```

Unless otherwise noted, intermediate and derived tabular datasets are stored under `files/`.

## Reproducibility Notes

- Run notebooks from the `notebooks/` directory so relative paths resolve correctly.
- Several notebooks contain exploratory sections and optional output-writing cells. Confirm which cells should be enabled before executing a complete run.
- Some intermediate files are read by downstream notebooks even though the cells that create them may be commented out.
- The raw voltage-processing scripts contain cluster-specific absolute paths. These paths need to be replaced only when rerunning the raw-data processing; the processed hourly files are already included in the repository.

## Code Marked for Archiving

The following notebooks are retained temporarily:

- `notebooks/archived/Extreme_Weather_per_Month.ipynb`
- `notebooks/archived/_Logit_Co_occurrence_per_EA_overlapping_hours_full_model_3_day.ipynb`
- `notebooks/archived/_Logit_spatial_analysis_outage_per_EA.ipynb`
- `notebooks/archived/_Logit_spatial_analysis_outage_per_EA_rev1.ipynb`
- `notebooks/archived/_Logit_spatial_analysis_outage_per_EA_rev2_copy.ipynb`
- `notebooks/archived/_Logit_spatial_analysis_rev1.ipynb`
- `notebooks/archived/_Logit_spatial_analysis_undervolt_Copy1.ipynb`
- `notebooks/archived/_pre_processing_undervolt_workflow_rev1_process_with_plotting_with_CESI.ipynb`

Additional superseded or duplicate notebooks may be moved to an archive as the repository is consolidated.
