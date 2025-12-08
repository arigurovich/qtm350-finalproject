import wbgapi as wb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Fetching Africa data from World Bank...")

# African countries
countries = ['DZA', 'EGY', 'ETH', 'GHA', 'KEN', 'MAR', 'NGA', 'ZAF', 'TZA', 'UGA']

# Fetch GDP growth and employment data
gdp = wb.data.DataFrame('NY.GDP.MKTP.KD.ZG', countries, time=range(2000, 2024), numericTimeKeys=True)
emp = wb.data.DataFrame('SL.EMP.TOTL.SP.ZS', countries, time=range(2000, 2024), numericTimeKeys=True)

# Reshape to long format
gdp_long = gdp.reset_index().melt(id_vars='economy', var_name='year', value_name='gdp_growth')
emp_long = emp.reset_index().melt(id_vars='economy', var_name='year', value_name='employment_ratio')

# Combine and clean
df = gdp_long.merge(emp_long, on=['economy', 'year'])
df.columns = ['country', 'year', 'gdp_growth', 'employment_ratio']
df_clean = df.dropna(subset=['gdp_growth', 'employment_ratio'])

print(f"Loaded {len(df_clean)} records from {df_clean['country'].nunique()} countries")
print(f"Time period: {int(df_clean['year'].min())}-{int(df_clean['year'].max())}")

# Set theme
sns.set_theme(style="whitegrid")

# 1. GDP Growth vs Employment over time (dual axis)
fig, ax1 = plt.subplots(figsize=(10, 6))

yearly_gdp = df_clean.groupby('year')['gdp_growth'].mean()
yearly_emp = df_clean.groupby('year')['employment_ratio'].mean()

color = 'tab:blue'
ax1.set_xlabel('Year')
ax1.set_ylabel('GDP Growth (%)', color=color)
ax1.plot(yearly_gdp.index, yearly_gdp.values, color=color, linewidth=2, marker='o', label='GDP Growth')
ax1.tick_params(axis='y', labelcolor=color)
ax1.axhline(y=0, color='red', linestyle='--', alpha=0.3)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Employment Ratio (%)', color=color)
ax2.plot(yearly_emp.index, yearly_emp.values, color=color, linewidth=2, marker='s', linestyle='--', label='Employment Ratio')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Africa: GDP Growth vs Employment Ratio (2000-2023)', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.savefig('figures/africa_gdp_employment_trend.png', dpi=300, bbox_inches='tight')
print("Saved: figures/africa_gdp_employment_trend.png")

# 2. Scatter plot: GDP Growth vs Employment
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_clean, x='gdp_growth', y='employment_ratio', s=80, alpha=0.6)
plt.xlabel('GDP Growth (%)')
plt.ylabel('Employment Ratio (%)')
plt.title('Africa: Correlation between GDP Growth and Employment', fontsize=12, fontweight='bold')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('figures/africa_gdp_employment_scatter.png', dpi=300, bbox_inches='tight')
print("Saved: figures/africa_gdp_employment_scatter.png")

# Print summary statistics
print("\n" + "="*60)
print("AFRICA SUMMARY STATISTICS (2000-2023)")
print("="*60)
print(f"Average GDP Growth: {df_clean['gdp_growth'].mean():.2f}%")
print(f"Average Employment Ratio: {df_clean['employment_ratio'].mean():.2f}%")
print(f"Correlation: {df_clean['gdp_growth'].corr(df_clean['employment_ratio']):.3f}")
print("="*60)

print("\nAnalysis complete!")
