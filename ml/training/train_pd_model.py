import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier

def train_pd_model():
    print("Starting Probability of Default (PD) Model Training...")
    
    input_path = 'data/processed/anomalies.csv'
    output_model_path = 'backend/models/pd_model.pkl' # [cite: 106, 107]
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return
        
    df = pd.read_csv(input_path)
    
    # MVP Target Simulation: Simulate a default flag based on financial stress
    np.random.seed(42)
    stress_score = (df['expense_income_ratio'] * 0.4) - (df['liquidity_buffer'] * 0.3) + (df['income_volatility'] * 0.3)
    
    # Assume the top 15% most financially stressed profiles defaulted historically
    threshold = stress_score.quantile(0.85)
    df['default_flag'] = (stress_score >= threshold).astype(int)
    
    # Define features the model will learn from
    features = [
        'avg_monthly_income', 'income_std_dev', 'income_volatility', 
        'expense_income_ratio', 'liquidity_buffer', 'weekly_income_variance',
        'recurring_expense_count'
    ]
    
    X = df[features]
    y = df['default_flag']
    
    # 1. Train / Test Split [cite: 103]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Initialize Gradient Boosting Classifier 
    gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    
    # 3. Cross-validation [cite: 104]
    cv_scores = cross_val_score(gb_model, X_train, y_train, cv=5)
    print(f"Cross-Validation Accuracy: {cv_scores.mean():.2f} (+/- {cv_scores.std() * 2:.2f})")
    
    # Train the final model
    gb_model.fit(X_train, y_train)
    
    # 4. Feature Importance Extraction [cite: 105]
    print("\nFeature Importances (What the AI cares about most):")
    importances = gb_model.feature_importances_
    for feature, imp in zip(features, importances):
        print(f" - {feature}: {imp:.4f}")
        
    # 5. Save the compiled model [cite: 106]
    os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
    joblib.dump(gb_model, output_model_path)
    print(f"\nSuccess! Saved trained PD model to {output_model_path} [cite: 107]")

if __name__ == "__main__":
    train_pd_model()