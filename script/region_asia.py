import wbgapi as wb
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

print("Defining Asian Sub-regions...")

region_map = {
    'East Asia': [
        'CHN', 'JPN', 'MNG', 'KOR', 'PRK', 'HKG', 'MAC'   
    ],
    'Southeast Asia': [
        'IDN', 'THA', 'VNM', 'MYS', 'SGP', 'PHL', 'KHM', 'LAO', 'MMR', 'BRN', 'TLS'
    ],
    'South Asia': [
        'IND', 'PAK', 'BGD', 'LKA', 'NPL', 'BTN', 'MDV', 'AFG'
    ],
    'Central Asia': [
        'KAZ', 'UZB', 'KGZ', 'TJK', 'TKM'
    ],
    'West Asia / Middle East': [
        'SAU', 'ARE', 'QAT', 'BHR', 'OMN', 'KWT', 'TUR', 'ISR',
        'JOR', 'LBN', 'IRQ', 'IRN', 'YEM', 'SYR'
    ]
}

# Flatten dictionary → country_to_region mapping
country_to_region = {
    code: region for region, codes in region_map.items() for code in codes
}

all_codes = list(country_to_region.keys())
print(f"Fetching data for {len(all_codes)} Asian countries...")

indicators = {
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth',
    'SL.EMP.TOTL.SP.ZS': 'employment_ratio'
}

data_generator = wb.data.fetch(indicators.keys(), economy=all_codes, time=range(1990, 2024))
df_raw = pd.DataFrame(data_generator)

print("Structuring and aggregating data...")
df_raw['year'] = df_raw['time'].astype(str).str.replace('YR', '').astype(int)

df_pivoted = df_raw.pivot(
    index=['economy', 'year'],
    columns='series',
    values='value'
).reset_index()

df_pivoted = df_pivoted.rename(columns={
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth',
    'SL.EMP.TOTL.SP.ZS': 'employment_ratio'
})

df_pivoted['region'] = df_pivoted['economy'].map(country_to_region)

print("Aggregating by region using SQL...")

agg_query = """
SELECT
    region,
    year,
    AVG(gdp_growth) AS avg_gdp_growth,
    AVG(employment_ratio) AS avg_emp_ratio
FROM df_pivoted
WHERE region IS NOT NULL
GROUP BY region, year
ORDER BY region, year
"""

df_regional = duckdb.query(agg_query).df()

print("Generating regional comparison plots...")

sns.set_theme(style="whitegrid")

# GDP GROWTH COMPARISON
plt.figure(figsize=(12, 7))
sns.lineplot(
    data=df_regional,
    x='year', y='avg_gdp_growth',
    hue='region', linewidth=2, palette='bright'
)
plt.title('Average GDP Growth by Asian Sub-Region (1990–2023)')
plt.ylabel('GDP Growth (%)')
plt.xlabel('Year')
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('asia_subregions_gdp.png')
print("Saved: asia_subregions_gdp.png")

# EMPLOYMENT RATIO COMPARISON
plt.figure(figsize=(12, 7))
sns.lineplot(
    data=df_regional,
    x='year', y='avg_emp_ratio',
    hue='region', linewidth=2, palette='bright'
)
plt.title('Average Employment Ratio by Asian Sub-Region (1990–2023)')
plt.ylabel('Employment Ratio (%)')
plt.xlabel('Year')
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('asia_subregions_emp.png')
print("Saved: asia_subregions_emp.png")

print("Asian Sub-region Analysis Complete.")
