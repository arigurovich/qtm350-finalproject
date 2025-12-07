import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load cleaned data
conn = sqlite3.connect("south_asia/data/wdi.db")
df = pd.read_sql("SELECT * FROM south_asia_clean", conn)
conn.close()

df["year"] = df["year"].astype(int)

regional = df.groupby("year")[["gdp_growth", "employment_ratio"]].mean().reset_index()

# Calculate correlation
corr = regional["gdp_growth"].corr(regional["employment_ratio"])
print("Correlation between GDP growth and employment ratio:", round(corr, 3))

Path("south_asia/figures").mkdir(exist_ok=True)

fig, ax = plt.subplots(figsize=(10,6))

ax.scatter(
    regional["gdp_growth"],
    regional["employment_ratio"],
    s=55,
    alpha=0.7
)

ax.set_xlabel("GDP Growth (%)", fontsize=11)
ax.set_ylabel("Employment-to-Population Ratio (%)", fontsize=11)
ax.set_title("South Asia: GDP Growth vs Employment Ratio (1990–2023)", fontsize=13)

# Subtle grid
ax.grid(True, linestyle=":", alpha=0.6)

# Annotate correlation
corr = regional["gdp_growth"].corr(regional["employment_ratio"])

ax.text(
    x=regional["gdp_growth"].min(),
    y=regional["employment_ratio"].max(),
    s=f"Correlation = {corr:.2f}",
    fontsize=11,
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
)

fig.tight_layout()
fig.savefig("south_asia/figures/gdp_vs_employment_scatter.png", dpi=300)
plt.close(fig)

print("Correlation plot saved")
