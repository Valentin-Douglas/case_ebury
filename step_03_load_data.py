import sqlite3

# ==========================================
# 1. LOAD (Data Loading)
# ==========================================
def load_data(df_payment=None, df_partner=None, db_path=None):
    """Saves the DataFrames as tables in the SQLite database."""
    conn = sqlite3.connect(db_path)
    
    # if_exists='replace' assures that we overwrite the tables if they already exist.
    # Which is useful for development and testing.
    if not df_payment.empty:
        df_payment.to_sql('Payment', conn, if_exists='replace', index=False)
        print(f"Payment table created with {len(df_payment)} rows.")
        
    if not df_partner.empty:
        df_partner.to_sql('Partner', conn, if_exists='replace', index=False)
        print(f"Partner table created with {len(df_partner)} rows.")
        
    conn.close()
