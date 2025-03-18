-- TODO: Esta consulta devolverá una tabla con dos columnas: estado_pedido y
-- Cantidad. La primera contendrá las diferentes clases de estado de los pedidos,
-- y la segunda mostrará el total de cada uno.

-- Query: order_status_count.sql
-- Calcula la cantidad de pedidos por estado.

SELECT 
    order_status AS estado_pedido,
    COUNT(*) AS Cantidad
FROM olist_orders
GROUP BY order_status;