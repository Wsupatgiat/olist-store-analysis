# Olist E-Commerce Analysis

Dataset: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
___

## Business Overview: Olist
Olist is the largest online retail marketplace in Brazil. It connects small and medium merchants to customers across the country, handling logistics and payments under a single contract. Sellers list products on the Olist platform and ship directly to customers using Olist's logistics partners.

The dataset covers orders placed between 2016 and 2018, including order details, product information, seller locations, payments, and customer reviews.

## Scope
This analysis focuses on the seller and revenue side of the business
- The relationship between states, product category, and revenue contribution
- How categories relate to seller's performance

The analysis covers 2017 to 2018. Data from 2016 is excluded because data count in that year is sparse and inconsistent, which could affect the analysis.
___

## Process
### 1. Data Profiling and Cleaning
Before any analysis, the raw data is profiled and cleaned:
- 610 products had missing category and dimension data and were excluded.
- Orders outside 2017-2018 were removed as the data count is too low to perform analysis on. Data distribution follows irregular patterns as well and do not reflect current business operations,
- 2 product categories do not have English translation (in the product category name translation table). The translations were added manually.

After cleaning, 99.7% of orders and order items were retained. The cleaning had minimal impact on coverage.

Details are shown in ``data_profiling.ipynb``

### 2. Exploratory Data Analysis
Four areas were analyzed:

- How total revenue and order count changed month by month across 2017-2018: ``monthly_orders_analysis.ipynb``
- Which Brazilian states generate the most revenue: ``state_revenue_analysis.ipynb``
- Which product categories drive the most revenue: ``category_revenue_analysis.ipynb``
- How the number of categories a seller operates in relates to their revenue: ``category_revenue_analysis.ipynb``
___

## Key Findings
### Overall Company Growth Trends
``monthly_orders_analysis.ipynb``
1. Revenue and order count grew consistently from 2017 into 2018. However, the average revenue per item stayed flat throughout the entire period. The business is growing because more orders are being placed, not because individual transactions are becoming more valuable.
2. Average revenue per item shows a strong seasonal pattern. Increasing and dropping off every 6 months. Seasonality patterns for amount of orders or total revenue can't be confirmed due to low amounts of data points (only 20 months). If we assume that there is no seasonality component in the amount of orders and total revenue, this could mean that people order less when the average price of each order increases, but when they make orders they are willing to spend more.
3. There is no increasing or decreasing trends on average revenue per order.
4. Different states and categories contribution to the overall revenue are consistent over time.

### State and Revenue
Sou Paulo (SP) accounts for 65% of total revenue, while the share of revenue contributions for other states are significantly lower. There is no statistical significance between how much the other states than SP contribute to the revenue as well (as confirmed by Kruskal-Wallis test).

### Category and Revenue
50% of total revenue are accounted by only 7 categories.
- Health and beauty
- Watches and gifts
- Bed/bath/table
- Sports and leasure
- Computers and accessories
- Furniture and decor
- Housewares

The trends of all these categories has been stable overtime, with no particular category exhibiting any significant chaneges over the other ones. Unlike states, different categories do have statistical significance in revenue contribution (as confirmed by Kruskal-Wallis test).

### Amount of Different Categories sold by a seller
Better performing sellers can be due to 2 factors
1. Sellers who focus on a small number of categories tend to perform better than ones with no specialization.
2. Sellers who spread across many categories can perform better as well, but this is due to the amount of items sold, and not becuase of focusing on multiple categories.

___
## Recommendations
1. Dependency on Sao Paulo should be reduced, as any changes in this state could affect the overall revenue significantly. Other states with lower revenue generation could be promoted more.
2. Business operations could be planned around seasonality of average revenue per order. Promotion on lower costing items could be done to offset the drop-off periods.
3. Dependency on the 7 top categories should be reduced. Promoting other categories more could help this.
4. Build 2 seller programs. One for sellers with a focused category, and one for miscellaneous sellers.

___
## Tools Used
- **Python** (pandas, numpy, matplotlib, seaborn, scipy, statsmodels)
- **SQL**

## Project Structure
- ``raw_data``: Original CSVs from Kaggle
- ``data``: SQLite database (olist.db) and DB connection helper
- ``scripts``: ETL pipeline: cleaning, upload to DB, CSV export
- ``sql``: SQL queries used in analysis
- ``exports``: Cleaned CSVs used by notebooks
- ``notebooks``: Analysis notebooks (data profiling, time series, state, category)
- ``utils``: Shared plotting and loading utilities
