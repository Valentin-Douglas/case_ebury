import sqlite3
import pandas as pd
from step_03_01_dt_utils import check_table_exists, get_existing_ids

# ==========================================
# SMART GENERIC LOADER
# ==========================================
def execute_smart_load(df: pd.DataFrame, table_name: str, id_column: str, db_path: str):
    """
    Executes the decision tree for data loading:
    1. If table doesn't exist -> Create (Overwrite)
    2. If table exists and data has new rows -> Append new rows
    3. If table exists and all data is already there -> Overwrite (Replace)
    """
    if df is None or df.empty:
        print(f"[{table_name}] No incoming data. Skipping process.")
        return

    # SQLite creates the database file automatically on connect if it doesn't exist
    conn = sqlite3.connect(db_path)

    # Scenario 1: Table does not exist
    if not check_table_exists(conn, table_name):
        print(f"[{table_name}] Table not found. Creating and loading new data...")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        return

    # Scenarios 2 & 3: Table exists, let's validate the data
    existing_ids = get_existing_ids(conn, table_name, id_column)
    
    # Filter to find strictly new records
    df_new_records = df[~df[id_column].isin(existing_ids)]

    if df_new_records.empty:
        # Scenario 2: No new records found (The data is the exact same)
        print(f"[{table_name}] Data is identical to existing records. Performing full Overwrite...")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    else:
        # Scenario 3: New records found. We append ONLY the new ones.
        print(f"[{table_name}] Found {len(df_new_records)} new records. Appending to database...")
        df_new_records.to_sql(table_name, conn, if_exists='append', index=False)

    conn.close()
    return None