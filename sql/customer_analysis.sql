-- Top 10 Customers by Revenue
SELECT 
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.price + f.freight_value) AS total_spent,
    AVG(f.price + f.freight_value) AS avg_order_value
FROM fact_orders f
JOIN dim_customers c ON f.customer_key = c.customer_key
GROUP BY c.customer_unique_id, c.customer_city, c.customer_state
ORDER BY total_spent DESC
LIMIT 10;

-- RFM Segmentation
SELECT
    c.customer_unique_id,
    MAX(d.full_date) AS last_purchase_date,
    COUNT(DISTINCT f.order_id) AS frequency,
    SUM(f.price + f.freight_value) AS monetary,
    CURRENT_DATE - MAX(d.full_date) AS days_since_last_purchase
FROM fact_orders f
JOIN dim_customers c ON f.customer_key = c.customer_key
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY c.customer_unique_id
ORDER BY days_since_last_purchase ASC
LIMIT 20;

-- Churn Risk Customers (no purchase in last 180 days)
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
GROUP BY c.customer_unique_id, c.customer_state
HAVING CURRENT_DATE - MAX(d.full_date) > 180
ORDER BY total_spent DESC
LIMIT 20;