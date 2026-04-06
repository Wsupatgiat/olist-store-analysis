"""
upload_to_db.py

Runs the filter pipeline from filter_data.py and uploads the resulting
DataFrames into olist.db via SQLite.

Usage (from project root):
	python scripts/upload_to_db.py

Output:
	data/olist.db — SQLite database with 5 filtered tables:
		orders, order_items, sellers, products, category_translation
"""

import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from filter_data import (
	orders_filtered,
	order_items_filtered,
	sellers,
	products_filtered,
	cat_trans_filled,
)

# --- DB path ---
ROOT = Path(__file__).parent.parent
DB_PATH = Path(f"{ROOT}/data/olist.db")

TABLES = {
	"orders": orders_filtered,
	"order_items": order_items_filtered,
	"sellers": sellers,
	"products": products_filtered,
	"category_translation": cat_trans_filled,
}

conn = sqlite3.connect(DB_PATH)

print(f"Writing to {DB_PATH}\n")
for table_name, df in TABLES.items():
	df.to_sql(table_name, conn, if_exists="replace", index=False)
	print(f"  {table_name:<25} {len(df):>7,} rows written")

# --- Verify via SQL ---
print("\n=== Verification (SQL row counts) ===")
sql_path = Path(f"{ROOT}/sql/upload_filtered.sql")
with open(sql_path) as f:
	sql = "\n".join(
		line for line in f
		if not line.strip().startswith("--") and line.strip()
	)

cursor = conn.execute(sql)
for row in cursor.fetchall():
	print(f"  {row[0]:<25} {row[1]:>7,}")

conn.close()
print("\nDone.")
