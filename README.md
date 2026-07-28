# Extending an Agent-Based Model of Cardiovascular Disease Risk Behaviour Spread

This repository contains the NetLogo agent-based model (ABM), empirical demographic datasets, BehaviorSpace output tables, and analysis scripts for the study on dynamic network adaptation and urban demographic churn in CVD risk behavior spread.

## Repository Structure

- `models/`: NetLogo model code (`.nlogo`).
- `data/raw_demographics/`: Initial demographic distribution data (`age_distribution.csv`, `employed.csv`, `sex.csv`).
- `data/behavior_space_results/`: Raw CSV outputs from NetLogo BehaviorSpace parameter sweeps (Experiments 4A, 4B, 4C).
- `scripts/`: Python scripts used for processing simulation output tables and generating publication figures.
- `docs/`: Model documentation.

## Requirements

- **NetLogo:** Version 6.x or higher.
- **Python:** Version 3.8+ (Required for analysis scripts).
  - Python Libraries: `pandas`, `matplotlib`, `seaborn`, `numpy`.

## How to Run the Simulations

1. Launch **NetLogo**.
2. Open `models/CVD_Risk_Behaviour.nlogo`.
3. Ensure input demographic CSVs in `data/raw_demographics/` are accessible relative to the model path.
4. Click `setup` and `go` to run interactive single-run simulations.

### Reproducing Experiments (BehaviorSpace)
1. In NetLogo, navigate to **Tools -> BehaviorSpace**.
2. Select the relevant experiment configuration (`Experiment_4A_Inflow`, `Experiment_4B_Outmigration`, or `Experiment_4C_Growth_Homophily`).
3. Click **Run** and export table outputs to the `data/behavior_space_results/` folder.

## Reproducing Figures and Analysis

Run the Python analysis script to generate figures:
```bash
python scripts/analysis_and_plots.py
