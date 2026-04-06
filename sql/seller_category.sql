SELECT
	oi.seller_id,
	s.seller_state,
	ct.product_category_name_english AS category,
	oi.price + oi.freight_value AS revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN category_translation ct ON p.product_category_name = ct.product_category_name
JOIN sellers s ON oi.seller_id = s.seller_id
WHERE o.order_status = 'delivered';
