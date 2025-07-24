# Retail Fashion Market Analysis Project

This project focuses on processing, analyzing, and comparing clothing data from multiple retailers (Jumia and PLT) to identify market opportunities and provide strategic recommendations for product assortment and pricing strategies.

## Project Overview

The analysis is divided into three main components:

1. **Jumia Data Analysis**: Processing and analyzing clothing products from Jumia across various categories
2. **PLT Data Analysis**: Processing and analyzing PrettyLittleThing (PLT) clothing products
3. **Retailer Comparison**: Comparing both retailers to identify market opportunities

## Directory Structure

- `Jumia Data/`: Contains Jumia product data files and analysis
  - `raw/`: Original CSV files for different product categories
  - `processed/`: Cleaned and standardized data
  - `analysis/`: Visualization outputs and summary reports

- `PLT Data/`: Contains PLT clothing data files and analysis
  - `PLT_clothing.csv`: Main clothing dataset
  - `PLT_new_in.csv`: New arrivals dataset
  - `PLT_sale_final.csv`: Sale items with discount information
  - `processed/`: Cleaned and standardized data
  - `analysis/`: Visualization outputs and summary reports

- `retailer_comparison/`: Outputs from the comparison between retailers
  - Price analysis files
  - Category distribution comparisons
  - Market opportunity reports

- `*.py`: Python scripts for data processing and analysis

## Key Scripts

1. **Jumia Data Processing**
   - `preprocess_jumia_data.py`: Cleans, standardizes, and combines Jumia product data
   - `analyze_jumia_data.py`: Creates visualizations and analyses of Jumia products

2. **PLT Data Processing**
   - `preprocess_plt_data.py`: Processes PLT clothing data with standardization and feature extraction
   - `analyze_plt_data.py`: Generates insights and visualizations for PLT products

3. **Comparison Analysis**
   - `compare_plt_jumia.py`: Compares retailers on price, category distribution, and size offerings

## Key Findings

### Jumia Product Analysis
- 2,371 total products across 5 clothing categories
- Average price: 14,859.91 NGN
- Balanced distribution among categories (Jeans, Tops, Skirts, Dresses, Jumpsuits)
- Most products offer multiple size options

### PLT Product Analysis
- 622 total products across 12 categories
- Average price: 50,664.37 NGN
- Top categories: Activewear (23.2%), Dresses (17.2%), Co-ords (15.4%)
- Higher price point positioning compared to Jumia

### Retailer Comparison Insights
- PLT products are priced 240.9% higher than Jumia products
- Major market opportunities in Jeans, Tops, and Skirts categories
- PLT has significantly fewer products but with higher price points
- Strategic recommendations include:
  - Expanding product offerings in underrepresented categories
  - Ensuring premium pricing is supported by quality and branding
  - Targeted promotions in high-opportunity categories
  - Emphasis on product quality and style differentiation

## Getting Started

### Prerequisites
- Python 3.6+
- pandas
- matplotlib
- seaborn
- numpy

### Running the Analysis

1. Clone this repository
2. Run the preprocessing scripts:
   ```
   python preprocess_jumia_data.py
   python preprocess_plt_data.py
   ```
3. Run the analysis scripts:
   ```
   python analyze_jumia_data.py
   python analyze_plt_data.py
   ```
4. Run the comparison analysis:
   ```
   python compare_plt_jumia.py
   ```

5. Check the output directories for visualizations and reports:
   - `Jumia Data/analysis/`
   - `PLT Data/analysis/`
   - `retailer_comparison/`

## Methodology

The analysis followed a structured approach:
1. Data inspection and cleaning
2. Standardization of fields and formats
3. Feature extraction (sizes, materials, categories)
4. Statistical analysis of product distributions
5. Price and category analysis across retailers
6. Opportunity identification through gap analysis
7. Development of strategic recommendations

## Future Work

- Incorporate sales data to measure actual demand
- Add more retailers for broader market analysis
- Implement time-series analysis for seasonal trends
- Develop predictive models for optimal pricing strategies 