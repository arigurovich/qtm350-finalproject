# Project Codebook: Global Analysis of GDP and Employment

## 1. Data Source

All data for this project was retrieved from the World Bank **World Development Indicators (WDI)** database. The data was accessed programmatically using the `wbgapi` Python library.

The analysis focuses on the interaction between economic growth and labor market participation across multiple global regions.

## 2. Variables

The following variables were consistent across all regional analyses:

| Variable Name | Original WDI Code | Definition | Unit | Data Type |
| :--- | :--- | :--- | :--- | :--- |
| **Year** | N/A | The calendar year of observation. Range varies slightly by region (typically 1990–2023). | Year | Integer |
| **GDP Growth** | `NY.GDP.MKTP.KD.ZG` | Annual percentage growth rate of GDP at market prices based on constant local currency. Aggregates are based on constant 2015 U.S. dollars. | % | Float |
| **Employment Ratio** | `SL.EMP.TOTL.SP.ZS` (or `.NE.ZS`) | Employment-to-population ratio is the proportion of a country's population that is employed. Age 15+, Total. | % | Float |
| **Country** | `economy` | The specific country name derived from ISO-3 country codes. | N/A | String |
| **Region** | Derived | The geographic region (e.g., "Europe") used for high-level grouping. | N/A | String |
| **Sub-Region** | Derived | More granular geographic clusters used for specific regional analyses. | N/A | String |

## 3. Region Classifications

### Europe
Countries were aggregated into six sub-regions:
* **Northern Europe:** Denmark, Finland, Iceland, Norway, Sweden, Estonia, Latvia, Lithuania.
* **Southern Europe:** Italy, Greece, Portugal, Croatia, Malta, Cyprus.
* **Eastern Europe:** Russia, Ukraine, Bulgaria, Romania, Moldova, Belarus.
* **Western Europe:** France, Spain, Belgium, Netherlands, Switzerland, Luxembourg.
* **Central Europe:** Germany, Poland, Austria, Hungary, Czechia, Slovakia, Slovenia.
* **British Isles:** United Kingdom, Ireland.

### North America
Analysis focused on the three major economies:
* **Northern:** Canada (CAN)
* **Central:** United States (USA)
* **Southern:** Mexico (MEX)

### Asia
Countries were analyzed in broad geographic blocs, with a specific deep-dive on South Asia:
* **East Asia:** China, Japan, Mongolia, South Korea, North Korea, Macao.
* **Southeast Asia:** Indonesia, Thailand, Vietnam, Malaysia, Singapore, Philippines, Cambodia, Laos, Myanmar, Brunei, Timor-Leste.
* **South Asia:** India, Pakistan, Bangladesh, Sri Lanka, Nepal, Bhutan, Maldives, Afghanistan.
* **Central Asia:** Kazakhstan, Uzbekistan, Kyrgyzstan, Tajikistan, Turkmenistan.
* **West Asia / Middle East:** Saudi Arabia, UAE, Qatar, Bahrain, Oman, Kuwait, Turkey, Israel, Jordan, Lebanon, Iraq, Iran, Yemen, Syria.

### Africa
The analysis focused on a representative sample of major economies across the continent (2000–2023):
* **North Africa:** Algeria (DZA), Egypt (EGY), Morocco (MAR).
* **West Africa:** Ghana (GHA), Nigeria (NGA).
* **East Africa:** Ethiopia (ETH), Kenya (KEN), Tanzania (TZA), Uganda (UGA).
* **Southern Africa:** South Africa (ZAF).

## 4. Entity-Relationship Diagram (ERD)

The database structure is consistent across all regions. The schema links geographic entities (Regions/Countries) to time-series Indicator Data.

```mermaid
erDiagram
    REGION ||--|{ COUNTRY : "contains"
    COUNTRY ||--|{ INDICATOR_DATA : "has"

    REGION {
        string region_name PK "e.g., Europe, South Asia"
        string sub_region  "e.g., Northern Europe"
    }

    COUNTRY {
        string country_code PK "ISO-3 (e.g., DEU, NGA)"
        string country_name "e.g., Germany, Nigeria"
    }

    INDICATOR_DATA {
        string country_code FK
        int year PK
        float gdp_growth
        float employment_ratio
    }
