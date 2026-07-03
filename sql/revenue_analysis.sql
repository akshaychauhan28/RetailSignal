-- Monthly Revenue Trend
SELECT 
    d.year,
    d.month,
    d.month_name,
    SUM(f.price + f.freight_value) AS total_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders,
    AVG(f.price + f.freight_value) AS avg_order_value
FROM fact_orders f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- Revenue by Category
SELECT 
    p.product_category_name_english AS category,
    SUM(f.price) AS total_revenue,
    COUNT(DISTINCT f.order_id) AS total_orders,
    AVG(f.price) AS avg_price
FROM fact_orders f
JOIN dim_products p ON f.product_key = p.product_key
GROUP BY p.product_category_name_english
ORDER BY total_revenue DESC;

-- Top 10 Revenue Days
SELECT 
    d.full_date,
    d.month_name,
    d.year,
    SUM(f.price + f.freight_value) AS total_revenue
FROM fact_orders f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.price IS NOT NULL
GROUP BY d.full_date, d.month_name, d.year
ORDER BY total_revenue DESC
LIMIT 10;