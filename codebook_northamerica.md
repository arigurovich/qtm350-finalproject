# Codebook: North America Region Analysis

## Data Source
All data was retrieved from the World Bank World Development Indicators (WDI) API using the `wbgapi` Python library. The following indicators were used:

- **NY.GDP.MKTP.KD.ZG** – GDP growth (annual %)
- **SL.EMP.TOTL.SP.NE.ZS** – Employment-to-population ratio, 15+ (national estimate, %)

The analysis covers the period **1990–2023** (inclusive).

## Region Classifications
Countries were aggregated into the following North American sub-regions for analysis:

**Northern North America**: Canada (CAN)  
**Central North America**: United States of America (USA)  
**Southern North America**: Mexico (MEX)

These sub-regions are used to compute regional averages (e.g., average GDP growth by sub-region over time).

## Entity-Relationship Diagram

```mermaid
erDiagram
    COUNTRY ||--|{ INDICATOR_DATA : "has"
    REGION  ||--|{ COUNTRY        : "contains"

    REGION {
        string region_name PK "e.g., Northern North America"
    }

    COUNTRY {
        string country_code PK "ISO-3 (e.g., USA)"
        string country_name  "e.g., United States of America"
        string region_name FK
    }

    INDICATOR_DATA {
        string country_code FK
        int    year PK       "e.g., 1995"
        float  gdp_growth    "NY.GDP.MKTP.KD.ZG"
        float  employment_ratio "SL.EMP.TOTL.SP.NE.ZS"
    }
