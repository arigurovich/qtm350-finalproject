import wbgapi as wb
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

print("Fetching data from World Bank...")

# Same indicators as Europe
indicators = {
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth',
    'SL.EMP.TOTL.SP.ZS': 'employment_ratio'
}

# Use World Bank regional aggregate for East Asia & Pacific: 'EAS'
# (analogous to using 'ECS' for Europe & Central Asia)
data_generator = wb.data.fetch(indicators.keys(), economy='EAS', time=range(1990, 2024))
df_raw = pd.DataFrame(data_generator)

print("Structuring data...")

df_raw['year'] = df_raw['time'].astype(str).str.replace('YR', '').astype(int)

df_pivoted = df_raw.pivot(
    index='year',
    columns='series',
    values='value'
).reset_index()

df_pivoted = df_pivoted.rename(columns={
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth',
    'SL.EMP.TOTL.SP.ZS': 'employment_ratio'
})

print("Columns available:", df_pivoted.columns.tolist())

print("Cleaning data using SQL...")

clean_query = """
SELECT
    year,
    gdp_growth,
    employment_ratio
FROM df_pivoted
WHERE
    gdp_growth IS NOT NULL
    AND employment_ratio IS NOT NULL
ORDER BY year
"""

df_cleaned = duckdb.query(clean_query).df()

print("Calculating statistics using SQL...")

stats_query = """
SELECT
    AVG(gdp_growth) AS avg_gdp_growth,
    STDDEV(gdp_growth) AS std_gdp_growth,
    AVG(employment_ratio) AS avg_emp_ratio,
    STDDEV(employment_ratio) AS std_emp_ratio,
    CORR(gdp_growth, employment_ratio) AS correlation
FROM df_cleaned
"""

stats_df = duckdb.query(stats_query).df()

print("\n--- Descriptive Statistics (Asia) ---")
print(stats_df)
print("---------------------------------------")

print("Generating plots...")
sns.set_theme(style="whitegrid")

# Time series plot: GDP growth vs Employment ratio (Asia)
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Year')
ax1.set_ylabel('GDP Growth (%)', color=color)
ax1.plot(df_cleaned['year'], df_cleaned['gdp_growth'], color=color, linewidth=2, label='GDP Growth')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Employment Ratio (%)', color=color)
ax2.plot(df_cleaned['year'], df_cleaned['employment_ratio'], color=color,
         linewidth=2, linestyle='--', label='Emp Ratio')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Asia (East Asia & Pacific): GDP Growth vs Employment Ratio (1990-2023)')
fig.tight_layout()
plt.savefig('asia_evolution_plot.png')
print("Saved: asia_evolution_plot.png")

# Scatter plot: correlation between GDP growth and employment ratio
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_cleaned, x='gdp_growth', y='employment_ratio', s=100)
plt.title('Correlation: GDP Growth vs Employment Ratio (Asia)')
plt.xlabel('GDP Growth (%)')
plt.ylabel('Employment Ratio (%)')
plt.tight_layout()
plt.savefig('asia_scatter_plot.png')
print("Saved: asia_scatter_plot.png")

print("Analysis Complete.")
