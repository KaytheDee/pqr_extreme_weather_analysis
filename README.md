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
├── files/
│   ├── SAIDI_SAIFI/
│   ├── miscellaneous/
│   ├── processed_undervolt_data/
│   ├── processed_weather_data/
│   └── spatial docs_to_cluster/
├── notebooks/
├── outputs/
│   └── plots/
├── scripts/
├── LICENSE
└── README.md