import pandas as pd
import os

def clean_data():
    print("Starting data cleaning pipeline...")
    input_path = '../data/synthetic/gig_transactions.csv'
    output_path = '../data/processed/transactions_clean.csv'
    
    # Check if the synthetic data exists
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}. Did you run generate_transactions.py?")
        return

    # Load data
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} raw transactions.")
    
    # 1. Remove null rows
    initial_len = len(df)
    df = df.dropna()
    print(f"Removed {initial_len - len(df)} null rows.")
    
    # 2. Normalize timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 3. Convert amounts to float (decimals)
    df['amount'] = df['amount'].astype(float)
    
    # 4. Encode direction (Machine Learning prefers numbers: CREDIT = 1, DEBIT = 0)
    df['direction_encoded'] = df['direction'].map({'CREDIT': 1, 'DEBIT': 0})
    
    # 5. Categorize transaction description (Ensuring they are treated as categorical data)
    df['category'] = df['category'].astype(str).str.strip().str.title()
    
    # Ensure processed directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"Data cleaning complete! Saved {len(df)} clean transactions to {output_path}")

if __name__ == "__main__":
    clean_data()