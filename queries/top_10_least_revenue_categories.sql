-- TODO: Esta consulta devolverá una tabla con las 10 categorías con menores ingresos
-- (en inglés), el número de pedidos y sus ingresos totales. La primera columna será
-- Category, que contendrá las 10 categorías con menores ingresos; la segunda será
-- Num_order, con el total de pedidos de cada categoría; y la última será Revenue,
-- con el ingreso total de cada categoría.
-- PISTA: Todos los pedidos deben tener un estado 'delivered' y tanto la categoría
-- como la fecha real de entrega no deben ser nulas.

-- Query: top_10_least_revenue_categories.sql
-- Obtiene las 10 categorías con menores ingresos.

SELECT 
    p.product_category_name AS Category,
    COUNT(o.order_id) AS Num_order,
    SUM(pay.payment_value) AS Revenue
FROM olist_orders o
JOIN olist_order_items oi ON o.order_id = oi.order_id
JOIN olist_products p ON oi.product_id = p.product_id
JOIN olist_order_payments pay ON o.order_id = pay.order_id
WHERE o.order_status = 'delivered'
    AND p.product_category_name IS NOT NULL
    AND o.order_delivered_customer_date IS NOT NULL
GROUP BY p.product_category_name
ORDER BY Revenue ASC
LIMIT 10;