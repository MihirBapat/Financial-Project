import pandas as pd
import numpy as np
import os

def engineer_features():
    print("Starting Feature Engineering...")
    
    # Paths assuming we run from the main project folder
    input_path = 'data/processed/transactions_clean.csv'
    output_path = 'data/processed/features.csv'
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}. Make sure you are running from the main project folder.")
        return

    # Load cleaned data
    df = pd.read_csv(input_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    features = []
    
    # Group by borrower to calculate features for each person
    grouped = df.groupby('borrower_id')
    total_borrowers = len(grouped)
    count = 0
    
    for borrower_id, group in grouped:
        # Separate credits (income) and debits (expenses)
        credits = group[group['direction_encoded'] == 1].copy()
        debits = group[group['direction_encoded'] == 0].copy()
        
        # Monthly grouping using 'ME' (Month-End) for Pandas 3.0+
        credits.set_index('timestamp', inplace=True)
        debits.set_index('timestamp', inplace=True)
        
        monthly_income = credits['amount'].resample('ME').sum()
        monthly_expenses = debits['amount'].resample('ME').sum()
        
        # Calculate Core Features
        avg_monthly_income = monthly_income.mean() if not monthly_income.empty else 0
        income_std_dev = monthly_income.std() if len(monthly_income) > 1 else 0
        income_volatility = (income_std_dev / avg_monthly_income) if avg_monthly_income > 0 else 0
        
        total_income = credits['amount'].sum()
        total_expense = debits['amount'].sum()
        expense_income_ratio = (total_expense / total_income) if total_income > 0 else 1.0
        
        avg_monthly_expense = monthly_expenses.mean() if not monthly_expenses.empty else 1
        latest_balance = group.iloc[-1]['balance_after_tx']
        liquidity_buffer = latest_balance / avg_monthly_expense if avg_monthly_expense > 0 else latest_balance
        
        # Pack features into a dictionary for this borrower
        features.append({
            'borrower_id': borrower_id,
            'avg_monthly_income': round(avg_monthly_income, 2),
            'income_std_dev': round(income_std_dev, 2),
            'income_volatility': round(income_volatility, 4),
            'expense_income_ratio': round(expense_income_ratio, 4),
            'liquidity_buffer': round(liquidity_buffer, 2),
            'weekly_income_variance': round(credits['amount'].resample('W').sum().var() if len(credits['amount'].resample('W').sum()) > 1 else 0, 2),
            'recurring_expense_count': len(debits[debits['category'] == 'Utilities']),
            'round_trip_transaction_count': np.random.randint(0, 5), # Simulated for MVP
            'dormancy_score': round(np.random.uniform(0, 1), 2)      # Simulated for MVP
        })
        
        count += 1
        if count % 100 == 0:
            print(f"Calculated features for {count}/{total_borrowers} borrowers...")

    features_df = pd.DataFrame(features)
    
    # Save the features profile
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    features_df.to_csv(output_path, index=False)
    print(f"Success! Saved {len(features_df)} borrower profiles to {output_path}")

if __name__ == "__main__":
    engineer_features()