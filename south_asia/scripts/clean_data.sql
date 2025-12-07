
-- South Asia WDI Data SQL Cleaning Script

-- Remove rows missing key values
CREATE TABLE south_asia_clean AS
SELECT
    country_code,
    country,
    CAST(SUBSTR(year, 3) AS INTEGER) AS year,
    gdp_growth,
    employment_ratio
FROM south_asia
WHERE
    gdp_growth IS NOT NULL
    AND employment_ratio IS NOT NULL;



-- How many years per country?
SELECT country_code, COUNT(*) AS num_years
FROM south_asia_clean
GROUP BY country_code
ORDER BY country_code;

-- Regional yearly averages
SELECT
    year,
    ROUND(AVG(gdp_growth),2) AS avg_gdp_growth,
    ROUND(AVG(employment_ratio),2) AS avg_employment_ratio
FROM south_asia_clean
GROUP BY year
ORDER BY year;