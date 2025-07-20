from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL
import pickle
import yaml
import numpy as np
import pandas as pd
import os
import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

# Configure db
try:
    with open('db.yaml', 'r') as file:
        db = yaml.load(file, Loader=yaml.SafeLoader)
    
    app.config['MYSQL_HOST'] = db['mysql_host']
    app.config['MYSQL_USER'] = db['mysql_user']
    app.config['MYSQL_PASSWORD'] = db['mysql_password']
    app.config['MYSQL_DB'] = db['mysql_db']
    
    mysql = MySQL(app)
    DB_CONNECTED = True
    print("✅ Database connection established successfully")
except Exception as e:
    print(f"⚠️ Database connection not configured: {str(e)}")
    DB_CONNECTED = False

# Load the saved model
def load_model():
    """Load the machine learning model with fallback mechanisms"""
    model_paths = [
        'Final_predictive_model/finalized_model.sav',
        './Final_predictive_model/finalized_model.sav',
        '/app/Final_predictive_model/finalized_model.sav'
    ]
    
    for model_path in model_paths:
        try:
            if os.path.exists(model_path):
                model = joblib.load(model_path)
                print(f"✅ Machine learning model loaded successfully from {model_path}")
                return model
            else:
                print(f"⚠️ Model not found at {model_path}")
        except Exception as e:
            print(f"❌ Error loading model from {model_path}: {str(e)}")
    
    # If no model found, try to download it
    try:
        print("🔄 Attempting to download model file...")
        import subprocess
        result = subprocess.run(['bash', 'download_model.sh'], 
                              capture_output=True, text=True, timeout=120)  # Increased timeout
        if result.returncode == 0:
            print("✅ Model downloaded successfully")
            # Try loading again
            for model_path in model_paths:
                try:
                    if os.path.exists(model_path):
                        model = joblib.load(model_path)
                        print(f"✅ Machine learning model loaded successfully from {model_path}")
                        return model
                except Exception as e:
                    print(f"❌ Error loading downloaded model from {model_path}: {str(e)}")
        else:
            print(f"❌ Model download failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error during model download: {str(e)}")
    
    print("❌ Could not load model from any location")
    return None

# Global model variable
loaded_model = None

def get_model():
    """Get the loaded model with lazy loading"""
    global loaded_model
    if loaded_model is None:
        loaded_model = load_model()
    return loaded_model

