import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading Africa data from database...")

# Load data from existing database
conn = sqlite3.connect('data/data_africa.db')
df = pd.read_sql_query("""
    SELECT country, year, gdp_growth, employment_ratio
    FROM africa_data
    WHERE gdp_growth IS NOT NULL AND employment_ratio IS NOT NULL
""", conn)
conn.close()

print(f"Loaded {len(df)} records from {df['country'].nunique()} countries")
print(f"Time period: {int(df['year'].min())}-{int(df['year'].max())}")

# Set theme
sns.set_theme(style="whitegrid")

# 1. GDP Growth vs Employment over time (dual axis)
fig, ax1 = plt.subplots(figsize=(10, 6))

yearly_gdp = df.groupby('year')['gdp_growth'].mean()
yearly_emp = df.groupby('year')['employment_ratio'].mean()

color = 'tab:blue'
ax1.set_xlabel('Year', fontsize=11)
ax1.set_ylabel('GDP Growth (%)', color=color, fontsize=11)
ax1.plot(yearly_gdp.index, yearly_gdp.values, color=color, linewidth=2.5, marker='o', markersize=5, label='GDP Growth')
ax1.tick_params(axis='y', labelcolor=color)
ax1.axhline(y=0, color='red', linestyle='--', alpha=0.3, linewidth=1)
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Employment Ratio (%)', color=color, fontsize=11)
ax2.plot(yearly_emp.index, yearly_emp.values, color=color, linewidth=2.5, marker='s', markersize=5, linestyle='--', label='Employment Ratio')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Africa: GDP Growth vs Employment Ratio (2000-2023)', fontsize=13, fontweight='bold', pad=15)
fig.tight_layout()
plt.savefig('figures/africa_gdp_employment_trend.png', dpi=300, bbox_inches='tight')
print("Saved: figures/africa_gdp_employment_trend.png")
plt.close()

# 2. Scatter plot: GDP Growth vs Employment
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='gdp_growth', y='employment_ratio', s=80, alpha=0.6, color='steelblue')
plt.xlabel('GDP Growth (%)', fontsize=11)
plt.ylabel('Employment Ratio (%)', fontsize=11)
plt.title('Africa: Correlation between GDP Growth and Employment (2000-2023)',
          fontsize=12, fontweight='bold', pad=15)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('figures/africa_gdp_employment_scatter.png', dpi=300, bbox_inches='tight')
print("Saved: figures/africa_gdp_employment_scatter.png")
plt.close()

# Print summary statistics
print("\n" + "="*60)
print("AFRICA SUMMARY STATISTICS (2000-2023)")
print("="*60)
print(f"Countries analyzed: {df['country'].nunique()}")
print(f"Total observations: {len(df)}")
print(f"Average GDP Growth: {df['gdp_growth'].mean():.2f}%")
print(f"Average Employment Ratio: {df['employment_ratio'].mean():.2f}%")
print(f"GDP-Employment Correlation: {df['gdp_growth'].corr(df['employment_ratio']):.3f}")
print("="*60)

print("\nAfrica analysis complete!")
