import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- Load data ----------
df_gamma = pd.read_csv('C:/Users/User/ABM/rrr/gamma_sweep.csv', skiprows=6)
df_wh    = pd.read_csv('C:/Users/User/ABM/rrr/wh_sweep.csv', skiprows=6)
df_wf    = pd.read_csv('C:/Users/User/ABM/rrr/wf_sweep.csv', skiprows=6)
param_col = {
    'gamma_behavior': ('gamma_behavior', df_gamma),
    'w_h': ('influence_weight_household', df_wh),
    'w_f': ('influence_weight_friend', df_wf),
}

# ---------- Step 3: tornado swing table (mean-risk at tick 120) ----------
results = {}
for label, (col, df) in param_col.items():
    final = df[df['[step]'] == 120]
    grouped = final.groupby(col)['report-mean-risk'].agg(['mean', 'std']).reset_index()
    low_val = grouped[col].min()
    high_val = grouped[col].max()
    low_out = grouped.loc[grouped[col] == low_val, 'mean'].values[0]
    high_out = grouped.loc[grouped[col] == high_val, 'mean'].values[0]
    swing = abs(high_out - low_out)
    results[label] = dict(low_val=low_val, high_val=high_val,
                           low_out=low_out, high_out=high_out, swing=swing,
                           table=grouped)

# Rank by swing
ranked = sorted(results.items(), key=lambda kv: kv[1]['swing'], reverse=True)
for rank, (label, r) in enumerate(ranked, start=1):
    r['rank'] = rank

print("=== TORNADO TABLE (Step 3) ===")
print(f"{'Parameter':<15}{'Low val':<10}{'Low out':<12}{'High val':<10}{'High out':<12}{'Swing':<10}{'Rank'}")
for label, r in results.items():
    print(f"{label:<15}{r['low_val']:<10}{r['low_out']:<12.4f}{r['high_val']:<10}{r['high_out']:<12.4f}{r['swing']:<10.4f}{r['rank']}")

# ---------- Convergence tick ----------
# Definition: first tick where the rolling range (max-min) of report-mean-risk
# over the next 12 ticks stays below 0.05, per run, then averaged.
def convergence_tick(series_by_step, window=12, threshold=0.05):
    vals = series_by_step.values
    steps = series_by_step.index.values
    for i in range(len(vals) - window):
        segment = vals[i:i+window]
        if (segment.max() - segment.min()) < threshold:
            return steps[i]
    return np.nan

conv_results = {}
for label, (col, df) in param_col.items():
    ticks_found = []
    for (pval, run), grp in df.groupby([col, '[run number]']):
        grp = grp.sort_values('[step]').set_index('[step]')['report-mean-risk']
        t = convergence_tick(grp)
        if not np.isnan(t):
            ticks_found.append(t)
    conv_results[label] = dict(mean=np.mean(ticks_found), std=np.std(ticks_found), n=len(ticks_found))

print("\n=== CONVERGENCE TICK (mean-risk stabilises, <0.05 change over 12 ticks) ===")
for label, r in conv_results.items():
    print(f"{label}: mean tick = {r['mean']:.1f}  (std {r['std']:.1f}, n={r['n']} runs)")

# ---------- Boxplots: w_h and w_f effect on mean-risk at tick 120 ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, df, col, color in zip(
    axes,
    [df_wh, df_wf],
    ['influence_weight_household', 'influence_weight_friend'],
    ['#2E74B5', '#ADB9CA']
):
    final = df[df['[step]'] == 120]
    groups = [grp['report-mean-risk'].values for _, grp in final.groupby(col)]
    labels = sorted(final[col].unique())
    ax.boxplot(groups, tick_labels=[str(round(l,2)) for l in labels], patch_artist=True,
               boxprops=dict(facecolor=color, alpha=0.7))
    ax.set_xlabel(col)
    ax.set_ylabel('Mean Risk Score')
    ax.set_title(f'OAT: {col}')
    ax.grid(alpha=0.3)

plt.suptitle('Member 2: Influence Weight Sensitivity (at tick 120)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('member2_boxplots.png', dpi=150)
plt.close()

# ---------- Gamma line plot with error bars ----------
final_gamma = df_gamma[df_gamma['[step]'] == 120]
g = final_gamma.groupby('gamma_behavior')['report-mean-risk'].agg(['mean','std']).reset_index()
fig, ax = plt.subplots(figsize=(7,5))
ax.errorbar(g['gamma_behavior'], g['mean'], yerr=g['std'], fmt='-o', capsize=4, color='#1F4E79')
ax.set_xlabel('gamma_behavior')
ax.set_ylabel('Mean Risk Score (tick 120)')
ax.set_title('OAT: Effect of gamma_behavior on Mean CVD Risk')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('member2_gamma_lineplot.png', dpi=150)
plt.close()

# ---------- Tornado chart ----------
params = list(results.keys())
swings = [results[p]['swing'] for p in params]
order = np.argsort(swings)

fig, ax = plt.subplots(figsize=(8, 4))
ax.barh([params[i] for i in order], [swings[i] for i in order], color='#2E74B5')
ax.set_xlabel('Swing in Mean Risk Score (High - Low)')
ax.set_title('Tornado Chart -- Member 2: Behaviour Influence Parameters')
plt.tight_layout()
plt.savefig('member2_tornado.png', dpi=150)
plt.close()

print("\nSaved: member2_boxplots.png, member2_gamma_lineplot.png, member2_tornado.png")
