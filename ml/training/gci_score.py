import pandas as pd
import os

def calculate_gci():
    print("Starting Gig Cashflow Index (GCI) Calculation...")
    
    # We load the data that already has our anomaly penalties attached
    input_path = 'data/processed/anomalies.csv'
    output_path = 'data/processed/gci_scores.csv'
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return
        
    df = pd.read_csv(input_path)
    
    # --- The GCI Scoring Formula ---
    BASE_SCORE = 500 
    
    # 1. Liquidity Weight (Bonus up to +150 points for having a cash cushion)
    liquidity_capped = df['liquidity_buffer'].clip(0, 5)
    liquidity_weight = (liquidity_capped / 5) * 150
    
    # 2. Income Stability Weight (Bonus up to +150 points for low expenses compared to income)
    ratio_capped = df['expense_income_ratio'].clip(0, 1)
    stability_weight = (1 - ratio_capped) * 150
    
    # 3. Volatility Penalty (Deduction up to -100 points for wildly fluctuating income)
    volatility_capped = df['income_volatility'].clip(0, 2)
    volatility_penalty = (volatility_capped / 2) * 100
    
    # Calculate the raw cashflow score
    df['raw_gci'] = BASE_SCORE + liquidity_weight + stability_weight - volatility_penalty
    
    # 4. Anomaly Penalty (Multiply by our Isolation Forest fraud label: 1.0, 0.75, or 0.50)
    df['final_gci_score'] = df['raw_gci'] * df['penalty_multiplier']
    
    # Ensure the final score strictly stays within the standard 300 to 900 range
    df['final_gci_score'] = df['final_gci_score'].clip(300, 900).astype(int)
    
    # Display the final results
    print("\nFinal GCI Score Distribution:")
    print(f" - Excellent (750-900): {len(df[df['final_gci_score'] >= 750])}")
    print(f" - Good (600-749): {len(df[(df['final_gci_score'] >= 600) & (df['final_gci_score'] < 750)])}")
    print(f" - Fair (450-599): {len(df[(df['final_gci_score'] >= 450) & (df['final_gci_score'] < 600)])}")
    print(f" - Poor (300-449): {len(df[df['final_gci_score'] < 450])}")
    
    # Save the final scores
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_output = df[['borrower_id', 'final_gci_score', 'manipulation_label']]
    final_output.to_csv(output_path, index=False)
    
    print(f"\nSuccess! Generated GCI scores for {len(df)} borrowers and saved to {output_path}")

if __name__ == "__main__":
    calculate_gci()