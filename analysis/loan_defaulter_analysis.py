# loan_defaulter_analysis.py
# Additional analysis and visualizations for the loan defaulter prediction model

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report
from sklearn.inspection import permutation_importance
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'ModelData', 'cs-training.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'Final_predictive_model')
MODEL_FILENAME = 'finalized_model.sav'
FULL_MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)

# Load the model
print("Loading model...")
with open(FULL_MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# Load the data
print("Loading data...")
data = pd.read_csv(DATA_PATH)

# Preprocess the data (same as in train_model.py)
print("Preprocessing data...")
# Drop 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in data.columns:
    data.drop('Unnamed: 0', axis=1, inplace=True)

# Clean column names
data.columns = [col.replace('-', '').lower() for col in data.columns]

# Handle missing values
median_monthlyincome = data['monthlyincome'].median()
data['monthlyincome'].fillna(median_monthlyincome, inplace=True)
mode_dependents = data['numberofdependents'].mode()[0]
data['numberofdependents'].fillna(mode_dependents, inplace=True)

# Remove rows where age is 0
initial_rows = data.shape[0]
data = data[data['age'] != 0]

# Feature and target split
TARGET_COLUMN = 'seriousdlqin2yrs'
FEATURES = [col for col in data.columns if col != TARGET_COLUMN]
X = data[FEATURES]
y = data[TARGET_COLUMN]

# Create output directory if it doesn't exist
if not os.path.exists('analysis_output'):
    os.makedirs('analysis_output')

# 1. Feature Importance Analysis
def plot_feature_importance():
    print("Generating feature importance plot...")
    
    # Get feature importances using permutation importance
    result = permutation_importance(model, X, y, n_repeats=10, random_state=42)
    
    # Sort features by importance
    sorted_idx = result.importances_mean.argsort()[::-1]
    
    plt.figure(figsize=(12, 8))
    plt.barh(range(len(sorted_idx)), result.importances_mean[sorted_idx], align='center')
    plt.yticks(range(len(sorted_idx)), np.array(FEATURES)[sorted_idx])
    plt.xlabel("Feature Importance")
    plt.title("Feature Importance Analysis")
    plt.tight_layout()
    plt.savefig('analysis_output/feature_importance.png', dpi=300)
    plt.close()

# 2. ROC Curve Analysis
def plot_roc_curve():
    print("Generating ROC curve...")
    y_pred_proba = model.predict_proba(X)[:, 1]
    fpr, tpr, _ = roc_curve(y, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.savefig('analysis_output/roc_curve.png', dpi=300)
    plt.close()

# 3. Confusion Matrix Analysis
def plot_confusion_matrix():
    print("Generating confusion matrix...")
    y_pred = model.predict(X)
    cm = confusion_matrix(y, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
               xticklabels=['Non-Defaulter', 'Defaulter'],
               yticklabels=['Non-Defaulter', 'Defaulter'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.savefig('analysis_output/confusion_matrix.png', dpi=300)
    plt.close()

# 4. Detailed Classification Report
def generate_classification_report():
    print("Generating detailed classification report...")
    y_pred = model.predict(X)
    report = classification_report(y, y_pred, output_dict=True)
    
    # Convert to DataFrame for better formatting
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv('analysis_output/classification_report.csv', index_label='Class')
    
    # Print summary
    print("\nDetailed Classification Report:")
    print(report_df)

# 5. Feature Correlation Analysis
def plot_feature_correlations():
    print("Generating feature correlation heatmap...")
    plt.figure(figsize=(12, 10))
    sns.heatmap(X.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig('analysis_output/feature_correlations.png', dpi=300)
    plt.close()

# 6. Target Distribution Analysis
def plot_target_distribution():
    print("Generating target distribution plot...")
    plt.figure(figsize=(8, 6))
    sns.countplot(data=data, x=TARGET_COLUMN)
    plt.title('Target Distribution (Defaulters vs Non-Defaulters)')
    plt.xlabel('Serious Delinquency in 2 Years')
    plt.ylabel('Count')
    plt.savefig('analysis_output/target_distribution.png', dpi=300)
    plt.close()

# Run all analyses
if __name__ == "__main__":
    print("Starting additional analysis...")
    
    # Create plots and reports
    plot_feature_importance()
    plot_roc_curve()
    plot_confusion_matrix()
    generate_classification_report()
    plot_feature_correlations()
    plot_target_distribution()
    
    print("\nAnalysis complete. All plots and reports have been saved to 'analysis_output' directory.")
