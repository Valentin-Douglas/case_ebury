# Ebury Data Engineering Case Study

## Overview
This repository contains the solution for the Ebury Data Engineering Case Study. 
It implements a resilient ETL (Extract, Transform, Load) pipeline and a Data Querying module using Python, Pandas, and SQLite, all fully containerized using Docker.

The architecture follows S.O.L.I.D. principles, ensuring modularity, easy maintenance, and scalability.

## Project Architecture
The project is divided into two main components as requested:
1. **Part 1 - ETL Pipeline:** Extracts data from a semi-structured (and partially malformed/dirty) JSON file, applies a strict Data Contract, flattens nested structures, and loads the cleaned data into a dimensional SQLite database (`Payment` and `Partner` tables).
2. **Part 2 - Querying:** Connects to the generated SQLite database, extracts the tables into Pandas DataFrames, and performs analytical operations to answer the proposed business questions.

To run the process, follow these steps:
1. **Powershell Terminal** Run the following command inside the project folder to build the Docker image: docker build -t case-ebury .
2. **Excecute the Docker Image** Just run the Docker image and container.

## Folder Structure After Run The Solution
```text
case_ebury/
├── data/
│   └── case_study_json_file.json  # Raw data goes here (not versioned)
├── db_volume/                     # Docker volume mapping for SQLite DB and Reports
│   ├── ebury_datalake.db          # Datalake generated from the JSON file
│   └── msc/
│       └── reports/               # Generated PNG visualization charts
├── step_01_extract_data.py        # Resilient JSON Line extraction logic
├── step_02_transform_data.py      # Data Contract and cleaning logic
├── step_03_01_dt_utils.py         # Database validation utilities (SRP compliant)
├── step_03_02_smart_load.py       # Smart Database ingestion logic (Append/Skip)
├── step_03_03_load_data.py        # Orchestrator for the data loading phase
├── step_04_fetch_data_retrive.py  # Database querying logic via Pandas
├── step_05_reporting.py           # Deterministic data visualization logic
├── main.py                        # Main orchestrator
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container configuration
└── README.md                      # Project documentation