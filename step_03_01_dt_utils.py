import sqlite3
import pandas as pd

# ==========================================
# DATABASE UTILITIES (SRP Compliant)
# ==========================================

def check_table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    """Checks if a specific table exists in the SQLite database."""
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    result = pd.read_sql_query(query, conn)
    return not result.empty

def get_existing_ids(conn: sqlite3.Connection, table_name: str, id_column: str) -> list:
    """Fetches existing IDs from the database. Returns empty list if table doesn't exist."""
    if not check_table_exists(conn, table_name):
        return []
        
    try:
        query = f"SELECT {id_column} FROM {table_name}"
        existing_ids = pd.read_sql_query(query, conn)[id_column].tolist()
        return existing_ids
    except Exception as e:
        print(f"Validation Note: Could not fetch IDs for '{table_name}'. Detail: {e}")
        return []