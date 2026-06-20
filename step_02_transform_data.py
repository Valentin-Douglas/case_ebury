import pandas as pd
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
    'exchangeRate': float,
    'cancellation': str
}

PARTNER_SCHEMA = {
    'partnerId': str,
    'fullName': str
}



# ==========================================
# 2. TRANSFORM (Data Transformation and Cleaning)
# ==========================================
def transform_data(raw_data=None):
    """Split the raw JSON data into two DataFrames: one for payments and another for partners."""
    payments = []
    partners = []
    
    # The JSON structure can be either a list of records or a single record. We need to handle both cases.
    # This logic ensures correct iteration.
    records = raw_data if isinstance(raw_data, list) else [raw_data]

    for record in records:
        if 'payment' in record and record['payment']:
            payment_node = record['payment']
            
            # --- DATA FLATTENING LOGIC ---
            # Safely extract the nested cappingRate and create a root-level key for it
            if 'contractInfo' in payment_node and isinstance(payment_node['contractInfo'], dict):
                payment_node['cappingRate'] = payment_node['contractInfo'].get('cappingRate')
            # -----------------------------
            
            payments.append(payment_node)
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