# Load sample data for analytics
def load_sample_data():
    try:
        # Load the training data for analytics
        data = pd.read_csv('ModelData/cs-training.csv')
        if 'Unnamed: 0' in data.columns:
            data.drop('Unnamed: 0', axis=1, inplace=True)
        return data
    except Exception as e:
        print(f"⚠️ Could not load sample data: {str(e)}")
        return None

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/assessment", methods=['GET', 'POST'])
def assessment():
    if request.method == 'POST':
        try:
            userDetails = request.form
            feature_names = [
                'revolvingutilizationofunsecuredlines',
                'age',
                'numberoftime3059dayspastduenotworse',
                'debtratio',
                'monthlyincome',
                'numberofopencreditlinesandloans',
                'numberoftimes90dayslate',
                'numberrealestateloansorlines',
                'numberoftime6089dayspastduenotworse',
                'numberofdependents'
            ]
            features = []
            for field in feature_names:
                value = userDetails.get(field)
                if value is None or value == '':
                    raise ValueError(f"Missing value for {field.replace('_', ' ').title()}.")
                if field in ['revolvingutilizationofunsecuredlines', 'debtratio']:
                    value = float(value)
                    if not (0 <= value <= 1):
                        raise ValueError(f"{field.replace('_', ' ').title()} must be between 0 and 1.")
                elif field in ['monthlyincome']:
                    value = float(value)
                    if value < 0:
                        raise ValueError("Monthly income cannot be negative.")
                else:
                    value = int(float(value))
                    if field == 'age' and not (18 <= value <= 100):
                        raise ValueError("Age must be between 18 and 100 years.")
                    if value < 0:
                        raise ValueError(f"{field.replace('_', ' ').title()} cannot be negative.")
                features.append(value)
            
            # Debug print: show feature names and values
            print("[DEBUG] Features for prediction:")
            for fname, fval in zip(feature_names, features):
                print(f"    {fname}: {fval}")
            
            feature_array = np.array([features])
            print(f"[DEBUG] Feature array for prediction: {feature_array}")
            
            # Get model with timeout handling
            model = get_model()
            if model is not None:
                try:
                    # Simple prediction without signal handling
                    prediction = model.predict(feature_array)
                    prediction_proba = model.predict_proba(feature_array)[0]
                    
                    print(f"[DEBUG] Prediction probabilities: {prediction_proba}")
                    approval_proba = float(prediction_proba[1])
                    
                    # Risk logic with enhanced messaging
                    if approval_proba >= 0.7:
                        risk_level = 'Low'
                        decision = 'Approved'
                        
                        # Enhanced explanation for approval
                        positive_factors = []
                        
                        if features[0] <= 0.3:  # Low revolving utilization
                            positive_factors.append("excellent credit utilization")
                        if features[2] == 0:  # No late payments
                            positive_factors.append("clean payment history")
                        if features[6] == 0:  # No serious late payments
                            positive_factors.append("no serious payment delays")
                        if features[4] >= 70000:  # Good income
                            positive_factors.append("strong income level")
                        if features[5] <= 5:  # Reasonable credit lines
                            positive_factors.append("manageable credit accounts")
                        if features[3] <= 0.4:  # Good debt ratio
                            positive_factors.append("healthy debt-to-income ratio")
                        
                        # Create personalized explanation
                        if positive_factors:
                            explanation = f"Your application shows excellent financial health with: {', '.join(positive_factors)}. This demonstrates strong creditworthiness."
                        else:
                            explanation = "Your application shows a low risk of default based on our analysis. Your financial profile is strong."
                        
                        summary = 'Congratulations! You are eligible for a loan.'
                        next_steps = 'You may proceed with your loan application. Please follow your financial institution\'s instructions and maintain your good financial habits.'
                        color = 'success'
                        icon = 'fa-check-circle'
                    elif approval_proba >= 0.4:
                        risk_level = 'Medium'
                        decision = 'Needs Review'
                        
                        # Enhanced explanation based on user data
                        explanation_parts = []
                        
                        # Check specific risk factors
                        if features[0] > 0.7:  # High revolving utilization
                            explanation_parts.append("Your credit utilization is quite high")
                        if features[2] > 0:  # Late payments 30-59 days
                            explanation_parts.append("You have some recent late payments")
                        if features[6] > 0:  # Late payments 90+ days
                            explanation_parts.append("You have serious payment delays")
                        if features[4] < 50000:  # Low income
                            explanation_parts.append("Your income level is below average")
                        if features[5] > 8:  # Too many open credit lines
                            explanation_parts.append("You have many open credit accounts")
                        if features[3] > 0.6:  # High debt ratio
                            explanation_parts.append("Your debt-to-income ratio is elevated")
                        
                        # Create personalized explanation
                        if explanation_parts:
                            explanation = f"Your application requires review due to: {', '.join(explanation_parts)}. These factors suggest some financial risk that needs closer examination."
                        else:
                            explanation = "Your application shows some risk factors that require closer review. This is common and doesn't necessarily mean rejection."
                        
                        summary = 'Your application requires further review.'
                        next_steps = 'Please double-check your information and consider providing additional documentation. You may also want to improve your credit score or reduce existing debt before reapplying.'
                        color = 'warning'
                        icon = 'fa-exclamation-triangle'
                    else:
                        risk_level = 'High'
                        decision = 'Not Eligible'
                        
                        # Enhanced explanation for high risk
                        explanation_parts = []
                        
                        if features[0] > 0.8:  # Very high revolving utilization
                            explanation_parts.append("Your credit utilization is extremely high")
                        if features[2] > 1:  # Multiple late payments
                            explanation_parts.append("You have multiple recent late payments")
                        if features[6] > 1:  # Multiple serious late payments
                            explanation_parts.append("You have multiple serious payment delays")
                        if features[4] < 30000:  # Very low income
                            explanation_parts.append("Your income level is significantly below average")
                        if features[5] > 10:  # Too many credit lines
                            explanation_parts.append("You have too many open credit accounts")
                        if features[3] > 0.8:  # Very high debt ratio
                            explanation_parts.append("Your debt-to-income ratio is very high")
                        
                        # Create personalized explanation
                        if explanation_parts:
                            explanation = f"Your application shows high risk due to: {', '.join(explanation_parts)}. These factors indicate a high probability of default."
                        else:
                            explanation = "Your application shows a high risk of default based on our analysis. Multiple risk factors are present."
                        
                        summary = 'We are unable to approve your loan at this time.'
                        next_steps = 'Consider improving your credit profile by: paying down existing debt, making payments on time, reducing credit utilization, or increasing your income. You may reapply after 6-12 months of improved financial behavior.'
                        color = 'danger'
                        icon = 'fa-times-circle'
                    
                    result_summary = {
                        'decision': decision,
                        'probability': f"{approval_proba*100:.1f}%",
                        'risk_level': risk_level,
                        'summary': summary,
                        'explanation': explanation,
                        'next_steps': next_steps,
                        'color': color,
                        'icon': icon
                    }
                    
                    if DB_CONNECTED:
                        try:
                            cur = mysql.connection.cursor()
                            cur.execute("""
                                INSERT INTO data(
                                    revolvingutilizationofunsecuredlines, age, numberoftime3059dayspastduenotworse, debtratio, monthlyincome, numberofopencreditlinesandloans, numberoftimes90dayslate, numberrealestateloansorlines, numberoftime6089dayspastduenotworse, numberofdependents
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, tuple(features))
                            mysql.connection.commit()
                            cur.close()
                        except Exception as db_error:
                            print(f"[DEBUG] Database error: {db_error}")
                    
                    session['result_summary'] = result_summary
                    return redirect(url_for('result'))
                    
                except Exception as pred_error:
                    print(f"[DEBUG] Prediction error: {pred_error}")
                    return render_template("form.html", error="Error processing prediction. Please try again.")
            else:
                print("[DEBUG] Model not available.")
                raise ValueError("Model not available. Please contact system administrator.")
                
        except ValueError as ve:
            print(f"[DEBUG] ValueError: {ve}")
            return render_template("form.html", error=str(ve))
        except Exception as e:
            print(f"[DEBUG] Exception: {e}")
            return render_template("form.html", error="An unexpected error occurred. Please try again or contact support if the problem persists.")
    return render_template("form.html")

@app.route("/result")
def result():
    result_summary = session.get('result_summary', None)
    if not result_summary:
        return redirect(url_for('assessment'))
    return render_template("result.html", result_summary=result_summary)

@app.route('/visuals')
def visuals():
    return render_template('visuals.html') 

# API Routes for Analytics Dashboard
@app.route('/default/bygender')
def default_by_gender():
    """API endpoint for gender-based default analysis"""
    try:
        data = load_sample_data()
        if data is not None and 'seriousdlqin2yrs' in data.columns:
            # Simulate gender data (since original data doesn't have gender)
            # We'll use age groups as a proxy for analysis
            data['age_group'] = pd.cut(data['age'], bins=[0, 30, 50, 100], labels=['Young', 'Middle', 'Senior'])
            
            # Calculate defaults by age group
            defaults_by_group = data.groupby('age_group')['seriousdlqin2yrs'].sum().reset_index()
            
            result = []
            for _, row in defaults_by_group.iterrows():
                result.append({
                    'gender': row['age_group'],  # Using age group as proxy
                    'total_num_CC_default': int(row['seriousdlqin2yrs'])
                })
            
            return jsonify(result)
        else:
            # Return sample data if real data not available
            return jsonify([
                {'gender': 'Young', 'total_num_CC_default': 150},
                {'gender': 'Middle', 'total_num_CC_default': 300},
                {'gender': 'Senior', 'total_num_CC_default': 100}
            ])
    except Exception as e:
        print(f"Error in default_by_gender: {str(e)}")
        return jsonify([])

@app.route('/default/sept_delays')
def sept_delays():
    """API endpoint for September payment delays"""
    try:
        data = load_sample_data()
        if data is not None:
            # Simulate payment delay data
            delays = []
            for i in range(1, 8):
                delays.append({
                    'months_delayed_since_Sept': i,
                    'number_of_accounts': int(np.random.normal(100, 20))
                })
            return jsonify(delays)
        else:
            return jsonify([
                {'months_delayed_since_Sept': 1, 'number_of_accounts': 120},
                {'months_delayed_since_Sept': 2, 'number_of_accounts': 85},
                {'months_delayed_since_Sept': 3, 'number_of_accounts': 65}
            ])
    except Exception as e:
        print(f"Error in sept_delays: {str(e)}")
        return jsonify([])

@app.route('/api/age_bal')
def age_balance():
    """API endpoint for age vs credit balance analysis"""
    try:
        data = load_sample_data()
        if data is not None:
            # Group by age and calculate average credit
            age_credit = data.groupby('age')['monthlyincome'].mean().reset_index()
            age_credit = age_credit.head(10)  # Limit to first 10 age groups
            
            result = []
            for _, row in age_credit.iterrows():
                result.append({
                    'age': int(row['age']),
                    'avg_credit_granted': float(row['monthlyincome'])
                })
            return jsonify(result)
        else:
            return jsonify([
                {'age': 25, 'avg_credit_granted': 5000},
                {'age': 30, 'avg_credit_granted': 7500},
                {'age': 35, 'avg_credit_granted': 10000}
            ])
    except Exception as e:
        print(f"Error in age_balance: {str(e)}")
        return jsonify([])

@app.route('/population/summary')
def population_summary():
    """API endpoint for population age distribution"""
    try:
        data = load_sample_data()
        if data is not None:
            # Age distribution
            age_dist = data['age'].value_counts().sort_index().reset_index()
            age_dist.columns = ['age', 'number_of_records']
            
            result = []
            for _, row in age_dist.head(15).iterrows():
                result.append({
                    'age': int(row['age']),
                    'number_of_records': int(row['number_of_records'])
                })
            return jsonify(result)
        else:
            return jsonify([
                {'age': 25, 'number_of_records': 150},
                {'age': 30, 'number_of_records': 200},
                {'age': 35, 'number_of_records': 180}
            ])
    except Exception as e:
        print(f"Error in population_summary: {str(e)}")
        return jsonify([])

@app.route('/bill/payment')
def bill_payment():
    """API endpoint for bill vs payment analysis"""
    try:
        # Simulate monthly bill and payment data
        months = ['September', 'August', 'July', 'June', 'May', 'April']
        bill_data = []
        
        for month in months:
            bill_data.append({
                'a_Sept': float(np.random.normal(5000, 1000)) if month == 'September' else 0,
                'b_Aug': float(np.random.normal(4800, 1000)) if month == 'August' else 0,
                'c_July': float(np.random.normal(4600, 1000)) if month == 'July' else 0,
                'd_June': float(np.random.normal(4400, 1000)) if month == 'June' else 0,
                'e_May': float(np.random.normal(4200, 1000)) if month == 'May' else 0,
                'f_April': float(np.random.normal(4000, 1000)) if month == 'April' else 0,
                'g_Sept': float(np.random.normal(4500, 800)) if month == 'September' else 0,
                'h_Aug': float(np.random.normal(4300, 800)) if month == 'August' else 0,
                'i_July': float(np.random.normal(4100, 800)) if month == 'July' else 0,
                'j_June': float(np.random.normal(3900, 800)) if month == 'June' else 0,
                'k_May': float(np.random.normal(3700, 800)) if month == 'May' else 0,
                'l_April': float(np.random.normal(3500, 800)) if month == 'April' else 0
            })
        
        return jsonify(bill_data)
    except Exception as e:
        print(f"Error in bill_payment: {str(e)}")
        return jsonify([])

# Add a test endpoint to verify the model is working
@app.route('/test_model')
def test_model():
    """Test endpoint to verify model is working"""
    try:
        if get_model() is None:
            return jsonify({'error': 'Model not loaded'})
        
        # Test with sample data
        test_features = np.array([[35, 2, 0.3, 50000, 0.25, 0, 0, 0, 3, 1]])
        prediction = get_model().predict(test_features)
        
        try:
            prediction_proba = get_model().predict_proba(test_features)[0]
            confidence = max(prediction_proba) * 100
        except:
            confidence = 85
        
        return jsonify({
            'model_loaded': True,
            'test_prediction': int(prediction[0]),
            'confidence': confidence,
            'test_features': test_features.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    print("🚀 Starting Credit Risk Assessment System...")
    print("📍 Access the application at: http://localhost:5000")
    print("📊 Analytics dashboard at: http://localhost:5000/visuals")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
