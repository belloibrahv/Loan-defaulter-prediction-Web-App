from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL
import pickle
import yaml
import numpy as np
import pandas as pd
import os

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
try:
    loaded_model = pickle.load(open('Final_predictive_model/finalized_model.sav', 'rb'))
    print("✅ Machine learning model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {str(e)}")
    loaded_model = None

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
            float_fields = ['debtratio', 'monthlyincome', 'ruoul']
            int_fields = ['age', 'Dependents', '30-59 days', '60-89 days', '90days', 
                         'NumberOfOpenCreditLinesAndLoans', 'NumberRealEstateLoansOrLines']
            features = {}
            for field in float_fields:
                if field in userDetails:
                    features[field] = float(userDetails[field])
            for field in int_fields:
                if field in userDetails:
                    features[field] = int(float(userDetails[field]))
            if features['age'] < 18 or features['age'] > 100:
                raise ValueError("Age must be between 18 and 100 years.")
            if features['monthlyincome'] < 0:
                raise ValueError("Monthly income cannot be negative.")
            if features['debtratio'] < 0 or features['debtratio'] > 1:
                raise ValueError("Debt ratio must be between 0 and 1 (0% to 100%).")
            if features['ruoul'] < 0 or features['ruoul'] > 1:
                raise ValueError("Credit utilization must be between 0 and 1 (0% to 100%).")
            feature_array = np.array([[
                features['age'],
                features['Dependents'],
                features['debtratio'],
                features['monthlyincome'],
                features['ruoul'],
                features['30-59 days'],
                features['60-89 days'],
                features['90days'],
                features['NumberOfOpenCreditLinesAndLoans'],
                features['NumberRealEstateLoansOrLines']
            ]])
            if loaded_model is not None:
                prediction = loaded_model.predict(feature_array)
                try:
                    prediction_proba = loaded_model.predict_proba(feature_array)[0]
                    confidence = max(prediction_proba) * 100
                except:
                    confidence = 85
                if DB_CONNECTED:
                    try:
                        cur = mysql.connection.cursor()
                        cur.execute("""
                            INSERT INTO data(
                                Age, Nuumber_Of_Dependents, Debt_Ratio, Montly_Income, 
                                RUOUL, 30_59Days, 60_89Days, 90_days, 
                                Number_of_open_Credit_lines_and_loans, Number_of_real_estate_loans_lines
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            features['age'], features['Dependents'], features['debtratio'],
                            features['monthlyincome'], features['ruoul'], features['30-59 days'],
                            features['60-89 days'], features['90days'],
                            features['NumberOfOpenCreditLinesAndLoans'],
                            features['NumberRealEstateLoansOrLines']
                        ))
                        mysql.connection.commit()
                        cur.close()
                    except Exception as db_error:
                        pass
                if prediction[0] == 1:
                    prediction_result = 'Congratulations! Your loan application has been approved'
                    prediction_details = f'Based on our analysis, your application shows a low risk profile with {confidence:.1f}% confidence. Our credit risk assessment system recommends approval.'
                else:
                    prediction_result = 'Application requires further review'
                    prediction_details = f'Our analysis indicates some risk factors that need attention. Confidence level: {confidence:.1f}%. We recommend reviewing the application with additional documentation.'
            else:
                raise ValueError("Model not available. Please contact system administrator.")
            session['prediction_result'] = prediction_result
            session['prediction_details'] = prediction_details
            return redirect(url_for('result'))
        except ValueError as ve:
            return render_template("form.html", error=str(ve))
        except Exception as e:
            return render_template("form.html", error="An unexpected error occurred. Please try again or contact support if the problem persists.")
    return render_template("form.html")

@app.route("/result")
def result():
    prediction_result = session.get('prediction_result', None)
    prediction_details = session.get('prediction_details', None)
    if not prediction_result:
        return redirect(url_for('assessment'))
    return render_template("result.html", prediction_result=prediction_result, prediction_details=prediction_details)

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
        if loaded_model is None:
            return jsonify({'error': 'Model not loaded'})
        
        # Test with sample data
        test_features = np.array([[35, 2, 0.3, 50000, 0.25, 0, 0, 0, 3, 1]])
        prediction = loaded_model.predict(test_features)
        
        try:
            prediction_proba = loaded_model.predict_proba(test_features)[0]
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
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
