# NDA Credit Risk Assessment System - Testing Guide

This guide will help you verify that your machine learning model and database are working correctly with your Flask application.

## 🎯 What We're Testing

1. **Machine Learning Model**: Loading, predictions, and consistency
2. **Database Connection**: MySQL connectivity and data storage
3. **Flask Application**: Server response and form processing
4. **Integration**: End-to-end functionality

## 📋 Prerequisites

Before running tests, ensure you have:

- ✅ Python 3.8+ installed
- ✅ Flask app running on port 5001
- ✅ MySQL server running (if testing database)
- ✅ Required dependencies installed

## 🚀 Quick Start Testing

### Step 1: Start Your Flask App

```bash
python app.py
```

You should see output like:
```
🚀 Starting NDA Credit Risk Assessment System...
📍 Access the application at: http://localhost:5001
📊 Analytics dashboard at: http://localhost:5001/visuals
✅ Machine learning model loaded successfully
✅ Database connection established successfully
```

### Step 2: Run Comprehensive System Test

```bash
python test_system.py
```

This will test everything automatically and provide detailed results.

## 🔍 Individual Component Testing

### 1. Test Machine Learning Model Only

```bash
python test_model.py
```

**What it tests:**
- Model file existence and loading
- Prediction functionality with sample data
- Model consistency (same input = same output)
- Edge case handling

**Expected output:**
```
✅ Model loaded successfully
✅ Model type: AdaBoostClassifier
✅ Number of estimators: 100
✅ Prediction successful
```

### 2. Test Database Connection Only

```bash
python test_database.py
```

**What it tests:**
- MySQL server connectivity
- Database credentials validation
- Table structure verification
- Sample data insertion

**Expected output:**
```
✅ Database connection established successfully
✅ MySQL Version: 8.0.xx
✅ 'data' table exists
✅ Table contains X records
```

### 3. Test Flask Application

```bash
python test_system.py
```

**What it tests:**
- Server connectivity
- Form submission and processing
- Prediction result generation
- Analytics API endpoints

## 📊 Understanding Test Results

### ✅ Success Indicators

**Model Tests:**
- Model loads without errors
- Predictions are consistent
- Confidence scores are reasonable (0-100%)
- Edge cases are handled gracefully

**Database Tests:**
- Connection established successfully
- Tables exist with correct structure
- Data can be inserted and retrieved
- No connection timeouts

**Application Tests:**
- Server responds to requests
- Form submissions work
- Prediction results are displayed
- Analytics endpoints return data

### ❌ Common Issues and Solutions

#### Model Issues

**Problem:** `Model file not found`
```
❌ Model file not found: Final_predictive_model/finalized_model.sav
```

**Solution:**
1. Check if the model file exists
2. Run the training script: `python train_model.py`
3. Verify the file path is correct

**Problem:** `Error loading model`
```
❌ Error loading model: [Errno 2] No such file or directory
```

**Solution:**
1. Ensure you're in the correct directory
2. Check file permissions
3. Verify the model was saved correctly

#### Database Issues

**Problem:** `Database connection failed`
```
❌ Database connection failed: (2003, "Can't connect to MySQL server")
```

**Solution:**
1. Start MySQL server: `sudo service mysql start` (Linux) or `brew services start mysql` (Mac)
2. Check credentials in `db.yaml`
3. Verify database exists: `CREATE DATABASE credit_risk_analysis;`

**Problem:** `Table doesn't exist`
```
⚠️ 'data' table does not exist
```

**Solution:**
1. Create the table using the provided SQL script
2. Check database schema matches the application

#### Application Issues

**Problem:** `Server not responding`
```
❌ Cannot connect to Flask server. Make sure it's running on port 5001
```

**Solution:**
1. Start the Flask app: `python app.py`
2. Check if port 5001 is available
3. Verify no firewall blocking the connection

## 🧪 Manual Testing

### Test 1: Basic Form Submission

1. Open your browser to `http://localhost:5001`
2. Fill out the form with test data:
   - Age: 35
   - Dependents: 2
   - Monthly Income: 500000
   - Debt Ratio: 0.3
   - Credit Utilization: 0.25
   - All payment history: 0
   - Open Credit Lines: 3
   - Real Estate Loans: 1
3. Submit the form
4. Verify you get a prediction result

### Test 2: Analytics Dashboard

1. Navigate to `http://localhost:5001/visuals`
2. Check if charts load properly
3. Verify data is displayed in visualizations

### Test 3: API Endpoints

Test these URLs in your browser:
- `http://localhost:5001/test_model`
- `http://localhost:5001/default/bygender`
- `http://localhost:5001/api/age_bal`

## 🔧 Troubleshooting

### Check Server Logs

When you run `python app.py`, watch for these messages:

**Good signs:**
```
✅ Machine learning model loaded successfully
✅ Database connection established successfully
🔍 Form submitted! Processing...
🤖 Making prediction with loaded model...
✅ Data stored in database successfully
```

**Warning signs:**
```
⚠️ Database connection not configured
❌ Error loading model
⚠️ Database error
```

### Verify File Structure

Ensure you have this structure:
```
your-project/
├── app.py
├── db.yaml
├── test_system.py
├── test_model.py
├── test_database.py
├── Final_predictive_model/
│   └── finalized_model.sav
├── ModelData/
│   └── cs-training.csv
└── templates/
    └── template.html
```

### Check Dependencies

Install required packages:
```bash
pip install flask flask-mysqldb scikit-learn pandas numpy pyyaml requests
```

## 📈 Performance Testing

### Load Testing

For basic load testing, you can use the test script multiple times:

```bash
# Run multiple tests quickly
for i in {1..10}; do python test_system.py; done
```

### Memory Usage

Monitor memory usage while running tests:
```bash
# On Linux/Mac
top -p $(pgrep -f "python app.py")

# Or use htop
htop
```

## 🎯 Success Criteria

Your system is working correctly when:

1. **All test scripts pass** ✅
2. **Form submissions return predictions** ✅
3. **Database stores data successfully** ✅
4. **Analytics dashboard loads** ✅
5. **No error messages in server logs** ✅

## 📞 Getting Help

If tests fail:

1. **Check the error messages** - They usually indicate the specific problem
2. **Review server logs** - Look for detailed error information
3. **Verify prerequisites** - Ensure all services are running
4. **Check file paths** - Make sure all required files exist
5. **Test components individually** - Use the specific test scripts

## 🔄 Continuous Testing

For ongoing verification, you can:

1. **Set up automated testing** - Run tests before deployments
2. **Monitor server logs** - Watch for errors during normal operation
3. **Regular health checks** - Test the system periodically
4. **User feedback** - Monitor actual usage patterns

---

**Remember:** The testing scripts are designed to be non-destructive and safe to run multiple times. They help ensure your system is working correctly before going live. 