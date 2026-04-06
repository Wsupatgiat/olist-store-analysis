import sys
from pathlib import Path
import pandas as pd

# Fix imports
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from data.connection import get_connection

EXPORT_DIR = BASE_DIR / "exports"

def export_all_tables():
	EXPORT_DIR.mkdir(exist_ok=True)

	conn = get_connection()

	try:
		tables = pd.read_sql(
			"SELECT name FROM sqlite_master WHERE type='table';",
			conn
		)

		for table_name in tables['name']:
			print(f"Exporting: {table_name}")

			df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

			output_path = EXPORT_DIR / f"{table_name}.csv"
			df.to_csv(output_path, index=False)

			print(f"→ Saved to {output_path} ({len(df)} rows)")

	finally:
		conn.close()


if __name__ == "__main__":
	export_all_tables()
