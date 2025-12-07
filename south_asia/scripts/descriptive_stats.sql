
-- South Asia WDI Descriptive Statistics SQL Script
-- Country-level descriptive statistics

SELECT
    country_code,
    ROUND(AVG(gdp_growth),2) AS avg_gdp_growth,
    ROUND(AVG(employment_ratio),2) AS avg_employment_ratio,
    COUNT(*) AS num_observations
FROM south_asia_clean
GROUP BY country_code
ORDER BY country_code;


-- Yearly regional descriptive statistics

SELECT
    year,
    ROUND(AVG(gdp_growth),2) AS avg_gdp_growth,
    ROUND(AVG(employment_ratio),2) AS avg_employment_ratio
FROM south_asia_clean
GROUP BY year
ORDER BY year;