import pandas as pd
import sqlite3
import json
import os
from datetime import datetime

# ==========================================
# 1. DATA CONTRACT
# ==========================================

PAYMENT_SCHEMA = {
    'paymentId': str,
    'partnerId': str,
    'foreignGrossAmount': float,
    'currencyCode': str,
    'date': datetime,
    'createdAt': datetime,
    'updatedAt': datetime,
    'contractNumber': str,
    'cappingRate': float,
    'cancellation': str
}

PARTNER_SCHEMA = {
    'partnerId': str,
    'fullName': str
}

# ==========================================
# 2. EXTRACT (Data Extraction)
# ==========================================
def extract_data(filepath):
    """Reads the JSON file and returns the data as a Python object (list or dict)."""
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# ==========================================
# 3. TRANSFORM (Data Transformation and Cleaning)
# ==========================================
def transform_data(raw_data):
    """Split the raw JSON data into two DataFrames: one for payments and another for partners."""
    payments = []
    partners = []
    
    # The JSON structure can be either a list of records or a single record. We need to handle both cases.
    # This logic ensures correct iteration.
    records = raw_data if isinstance(raw_data, list) else [raw_data]

    for record in records:
        # Takes the "payment" node if it exists and is not empty.
        if 'payment' in record and record['payment']:
            payments.append(record['payment'])
        
        # Takes the "partner" node if it exists and is not empty.
        if 'partner' in record and record['partner']:
            partners.append(record['partner'])
            
    # Convert lists of dictionaries into DataFrames
    df_payment = pd.DataFrame(payments)
    df_partner = pd.DataFrame(partners)
    
    # Data Contract Enforcement: Keep only columns defined in the schema
    # (Avoids issues with extra columns in the JSON that are not part of the contract)
    colunas_payment = list(PAYMENT_SCHEMA.keys())
    colunas_partner = list(PARTNER_SCHEMA.keys())
    
    # Columns intersection: Only keep columns that are defined in the schema and exist in the DataFrame
    df_payment = df_payment[[col for col in colunas_payment if col in df_payment.columns]]
    df_partner = df_partner[[col for col in colunas_partner if col in df_partner.columns]]
    
    # Business Rule Enforcement: Partners cannot be duplicated in the dimension table
    if not df_partner.empty:
        df_partner = df_partner.drop_duplicates(subset=['partnerId'])
        
    return df_payment, df_partner

# ==========================================
# 4. LOAD (Data Loading)
# ==========================================
def load_data(df_payment, df_partner, db_path):
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

# ==========================================
# MAIN ORCHESTRATION
# ==========================================
def main():
    # Relative paths for the database and JSON file. 
    # This allows the script to be run from any location as long as the relative structure is maintained.
    db_path = './db_volume/ebury_datalake.db'
    json_path = './data/payments_case_study_json_file.json'
    
    print("Starting ETL process...")
    
    raw_data = extract_data(json_path)
    df_payment, df_partner = transform_data(raw_data)
    load_data(df_payment, df_partner, db_path)
    
    print("ETL process completed successfully. Database ready for queries!")

if __name__ == '__main__':
    main()