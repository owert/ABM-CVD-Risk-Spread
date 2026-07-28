import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set clean aesthetic style for academic journal presentation
sns.set_theme(style="whitegrid", font_scale=1.1)

# ==========================================
# 1. PROCESS EXPERIMENT 4A: INFLOW EFFECTS
# ==========================================
# NetLogo exports header info in the first few rows; skiprows=6 handles standard BehaviorSpace headers
df_4a = pd.read_csv("CVD_Risk_Behaviour Experiment_4A_Inflow-table.csv", skiprows=6)

# Clean column names by stripping spaces and quotes
df_4a.columns = [col.replace('"', '').strip() for col in df_4a.columns]

plt.figure(figsize=(9, 5))
sns.lineplot(
    data=df_4a,
    x="[step]",
    y="mean [risk-score] of turtles",
    hue="annual_inflow",
    palette="viridis",
    linewidth=2
)
plt.title("Figure 1: Mean CVD Risk Score Trajectory Across Annual City Inflow Rates", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Time (Months)", fontsize=11)
plt.ylabel("Mean CVD Risk Score", fontsize=11)
plt.legend(title="Annual Inflow ($annual\_inflow$)", title_fontsize='10', loc="upper right")
plt.tight_layout()
plt.savefig("Fig1_Inflow_Risk_Trajectory.png", dpi=300)
plt.show()

# ==========================================
# 2. PROCESS EXPERIMENT 4B: OUT-MIGRATION & NETWORK DENSITY
# ==========================================
df_4b = pd.read_csv("CVD_Risk_Behaviour Experiment_4B_Outmigration-table.csv", skiprows=6)
df_4b.columns = [col.replace('"', '').strip() for col in df_4b.columns]

# Filter for the final state at tick 120 (10 years)
df_4b_final = df_4b[df_4b["[step]"] == 120]

fig, ax1 = plt.subplots(figsize=(8, 5))

color = 'tab:blue'
ax1.set_xlabel('Monthly Out-Migration Probability ($monthly-outmigration-prob$)', fontsize=11)
ax1.set_ylabel('Mean Degree / Friends per Agent', color=color, fontsize=11)
sns.boxplot(
    data=df_4b_final,
    x="monthly-outmigration-prob",
    y="mean [count link-neighbors] of turtles",
    ax=ax1,
    palette="Blues"
)
ax1.tick_params(axis='y', labelcolor=color)

plt.title("Figure 2: Steady-State Network Density Under Out-Migration Rates", fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig("Fig2_Outmigration_Network_Density.png", dpi=300)
plt.show()

# ==========================================
# 3. PROCESS EXPERIMENT 4C: GROWTH VS HOMOPHILY
# ==========================================
df_4c = pd.read_csv("CVD_Risk_Behaviour Experiment_4C_Growth_Homophily-table.csv", skiprows=6)
df_4c.columns = [col.replace('"', '').strip() for col in df_4c.columns]
df_4c_final = df_4c[df_4c["[step]"] == 120]

plt.figure(figsize=(8, 5))
sns.barplot(
    data=df_4c_final,
    x="annual_inflow",
    y="mean [risk-score] of turtles",
    hue="theta_tol",
    palette="magma"
)
plt.title("Figure 3: Final Risk Score Under Rapid Inflow and Mismatch Tolerance", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Annual City Inflow ($annual\_inflow$)", fontsize=11)
plt.ylabel("Mean CVD Risk Score at Tick 120", fontsize=11)
plt.legend(title="Mismatch Tolerance ($\\theta_{tol}$)", title_fontsize='10')
plt.tight_layout()
plt.savefig("Fig3_Growth_vs_Homophily.png", dpi=300)
plt.show()
print("All 3 figures successfully generated and saved!")