# Power Quality, Outages, and Extreme Weather in Greater Accra

# pqr_extreme_weather_analysis

This repository contains data-processing and analysis workflows used to investigate relationships between extreme weather, power outages, voltage quality, and community-level climate vulnerability in Greater Accra, Ghana.

The analysis combines power-quality measurements, weather observations, spatial data, and a Climate Exposure and Sensitivity Index (CESI). The primary study period is 2022–2023.

## Research Overview

The project examines:

- The spatial and temporal distribution of power outages and voltage-quality events
- The occurrence of temperature, precipitation, wind, lightning, and compound extreme-weather events
- Associations between extreme weather and power outages
- Associations between temperature and undervoltage
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