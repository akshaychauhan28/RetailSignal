import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:password123@localhost:5432/retailsignal"
engine = create_engine(DATABASE_URL)

def get_churn_risk_customers(days_inactive=180, limit=20):
    query = """
        SELECT
            c.customer_unique_id,
            c.customer_state,
            MAX(d.full_date) AS last_purchase_date,
            COUNT(DISTINCT f.order_id) AS total_orders,
            SUM(f.price + f.freight_value) AS total_spent,
            CURRENT_DATE - MAX(d.full_date) AS days_inactive
        FROM fact_orders f
        JOIN dim_customers c ON f.customer_key = c.customer_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE f.price IS NOT NULL
        GROUP BY c.customer_unique_id, c.customer_state
        HAVING CURRENT_DATE - MAX(d.full_date) > %(days_inactive)s
        ORDER BY total_spent DESC
        LIMIT %(limit)s
    """
    return pd.read_sql(query, engine, params={'days_inactive': days_inactive, 'limit': limit})

def get_top_products(limit=10):
    query = """
        SELECT
            p.product_id,
            p.product_category_name_english AS category,
            COUNT(DISTINCT f.order_id) AS total_orders,
            SUM(f.price) AS total_revenue,
            AVG(f.price) AS avg_price
        FROM fact_orders f
        JOIN dim_products p ON f.product_key = p.product_key
        WHERE f.price IS NOT NULL
        GROUP BY p.product_id, p.product_category_name_english
        ORDER BY total_revenue DESC
        LIMIT %(limit)s
    """
    return pd.read_sql(query, engine, params={'limit': limit})

def get_low_rated_categories(min_orders=100):
    query = """
        SELECT
            p.product_category_name_english AS category,
            AVG(r.review_score) AS avg_review_score,
            COUNT(DISTINCT f.order_id) AS total_orders
        FROM fact_orders f
        JOIN dim_products p ON f.product_key = p.product_key
        LEFT JOIN fact_reviews r ON f.order_id = r.order_id
        WHERE f.price IS NOT NULL
        GROUP BY p.product_category_name_english
        HAVING COUNT(DISTINCT f.order_id) > %(min_orders)s
        ORDER BY avg_review_score ASC
        LIMIT 10
    """
    return pd.read_sql(query, engine, params={'min_orders': min_orders})

if __name__ == "__main__":
    print("=== CHURN RISK CUSTOMERS ===")
    print(get_churn_risk_customers())
    
    print("\n=== TOP PRODUCTS ===")
    print(get_top_products())
    
    print("\n=== LOW RATED CATEGORIES ===")
    print(get_low_rated_categories())