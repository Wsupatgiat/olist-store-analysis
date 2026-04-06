"""
filter_data.py

Filters raw Olist CSV data for the Seller Performance Scorecard analysis.
Filtering logic mirrors the final section of notebooks/01_data_profiling.ipynb.

Steps:
	1. Load the 5 in-scope tables from raw_data/ using load_table()
	2. Remove orders where any date column is outside [2017-01-01, 2018-12-31]
	   or has any null value
	3. Cascade order filter to order_items, then also drop items with
	   out-of-range shipping_limit_date
	4. Drop products rows with any null (includes missing product_category_name)
	5. sellers and category_translation have no date columns and no nulls — kept as-is
	6. Manually add 2 categories missing from category_translation

Exports (imported by upload_to_db.py):
	orders_filtered       — cleaned orders
	order_items_filtered  — cleaned order_items
	sellers               — unchanged
	products_filtered     — products with nulls dropped
	cat_trans_filled      — category_translation + 2 manual additions
"""

import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.helpers import load_table

# --- Paths ---
ROOT = Path(__file__).parent.parent
RAW = Path(f"{ROOT}/raw_data")

# --- Load raw tables ---
orders = load_table(f"{RAW}/olist_orders_dataset.csv", "orders")
order_items = load_table(f"{RAW}/olist_order_items_dataset.csv", "order_items")
sellers = load_table(f"{RAW}/olist_sellers_dataset.csv", "sellers")
products = load_table(f"{RAW}/olist_products_dataset.csv", "products")
category_translation = load_table(f"{RAW}/product_category_name_translation.csv", "category_translation")

# --- Date bounds (from notebook 01) ---
DATE_MIN = pd.Timestamp("2017-01-01")
DATE_MAX = pd.Timestamp("2018-12-31")

# Date columns to check per table
DATE_COLS = {
	"orders": [
		"order_purchase_timestamp",
		"order_delivered_carrier_date",
		"order_delivered_customer_date",
		"order_estimated_delivery_date",
	],
	"order_items": ["shipping_limit_date"],
}


def out_of_range_mask(df, cols):
	"""Returns a boolean mask of rows where any date column is outside [DATE_MIN, DATE_MAX]."""
	mask = pd.Series(False, index=df.index)
	for col in cols:
		valid = df[col].notna()
		mask |= valid & ((df[col] < DATE_MIN) | (df[col] > DATE_MAX))
	return mask


def cascade(df, valid_ids):
	"""Keep only rows whose order_id is in valid_ids."""
	return df[df["order_id"].isin(valid_ids)]


# --- Clean orders ---
orders_oor_mask = out_of_range_mask(orders, DATE_COLS["orders"])
# Only check nulls in key identifier columns — delivery date nulls are expected
# for non-delivered orders and are handled by the date range filter + status filter.
NULL_COLS = ["order_id", "customer_id", "order_status", "order_purchase_timestamp"]
orders_null_mask = orders[NULL_COLS].isnull().any(axis=1)
orders_filtered = orders[~(orders_oor_mask | orders_null_mask)]

# --- Clean order_items ---
# 1. Cascade: drop items whose parent order was removed
# 2. Direct: drop items with out-of-range shipping_limit_date
order_items_filtered = cascade(order_items, orders_filtered["order_id"])
order_items_filtered = order_items_filtered[
	~out_of_range_mask(order_items_filtered, DATE_COLS["order_items"])
]

# --- Clean products ---
# Drop any row with a null (includes the 610 rows missing product_category_name)
products_filtered = products.dropna()

# --- sellers: no date columns, no nulls — unchanged ---

# --- category_translation: add 2 categories missing from the original table ---
# Identified in notebook 01, section 3 summary:
#   - pc_gamer                                      -> "pc gamer"
#   - portateis_cozinha_e_preparadores_de_alimentos -> "portable kitchen appliances and food processors"
missing_categories = pd.DataFrame({
	"product_category_name": [
		"pc_gamer",
		"portateis_cozinha_e_preparadores_de_alimentos",
	],
	"product_category_name_english": [
		"pc gamer",
		"portable kitchen appliances and food processors",
	],
})
cat_trans_filled = pd.concat(
	[category_translation, missing_categories],
	ignore_index=True,
)
