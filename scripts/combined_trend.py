import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load clean data 
conn = sqlite3.connect("south_asia/data/wdi.db")
df = pd.read_sql("SELECT year, gdp_growth, employment_ratio FROM south_asia_clean", conn)
conn.close()

# Convert year to int
df["year"] = df["year"].astype(int)

# Regional averages by year
regional = (
    df.groupby("year")[["gdp_growth", "employment_ratio"]]
      .mean()
      .reset_index()
)

# Ensure figures folder exists
Path("south_asia/figures").mkdir(exist_ok=True)

fig, ax1 = plt.subplots(figsize=(10, 6))

# GDP Growth (left axis)
gdp_line = ax1.plot(
    regional["year"],
    regional["gdp_growth"],
    color="tab:blue",
    linewidth=2.5,
    marker="o",
    markersize=4,
    label="GDP Growth (%)"
)
ax1.set_xlabel("Year", fontsize=11)
ax1.set_ylabel("GDP Growth (%)", color="tab:blue", fontsize=11)
ax1.tick_params(axis="y", labelcolor="tab:blue")

# Employment ratio (right axis)
ax2 = ax1.twinx()
emp_line = ax2.plot(
    regional["year"],
    regional["employment_ratio"],
    color="tab:green",
    linestyle="--",
    linewidth=2.5,
    marker="s",
    markersize=4,
    label="Employment Ratio (%)"
)
ax2.set_ylabel("Employment-to-Population Ratio (%)", color="tab:green", fontsize=11)
ax2.tick_params(axis="y", labelcolor="tab:green")

# ---- Combine legends ----
lines = gdp_line + emp_line
labels = [l.get_label() for l in lines]
ax1.legend(
    lines,
    labels,
    loc="upper left",
    frameon=True
)

ax1.grid(True, linestyle=":", alpha=0.6)
plt.title("South Asia: GDP Growth vs Employment Ratio (1990–2023)", fontsize=13)
fig.tight_layout()

fig.savefig("south_asia/figures/gdp_and_employment_combined_trend.png", dpi=300)
plt.close(fig)

print("Combined figure saved")