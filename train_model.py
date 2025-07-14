# train_model.py
# This script loads the loan data, preprocesses it,
# trains a loan defaulter prediction model, and saves the model.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier # Assumed based on previous error 'weight_boosting'
from sklearn.tree import DecisionTreeClassifier # Base estimator for AdaBoost
from sklearn.metrics import accuracy_score, classification_report


# --- Configuration ---
DATA_PATH = 'ModelData/cs-training.csv'
MODEL_DIR = 'Final_predictive_model'
MODEL_FILENAME = 'finalized_model.sav'
FULL_MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)


# --- 1. Load Data ---
print(f"Loading data from: {DATA_PATH}")
try:
    data = pd.read_csv(DATA_PATH)
    print("Data loaded successfully.")
    print(f"Initial data shape: {data.shape}")
except FileNotFoundError:
    print(f"Error: Dataset not found at {DATA_PATH}. Please ensure 'cs-training.csv' is in the 'ModelData' directory.")
    exit() # Exit if the data file is not found

# Display initial head and columns
print("\nInitial Data Head:")
print(data.head())
print("\nInitial Columns:")
print(data.columns.tolist())


# --- 2. Data Preprocessing ---

# Drop the 'Unnamed: 0' column
if 'Unnamed: 0' in data.columns:
    print("\nDropping 'Unnamed: 0' column...")
    data.drop('Unnamed: 0', axis=1, inplace=True)
    print("Dropped 'Unnamed: 0'.")
else:
    print("\n'Unnamed: 0' column not found, skipping drop.")


# Clean column names (replace '-' and convert to lowercase)
print("Cleaning column names...")
cleancolumns = []
for col in data.columns:
    cleancolumns.append(col.replace('-', '').lower())
data.columns = cleancolumns
print("Column names cleaned.")
print("\nCleaned Columns:")
print(data.columns.tolist())


# Handle missing values
print("\nChecking for missing values (before imputation):")
print(data.isnull().sum())

# Impute 'monthlyincome' with its median
if 'monthlyincome' in data.columns:
    median_monthlyincome = data['monthlyincome'].median()
    data['monthlyincome'].fillna(median_monthlyincome, inplace=True)
    print(f"Imputed 'monthlyincome' missing values with median: {median_monthlyincome}")
else:
    print("'monthlyincome' column not found, skipping imputation.")

# Impute 'numberofdependents' with its mode (most frequent value)
if 'numberofdependents' in data.columns:
    mode_dependents = data['numberofdependents'].mode()[0]
    data['numberofdependents'].fillna(mode_dependents, inplace=True)
    print(f"Imputed 'numberofdependents' missing values with mode: {mode_dependents}")
else:
    print("'numberofdependents' column not found, skipping imputation.")


print("\nMissing values after imputation:")
print(data.isnull().sum())


# Handle outliers and inconsistencies

# Age can't be 0. Remove rows where age is 0.
if 'age' in data.columns:
    initial_rows = data.shape[0]
    data = data[data['age'] != 0]
    rows_removed = initial_rows - data.shape[0]
    if rows_removed > 0:
        print(f"Removed {rows_removed} rows where 'age' was 0.")
    else:
        print("No rows with 'age' as 0 found.")
else:
    print("'age' column not found, skipping age check.")


# Cap 'revolvingutilizationofunsecuredlines' at 1.0 (or a high percentile if > 1 is valid for over-utilization)
# Given the column name "utilization", values > 1 could mean over-utilization or errors. Capping at 1.0.
if 'revolvingutilizationofunsecuredlines' in data.columns:
    initial_max_ruoul = data['revolvingutilizationofunsecuredlines'].max()
    # Cap values that are excessively high, assuming 1.0 is full utilization.
    # We can consider keeping slight over-utilization if it's meaningful, but a cap makes sense.
    # Let's cap at 1.0 (assuming it means 100% utilization) to normalize.
    # If values > 1 are meant to indicate over-utilization (e.g., 1.5 means 150%), they should be kept
    # but extreme outliers (e.g., 50000) definitely need capping.
    # For now, a strict cap at 1.0, as implied by 'utilization'.
    data['revolvingutilizationofunsecuredlines'] = np.where(
        data['revolvingutilizationofunsecuredlines'] > 1.0, 1.0, data['revolvingutilizationofunsecuredlines']
    )
    # Alternatively, cap at 99.9th percentile for extremely large values while allowing slight over-utilization:
    # percentile_99_9 = data['revolvingutilizationofunsecuredlines'].quantile(0.999)
    # data['revolvingutilizationofunsecuredlines'] = np.where(
    #     data['revolvingutilizationofunsecuredlines'] > percentile_99_9, percentile_99_9, data['revolvingutilizationofunsecuredlines']
    # )
    print(f"Capped 'revolvingutilizationofunsecuredlines' at 1.0. Initial max was: {initial_max_ruoul}")
else:
    print("'revolvingutilizationofunsecuredlines' column not found, skipping capping.")


# Cap extreme outliers in 'numberoftime3059dayspastduenotworse', 'numberoftimes90dayslate', 'numberoftime6089dayspastduenotworse'
# These columns often have values like 96, 98 which are likely placeholders for "many" or errors.
# Let's cap them at a reasonable upper percentile (e.g., 99th percentile) to reduce outlier impact.
late_payment_cols = [
    'numberoftime3059dayspastduenotworse',
    'numberoftimes90dayslate',
    'numberoftime6089dayspastduenotworse'
]

for col in late_payment_cols:
    if col in data.columns:
        percentile_99 = data[col].quantile(0.99)
        initial_max = data[col].max()
        data[col] = np.where(data[col] > percentile_99, percentile_99, data[col])
        print(f"Capped '{col}' at {percentile_99:.2f}. Initial max was: {initial_max}")
    else:
        print(f"'{col}' column not found, skipping capping.")


print("\nData preprocessing complete.")
print(f"Final data shape after preprocessing: {data.shape}")


# --- 3. Feature and Target Split ---
TARGET_COLUMN = 'seriousdlqin2yrs'
FEATURES = [col for col in data.columns if col != TARGET_COLUMN]

if TARGET_COLUMN not in data.columns:
    print(f"Error: Target column '{TARGET_COLUMN}' not found in the data.")
    exit()

X = data[FEATURES]
y = data[TARGET_COLUMN]

print(f"\nFeatures (X) shape: {X.shape}")
print(f"Target (y) shape: {y.shape}")


# --- 4. Split Data into Training and Testing Sets ---
# Using a fixed random_state for reproducibility
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
# stratify=y ensures that the proportion of target classes is the same in both train and test sets.

print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_test shape: {y_test.shape}")


# --- 5. Train the Model ---
print("\nTraining the model...")

# AdaBoostClassifier with a DecisionTreeClassifier stump as base estimator
# This is a common setup for AdaBoost.
model = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1), # Base estimator is a shallow decision tree (stump)
    n_estimators=100, # Number of boosting stages
    random_state=42 # For reproducibility
)

model.fit(X_train, y_train)
print("Model training complete.")


# --- 6. Evaluate the Model (Optional, but Good Practice) ---
print("\nEvaluating the model on the test set...")
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# --- 7. Save the Trained Model ---
# Create the directory if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)

print(f"\nSaving model to: {FULL_MODEL_PATH}")
try:
    pickle.dump(model, open(FULL_MODEL_PATH, 'wb'))
    print("Model saved successfully!")
except Exception as e:
    print(f"Error saving model: {e}")

print("\nScript finished.")
