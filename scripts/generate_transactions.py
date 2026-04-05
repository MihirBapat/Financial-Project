import pandas as pd
import numpy as np
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta
import os

fake = Faker()

# Dataset Requirements
NUM_BORROWERS = 500
MIN_TX_PER_BORROWER = 300
MAX_TX_PER_BORROWER = 600

def generate_transactions():
    print("Starting synthetic data generation...")
    data = []
    
    for borrower_idx in range(NUM_BORROWERS):
        borrower_id = f"B_{borrower_idx+1:04d}"
        num_transactions = random.randint(MIN_TX_PER_BORROWER, MAX_TX_PER_BORROWER)
        
        # Start balance
        current_balance = round(random.uniform(100, 5000), 2)
        
        # Timeline: Last 12 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        for _ in range(num_transactions):
            tx_id = str(uuid.uuid4())
            timestamp = fake.date_time_between(start_date=start_date, end_date=end_date)
            
            direction = random.choices(['CREDIT', 'DEBIT'], weights=[0.4, 0.6])[0]
            
            if direction == 'CREDIT':
                amount = round(random.uniform(100, 3000), 2)
                current_balance += amount
                category = random.choice(['Gig Payout', 'Transfer In', 'Refund'])
                payment_mode = 'UPI'
            else:
                amount = round(random.uniform(10, 800), 2)
                current_balance -= amount
                category = random.choice(['Food', 'Transport', 'Utilities', 'Transfer Out', 'Entertainment'])
                payment_mode = random.choice(['UPI', 'Card', 'NetBanking'])
            
            data.append({
                'transaction_id': tx_id,
                'borrower_id': borrower_id,
                'timestamp': timestamp,
                'amount': amount,
                'direction': direction,
                'counterparty_id': f"C_{random.randint(1000, 9999)}",
                'counterparty_type': random.choice(['Merchant', 'Individual', 'Platform']),
                'payment_mode': payment_mode,
                'category': category,
                'description': fake.sentence(nb_words=3),
                'balance_after_tx': round(current_balance, 2)
            })
            
        if borrower_idx % 50 == 0:
            print(f"Generated data for {borrower_idx} borrowers...")

    df = pd.DataFrame(data)
    
    # Sort by borrower and timestamp to make it realistic
    df = df.sort_values(by=['borrower_id', 'timestamp'])
    
    # Save to the required path
    output_path = '../data/synthetic/gig_transactions.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Success! Saved {len(df)} transactions to {output_path}")

if __name__ == "__main__":
    generate_transactions()