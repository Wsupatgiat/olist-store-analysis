SELECT
	s.seller_id,
	s.seller_state,
	SUM(oi.price + oi.freight_value) AS revenue
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id
JOIN orders o ON oi.order_id  = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY s.seller_id, s.seller_state;
