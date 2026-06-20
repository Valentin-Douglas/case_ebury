import pandas as pd
import sqlite3

def fetch_data_to_dataframe(db_path: str, query: str) -> pd.DataFrame:
    """
    Connects to the SQLite database, executes a SQL query, 
    and returns the result as a Pandas DataFrame.
    
    Args:
        db_path (str): The path to the SQLite database file.
        query (str): The SQL query to be executed.
        
    Returns:
        pd.DataFrame: A dataframe containing the query results.
    """
    try:
        # Establish connection to the database mapped in the Docker volume
        conn = sqlite3.connect(db_path)
        
        # Read the SQL query directly into a Pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        return df
        
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return pd.DataFrame() # Returns an empty DataFrame on failure
        
    finally:
        # Ensures the connection is always closed to prevent database locks
        if 'conn' in locals() and conn:
            conn.close()