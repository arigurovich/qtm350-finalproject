import wbgapi as wb
import pandas as pd
import sqlite3
from pathlib import Path

# Economic indicators
INDICATORS = [
    "NY.GDP.MKTP.KD.ZG",   # GDP growth (annual %)
    "SL.EMP.TOTL.SP.ZS"   # Employment-to-population ratio (%)
]

# Get list of South Asia country codes (SAS region)
sas_members = wb.region.members("SAS")
sas_codes = list(sas_members)   # just turn the generator into a list of codes

# Download WDI data for those economies
df = wb.data.DataFrame(
    INDICATORS,
    economy=sas_codes,
    time=range(1990, 2024),
    columns="series"
).reset_index()


df.columns = [
    "country_code",
    "year",
    "gdp_growth",
    "employment_ratio"
]

df.columns = [
    "country_code",
    "year",
    "gdp_growth",
    "employment_ratio"
]

# (Optional) create a simple 'country' column equal to the code,
# so later we can relabel if we want nicer names.
df["country"] = df["country_code"]

# Final column order
df = df[
    ["country_code", "country", "year",
     "gdp_growth", "employment_ratio"]
]

# Ensure folder exists
Path("south_asia/data").mkdir(exist_ok=True)

# Save CSV
df.to_csv("south_asia/data/south_asia_data.csv", index=False)

# Save SQLite DB
conn = sqlite3.connect("south_asia/data/wdi.db")
df.to_sql("south_asia", conn, if_exists="replace", index=False)
conn.close()

print("South Asia data saved")