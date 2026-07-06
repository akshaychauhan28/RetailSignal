# RetailSignal
> Retail intelligence that tells you what to do next.

RetailSignal is an end-to-end retail decision intelligence platform built on 100,000+ real Brazilian e-commerce transactions. It answers four core business questions:

- **What happened?** — Revenue trends, category performance, order volume
- **Why did it happen?** — Customer behavior, product ratings, seller analysis
- **What will happen next?** — Churn risk indicators, declining categories
- **What should we do?** — Actionable recommendations for retention and growth

---

## Architecture
Raw CSV Data (Olist)
↓
Python ETL Pipeline (Pandas + SQLAlchemy)
↓
PostgreSQL Data Warehouse (Star Schema)
↓
SQL Analytics Layer
↓
Power BI Dashboard + Recommendation Engine
---

## Tech Stack

| Layer | Technology |
|---|---|
| Data Warehouse | PostgreSQL 18 |
| ETL Pipeline | Python, Pandas, SQLAlchemy |
| Analytics | SQL (CTEs, Window Functions, Aggregations) |
| Dashboard | Power BI |
| Recommendations | Python |

---

## Data Model

**Fact Tables**
- `fact_orders` — 113,425 rows — price, freight, order status
- `fact_payments` — 103,886 rows — payment type, installments, value
- `fact_reviews` — 99,224 rows — review scores

**Dimension Tables**
- `dim_customers` — 99,441 rows
- `dim_products` — 32,951 rows
- `dim_sellers` — 3,095 rows
- `dim_date` — 1,502 rows

---

## Key Insights

- **Top Category** — Health & Beauty generated $1.26M in revenue
- **Peak Month** — November 2017 (Black Friday) hit $1.17M — highest single month
- **Churn Risk** — High value customers identified with 180+ days inactivity
- **Low Rated** — Office Furniture has the lowest avg review score (3.49) despite 1,273 orders

---

## Project Structure
RetailSignal/
├── data/
│   └── raw/          # Olist CSV files (not tracked in git)
├── src/
│   ├── etl.py        # ETL pipeline
│   └── recommendations.py  # Recommendation engine
├── sql/
│   ├── revenue_analysis.sql
│   ├── customer_analysis.sql
│   └── product_analysis.sql
├── dashboard/
│   └── RetailSignal.pbix
├── notebooks/
│   └── exploration.ipynb
└── README.md
---

## Dataset

- **Source** — [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Size** — 100,000+ orders, 9 CSV files
- **Period** — 2016 to 2018