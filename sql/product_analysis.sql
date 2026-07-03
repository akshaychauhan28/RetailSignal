-- Top 10 Best Selling Products by Revenue
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
LIMIT 10;

-- Category Performance Summary
SELECT 
    p.product_category_name_english AS category,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS avg_price,
    AVG(r.review_score) AS avg_review_score
FROM fact_orders f
JOIN dim_products p ON f.product_key = p.product_key
LEFT JOIN fact_reviews r ON f.order_id = r.order_id
WHERE f.price IS NOT NULL
GROUP BY p.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 15;

-- Top 10 Sellers by Revenue
SELECT 
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS avg_order_value
FROM fact_orders f
JOIN dim_sellers s ON f.seller_key = s.seller_key
WHERE f.price IS NOT NULL
GROUP BY s.seller_id, s.seller_city, s.seller_state
ORDER BY total_revenue DESC
LIMIT 10;