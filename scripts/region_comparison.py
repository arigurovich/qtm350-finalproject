import wbgapi as wb
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

print("Defining European Sub-regions...")
region_map = {
    'Northern Europe': ['DNK', 'FIN', 'ISL', 'NOR', 'SWE', 'EST', 'LVA', 'LTU'], 
    'Southern Europe': ['ITA', 'GRC', 'PRT', 'HRV', 'MLT', 'CYP'],              
    'Eastern Europe':  ['RUS', 'UKR', 'BGR', 'ROU', 'MDA', 'BLR'],              
    'Western Europe':  ['FRA', 'ESP', 'BEL', 'NLD', 'CHE', 'LUX'],               
    'Central Europe':  ['DEU', 'POL', 'AUT', 'HUN', 'CZE', 'SVK', 'SVN'],        
    'British Isles':   ['GBR', 'IRL']                                            
}
country_to_region = {code: region for region, codes in region_map.items() for code in codes}
all_codes = list(country_to_region.keys())
print(f"Fetching data for {len(all_codes)} countries...")
indicators = {
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth',
    'SL.EMP.TOTL.SP.ZS': 'employment_ratio'
}

data_generator = wb.data.fetch(indicators.keys(), economy=all_codes, time=range(1990, 2024))
df_raw = pd.DataFrame(data_generator)
print("Structuring and aggregating data...")
df_raw['year'] = df_raw['time'].astype(str).str.replace('YR', '').astype(int)
df_pivoted = df_raw.pivot(index=['economy', 'year'], columns='series', values='value').reset_index()
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
    AVG(gdp_growth) as avg_gdp_growth,
    AVG(employment_ratio) as avg_emp_ratio
FROM df_pivoted
WHERE 
    region IS NOT NULL
GROUP BY region, year
ORDER BY region, year
"""
df_regional = duckdb.query(agg_query).df()
print("Generating regional comparison plots...")
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))
sns.lineplot(data=df_regional, x='year', y='avg_gdp_growth', hue='region', linewidth=2, palette='bright')
plt.title('Average GDP Growth by European Sub-Region (1990-2023)')
plt.ylabel('GDP Growth (%)')
plt.xlabel('Year')
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('figures/europe_subregions_gdp.png')
print("Saved: europe_subregions_gdp.png")
plt.figure(figsize=(12, 7))
sns.lineplot(data=df_regional, x='year', y='avg_emp_ratio', hue='region', linewidth=2, palette='bright')
plt.title('Average Employment Ratio by European Sub-Region')
plt.ylabel('Employment Ratio (%)')
plt.xlabel('Year')
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('figures/europe_subregions_emp.png')
print("Saved: europe_subregions_emp.png")
print("Sub-region Analysis Complete.")