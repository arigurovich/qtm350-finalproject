# QTM 350 Final Project: Global Analysis of GDP Growth and Employment Ratios

## Project Overview

This project presents a comprehensive analysis of the relationship between GDP growth and employment-to-population ratios across four major global regions: Europe, Asia, North America, and Africa. The analysis spans from 1990 to 2023 using data from the World Bank's World Development Indicators (WDI) database.

## Reports

The comprehensive report is available in two formats:

1. **PDF Report**: [regional_analysis_report.pdf](regional_analysis_report.pdf)
2. **HTML Report**: [regional_analysis_report.html](regional_analysis_report.html)

The HTML report includes all figures embedded and will display correctly on GitHub when you view the file.

## Project Structure

```
qtm350-finalproject/
├── data/                           # Data files
│   ├── south_asia_data.csv        # South Asia dataset
│   ├── overall_wdi.db             # Overall WDI database
│   └── data_africa.db             # Africa regional database
├── scripts/                        # Analysis scripts
│   ├── europe_project_analysis.py
│   ├── europe_region_comparison.py
│   ├── analysis_asia.py
│   ├── region_asia.py
│   ├── south_asia_*.py
│   ├── North_America_Analysis.ipynb
│   └── analysis-africa.ipynb
├── figures/                        # Generated visualizations
│   ├── europe_*.png
│   ├── asia_*.png
│   ├── south_asia_*.png
│   ├── NA_*.png
│   └── africa-*.png
├── documentation/                  # Project documentation
│   └── codebook.md                # Data dictionary and ERD
├── regional_analysis_report.qmd   # Quarto source file
├── regional_analysis_report.pdf   # PDF output
├── regional_analysis_report.html  # HTML output (GitHub-compatible)
└── README.md                      # This file
```

## Data Sources

All data was retrieved from the **World Bank World Development Indicators (WDI)** database using the `wbgapi` Python library.

### Key Indicators:
- **GDP Growth**: Annual % growth rate (NY.GDP.MKTP.KD.ZG)
- **Employment Ratio**: Employment-to-population ratio, ages 15+ (SL.EMP.TOTL.SP.ZS)

### Regions Analyzed:
- **Europe**: 6 sub-regions across Europe & Central Asia
- **Asia**: East Asia & Pacific with deep dive into South Asia
- **North America**: USA, Canada, Mexico
- **Africa**: 10 major economies across all sub-regions

## Reproducibility

### Prerequisites

To reproduce the analysis, you need:

```bash
# Python packages
pip install wbgapi pandas numpy matplotlib seaborn sqlite3 duckdb

# Quarto (for rendering the report)
# Install from https://quarto.org/docs/get-started/
```

### Running the Analysis

1. Clone this repository
2. Run the regional analysis scripts (if you want to regenerate the data and figures):
   ```bash
   # Europe analysis
   python scripts/europe_project_analysis.py
   python scripts/europe_region_comparison.py

   # Asia analysis
   python scripts/analysis_asia.py
   python scripts/region_asia.py

   # South Asia analysis
   python scripts/south_asia_get_data.py
   python scripts/south_asia_trends.py
   python scripts/south_asia_relationships.py
   python scripts/south_asia_combined_trend.py

   # North America analysis
   jupyter notebook scripts/North_America_Analysis.ipynb

   # Africa analysis
   jupyter notebook scripts/analysis-africa.ipynb
   ```

3. Render the Quarto report:
   ```bash
   # Generate PDF
   quarto render regional_analysis_report.qmd --to pdf

   # Generate HTML (with embedded figures)
   quarto render regional_analysis_report.qmd --to html
   ```

## Documentation

- [Codebook](documentation/codebook.md): Detailed data dictionary, variable definitions, and Entity-Relationship Diagram (ERD)