import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Load CLEAN data from SQLite
conn = sqlite3.connect("south_asia/data/wdi.db")
df = pd.read_sql("SELECT * FROM south_asia_clean", conn)
conn.close()

# 2. Make sure year is numeric
df["year"] = df["year"].astype(int)

# 3. Compute regional averages by year
regional = (
    df.groupby("year")[["gdp_growth", "employment_ratio"]]
      .mean()
      .reset_index()
)

# 4. Ensure figures folder exists
Path("south_asia/figures").mkdir(exist_ok=True)

# 5. Plot GDP growth trend over time
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(
    regional["year"],
    regional["gdp_growth"],
    linewidth=2.5,
    marker="o",
    markersize=4,
)

ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("GDP Growth (%)", fontsize=11)
ax.set_title("South Asia: Average GDP Growth Over Time (1990 - 2023)", fontsize=13)

ax.grid(True, linestyle=":", alpha=0.6)

fig.tight_layout()
fig.savefig("south_asia/figures/gdp_growth_trend.png", dpi=300)
plt.close(fig)

# 6. Plot employment ratio trend over time
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(
    regional["year"],
    regional["employment_ratio"],
    linewidth=2.5,
    marker="s",
    markersize=4,
)

ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Employment-to-Population Ratio (%)", fontsize=11)
ax.set_title("South Asia: Employment-to-Population Ratio Over Time (1990-2023)", fontsize=13)

ax.grid(True, linestyle=":", alpha=0.6)

fig.tight_layout()
fig.savefig("south_asia/figures/employment_ratio_trend.png", dpi=300)
plt.close(fig)

print("Trend plots saved in south_asia/figures")
