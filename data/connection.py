import sqlite3
import sys

def get_connection():
	return sqlite3.connect(f"{sys.path[0]}/data/olist.db")
