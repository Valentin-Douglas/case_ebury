from step_03_02_smart_load import execute_smart_load

# ==========================================
# 3. LOAD ORCHESTRATOR
# ==========================================
def load_data(df_payment=None, df_partner=None, db_path=None):
    """Orchestrates the Smart Load process for all ETL tables."""
    print("Starting smart validation and data loading...")
    
    execute_smart_load(df_payment, 'Payment', 'paymentId', db_path)
    execute_smart_load(df_partner, 'Partner', 'partnerId', db_path)
    
    print("Data loading phase completed successfully.")