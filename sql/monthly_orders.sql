SELECT
	o.order_purchase_timestamp,
	oi.order_id,
	oi.seller_id,
	s.seller_state AS state,
	ct.product_category_name_english  AS category,
	oi.price + oi.freight_value AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN sellers s  ON oi.seller_id = s.seller_id
JOIN products p ON oi.product_id = p.product_id
JOIN category_translation ct ON p.product_category_name = ct.product_category_name
WHERE o.order_status = 'delivered';
