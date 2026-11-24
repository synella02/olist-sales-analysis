

-- Q1. Is monthly revenue growing?
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS month,
    COUNT(DISTINCT o.order_id)                    AS orders,
    ROUND(SUM(p.payment_value), 2)                AS revenue
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;

-- Q2. Which product categories earn the most?
SELECT
    COALESCE(t.product_category_name_english, pr.product_category_name, 'unknown') AS category,
    COUNT(*)                          AS items_sold,
    ROUND(SUM(oi.price), 2)           AS revenue
FROM order_items oi
JOIN products pr ON oi.product_id = pr.product_id
LEFT JOIN category_translation t ON pr.product_category_name = t.product_category_name
GROUP BY category
ORDER BY revenue DESC
LIMIT 10;

-- Q3. Do late deliveries lead to lower review scores?
SELECT
    CASE
        WHEN date(o.order_delivered_customer_date) > date(o.order_estimated_delivery_date)
        THEN 'Late' ELSE 'On time'
    END                           AS delivery_status,
    COUNT(*)                      AS reviews,
    ROUND(AVG(r.review_score), 2) AS avg_review_score
FROM orders o
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY delivery_status;

-- Q4. What share of customers buy more than once?
WITH customer_orders AS (
    SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS order_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.customer_unique_id
)
SELECT
    COUNT(*)                                                 AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)         AS repeat_customers,
    ROUND(100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*), 2)
                                                             AS repeat_rate_pct
FROM customer_orders;

-- Q5. Who are the top 10 sellers by revenue? (window function)
SELECT *
FROM (
    SELECT
        oi.seller_id,
        ROUND(SUM(oi.price), 2)                        AS revenue,
        COUNT(DISTINCT oi.order_id)                    AS orders,
        RANK() OVER (ORDER BY SUM(oi.price) DESC)      AS revenue_rank
    FROM order_items oi
    GROUP BY oi.seller_id
)
WHERE revenue_rank <= 10
ORDER BY revenue_rank;
