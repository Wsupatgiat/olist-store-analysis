import pandas as pd

# Column dtypes per table.
# Datetime columns are listed under the key "datetime" and passed to parse_dates in read_csv.
# All other columns are passed to dtype=.
TABLE_DTYPES = {
	"customers": {
		"customer_id": str,
		"customer_unique_id": str,
		"customer_zip_code_prefix": str,
		"customer_city": str,
		"customer_state": str,
	},
	"geolocation": {
		"geolocation_zip_code_prefix": str,
		"geolocation_lat": float,
		"geolocation_lng": float,
		"geolocation_city": str,
		"geolocation_state": str,
	},

	# USED
	"order_items": {
		"order_id": str,
		"order_item_id": int,
		"product_id": str,
		"seller_id": str,
		"shipping_limit_date": "datetime",
		"price": float,
		"freight_value": float,
	},
	"order_payments": {
		"order_id": str,
		"payment_sequential": int,
		"payment_type": str,
		"payment_installments": int,
		"payment_value": float,
	},
	"order_reviews": {
		"review_id": str,
		"order_id": str,
		"review_score": int,
		"review_comment_title": str,
		"review_comment_message": str,
		"review_creation_date": "datetime",
		"review_answer_timestamp": "datetime",
	},

	# USED
	"orders": {
		"order_id": str,
		"customer_id": str,
		"order_status": str,
		"order_purchase_timestamp": "datetime",
		"order_approved_at": "datetime",
		"order_delivered_carrier_date": "datetime",
		"order_delivered_customer_date": "datetime",
		"order_estimated_delivery_date": "datetime",
	},

	# USED
	"products": {
		"product_id": str,
		"product_category_name": str,
		"product_name_lenght": "Int64",
		"product_description_lenght": "Int64",
		"product_photos_qty": "Int64",
		"product_weight_g": float,
		"product_length_cm": float,
		"product_height_cm": float,
		"product_width_cm": float,
	},

	# USED
	"sellers": {
		"seller_id": str,
		"seller_zip_code_prefix": str,
		"seller_city": str,
		"seller_state": str,
	},

	# USED
	"category_translation": {
		"product_category_name": str,
		"product_category_name_english": str,
	},
}


def check_pk_duplicates(df, pk_cols):
	"""Returns the number of duplicate rows for the given primary key columns."""
	return df.duplicated(subset=pk_cols).sum()


def load_table(path, table_name):
	"""Load a CSV with dtypes and datetime parsing applied at load time."""
	col_map = TABLE_DTYPES[table_name]
	dtype = {col: t for col, t in col_map.items() if t != "datetime"}
	parse_dates = [col for col, t in col_map.items() if t == "datetime"]
	return pd.read_csv(path, dtype=dtype, parse_dates=parse_dates)
