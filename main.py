import pandas as pd
import os

from step_01_extract_data import extract_data
from step_02_transform_data import transform_data
from step_03_load_data import load_data
from step_04_fetch_data_retrive import fetch_data_to_dataframe
from step_05_reporting import generate_reporting



# ==========================================
# MAIN ORCHESTRATION
# ==========================================
def main():
    # Part 1 - ETL
    print("--- PART 1: ETL PROCESS ---")
    # Check if the tables exist before running the ETL process. 
    # This is a simple check to prevent unnecessary processing if the data is already loaded.
    db_path = './db_volume/ebury_datalake.db'

    if not os.path.exists(db_path):
        print(f"Database does not exist at {db_path}. Running ETL process.")
        # Relative paths for the database and JSON file. 
        # This allows the script to be run from any location as long as the relative structure is maintained.
        db_path = f'./db_volume/ebury_datalake.db'
        json_path = f'./data/case_study_json_file.json'
        
        print("Starting ETL process...")
        # Layered approach to ETL: Extract, Transform, Load
        raw_data = extract_data(json_path)
        df_payment, df_partner = transform_data(raw_data)
        load_data(df_payment, df_partner, db_path)
        print("ETL process completed successfully. Database ready for queries!")
    
    else:

        print(f"Database already exists at {db_path}. Skipping ETL process.")
    
    # Part 2 - Querying
    print("--- PART 2: QUERYING RESULTS ---")
    
    payment_data = fetch_data_to_dataframe(db_path, "SELECT * FROM payment")
    partner_data = fetch_data_to_dataframe(db_path, "SELECT * FROM partner")
    
    print(payment_data.info()) # Display the structure of the fetched data
    print(payment_data.head(5)) # Display the first few rows of the fetched data
    print(partner_data.head(5)) # Display the first few rows of the fetched data
    
    # 1. Count the number of transactions from each partner.
    merged_data = pd.merge(payment_data, partner_data, on='partnerId', how='inner')
    transactions_per_partner = merged_data['fullName'].value_counts()
    print("Number of transactions per partner:")
    print(transactions_per_partner)

    # 2. Calculate the minimum and the maximum exchangeRate.
    min_exchange_rate = merged_data['exchangeRate'].min()
    max_exchange_rate = merged_data['exchangeRate'].max()
    print(f"Minimum exchange rate: {min_exchange_rate}")
    print(f"Maximum exchange rate: {max_exchange_rate}")

    # 3. Determine the number of trades per day.
    merged_data['createdAt'] = pd.to_datetime(merged_data['createdAt'])
    trades_per_day = merged_data.groupby(merged_data['createdAt'].dt.date).size()
    print("Number of trades per day:")
    print(trades_per_day)

    # 4. Determine the foreignGrossAmount per currency
    foreign_gross_amount_per_currency = merged_data.groupby('currencyCode')['foreignGrossAmount'].sum()
    print("Foreign gross amount per currency:")
    print(foreign_gross_amount_per_currency)

    # 5. Determine the average cappingRate per currency
    avg_capping_rate_per_currency = merged_data.groupby('currencyCode')['cappingRate'].mean()
    print("Average capping rate per currency:")
    print(avg_capping_rate_per_currency)

    # Generate visual reports
    generate_reporting(
        transactions_per_partner,
        min_exchange_rate,
        max_exchange_rate, 
        trades_per_day, 
        foreign_gross_amount_per_currency, 
        avg_capping_rate_per_currency
        )

    return merged_data, transactions_per_partner, min_exchange_rate, max_exchange_rate, trades_per_day, foreign_gross_amount_per_currency, avg_capping_rate_per_currency


if __name__ == '__main__':
    main()