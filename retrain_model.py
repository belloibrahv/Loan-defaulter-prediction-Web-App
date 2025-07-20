#!/usr/bin/env python3
"""
Retrain the XGBoost model with current version for compatibility
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import xgboost as xgb
import joblib
import os

def load_and_prepare_data():
    """Load and prepare the training data"""
    print("📊 Loading training data...")
    
    # Load the training data
    data = pd.read_csv('ModelData/cs-training.csv')
    
    # Remove the index column if it exists
    if 'Unnamed: 0' in data.columns:
        data = data.drop('Unnamed: 0', axis=1)
    
    # Handle missing values
    data = data.fillna(data.median())
    
    # Prepare features and target with correct column names
    feature_columns = [
        'RevolvingUtilizationOfUnsecuredLines',
        'age',
        'NumberOfTime30-59DaysPastDueNotWorse',
        'DebtRatio',
        'MonthlyIncome',
        'NumberOfOpenCreditLinesAndLoans',
        'NumberOfTimes90DaysLate',
        'NumberRealEstateLoansOrLines',
        'NumberOfTime60-89DaysPastDueNotWorse',
        'NumberOfDependents'
    ]
    
    X = data[feature_columns]
    y = data['SeriousDlqin2yrs']
    
    print(f"✅ Data loaded: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"✅ Target distribution: {y.value_counts().to_dict()}")
    
    return X, y

def train_xgboost_model(X, y):
    """Train XGBoost model with current version"""
    print("🤖 Training XGBoost model...")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create and train the model
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss',
        use_label_encoder=False  # This is the key fix for compatibility
    )
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Evaluate the model
    print("\n📈 Model Performance:")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix:\n{cm}")
    
    return model

def save_model(model, filename='Final_predictive_model/finalized_model.sav'):
    """Save the trained model"""
    print(f"💾 Saving model to {filename}...")
    
    # Create directory if it doesn't exist
    os.makedirs('Final_predictive_model', exist_ok=True)
    
    # Save the model
    joblib.dump(model, filename)
    
    # Verify the model can be loaded
    loaded_model = joblib.load(filename)
    print("✅ Model saved and verified successfully")
    
    # Test prediction
    test_data = np.array([[0.1, 35, 0, 0.2, 80000, 5, 0, 1, 0, 2]])
    pred = loaded_model.predict(test_data)
    proba = loaded_model.predict_proba(test_data)
    print(f"✅ Test prediction: {pred[0]}, Probability: {proba[0][1]:.4f}")
    
    return True

def main():
    """Main function to retrain the model"""
    print("🚀 Starting model retraining with current XGBoost version...")
    
    try:
        # Load and prepare data
        X, y = load_and_prepare_data()
        
        # Train the model
        model = train_xgboost_model(X, y)
        
        # Save the model
        success = save_model(model)
        
        if success:
            print("\n🎉 Model retraining completed successfully!")
            print("✅ The model is now compatible with the current XGBoost version")
            print("✅ Ready for deployment")
        else:
            print("\n❌ Model retraining failed")
            
    except Exception as e:
        print(f"❌ Error during model retraining: {str(e)}")
        raise

if __name__ == "__main__":
    main() 