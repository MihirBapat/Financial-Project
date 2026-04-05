import pandas as pd
from sklearn.ensemble import IsolationForest
import os

def detect_manipulation():
    print("Starting Manipulation Detection (Isolation Forest)...")
    
    # Input comes from our feature engineering step
    input_path = 'data/processed/features.csv'
    output_path = 'data/processed/anomalies.csv'
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return
        
    df = pd.read_csv(input_path)
    
    # We feed the model specific behavioral features
    features_for_model = [
        'income_volatility', 
        'expense_income_ratio', 
        'weekly_income_variance',
        'round_trip_transaction_count',
        'dormancy_score'
    ]
    
    X = df[features_for_model]
    
    # Initialize the Machine Learning model
    # Contamination=0.10 means we assume roughly 10% of profiles might have suspicious activity
    iso_forest = IsolationForest(contamination=0.10, random_state=42)
    
    # Fit the model and calculate an anomaly score for every borrower
    iso_forest.fit(X)
    scores = iso_forest.decision_function(X)
    
    df['anomaly_score'] = round(pd.Series(scores), 4)
    
    # Apply the GCI Penalty Rules based on the score
    def assign_label_and_penalty(row):
        if row['anomaly_score'] > 0:
            return pd.Series(['clean', 1.0])
        elif row['anomaly_score'] > -0.05:
            return pd.Series(['suspicious', 0.75])
        else:
            return pd.Series(['high_risk', 0.50])
            
    df[['manipulation_label', 'penalty_multiplier']] = df.apply(assign_label_and_penalty, axis=1)
    
    # Tally up the results
    clean_count = len(df[df['manipulation_label'] == 'clean'])
    suspicious_count = len(df[df['manipulation_label'] == 'suspicious'])
    risk_count = len(df[df['manipulation_label'] == 'high_risk'])
    
    print(f"Detection Complete:")
    print(f" - Clean profiles: {clean_count}")
    print(f" - Suspicious profiles: {suspicious_count}")
    print(f" - High Risk profiles: {risk_count}")
    
    # Save the enriched data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Success! Saved scored profiles to {output_path}")

if __name__ == "__main__":
    detect_manipulation()