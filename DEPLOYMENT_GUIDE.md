# Deployment Guide for Loan Assessment Application

## 🚀 Pre-Deployment Checklist

### ✅ Local Testing Completed
- [x] All endpoints accessible
- [x] Model loads successfully
- [x] Form submissions work
- [x] Analytics dashboard functional
- [x] Error handling tested

### 📦 Dependencies Verified
- [x] requirements.txt updated with correct versions
- [x] Model file accessible and valid
- [x] All Python packages compatible

## 🌐 Deployment Platforms

### Render Deployment

1. **Connect Repository**
   - Link your GitHub repository to Render
   - Set build command: `bash deploy_setup.sh`
   - Set start command: `gunicorn app:app`

2. **Environment Variables**
   ```
   PYTHON_VERSION=3.11.5
   PORT=10000
   ```

3. **Build Configuration**
   - Build Command: `bash deploy_setup.sh`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Heroku Deployment

1. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

2. **Set Buildpacks**
   ```bash
   heroku buildpacks:set heroku/python
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

## 🔧 Troubleshooting Common Issues

### Issue 1: "Model not available" Error

**Symptoms:**
- Application starts but model predictions fail
- Error message: "Model not available. Please contact system administrator."

**Solutions:**
1. Check if model file exists:
   ```bash
   ls -la Final_predictive_model/
   ```

2. Verify model download:
   ```bash
   bash download_model.sh
   ```

3. Test model loading:
   ```python
   import joblib
   model = joblib.load('Final_predictive_model/finalized_model.sav')
   ```

### Issue 2: XGBoost Version Compatibility

**Symptoms:**
- Warning about XGBoost model serialization
- Model loads but predictions may be inconsistent

**Solutions:**
1. Use compatible XGBoost version:
   ```
   xgboost==1.7.6
   ```

2. Retrain model with current XGBoost version if needed

### Issue 3: Port Conflicts

**Symptoms:**
- Application fails to start
- Port already in use error

**Solutions:**
1. Check port usage:
   ```bash
   lsof -i :5000
   ```

2. Use different port:
   ```bash
   PORT=5001 python app.py
   ```

### Issue 4: Missing Dependencies

**Symptoms:**
- Import errors during startup
- ModuleNotFoundError

**Solutions:**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Check Python version compatibility

## 📊 Monitoring Deployment

### Health Check Endpoints

1. **Model Status**: `GET /test_model`
   - Returns model loading status and test prediction

2. **Application Status**: `GET /`
   - Returns welcome page if app is running

3. **Analytics Status**: `GET /visuals`
   - Returns analytics dashboard

### Log Monitoring

Monitor these log messages:
- ✅ "Machine learning model loaded successfully"
- ✅ "Database connection established successfully"
- ❌ "Error loading model"
- ❌ "Model not available"

## 🧪 Testing After Deployment

### Automated Testing
```bash
python test_app.py
```

### Manual Testing Steps

1. **Access Welcome Page**
   - Navigate to root URL
   - Verify "Start Assessment" button

2. **Test Assessment Form**
   - Fill out form with test data
   - Submit and verify result page

3. **Test Analytics Dashboard**
   - Navigate to `/visuals`
   - Verify charts load correctly

4. **Test Error Handling**
   - Submit form with missing fields
   - Verify proper error messages

## 🔄 Update Procedures

### Model Updates
1. Upload new model to Google Drive
2. Update `download_model.sh` with new file ID
3. Redeploy application

### Code Updates
1. Push changes to GitHub
2. Trigger automatic deployment
3. Monitor deployment logs

## 📞 Support

If deployment issues persist:
1. Check deployment logs for specific errors
2. Verify all dependencies are installed
3. Test locally before deploying
4. Contact system administrator with error details

## 🎯 Success Criteria

Deployment is successful when:
- [ ] Application starts without errors
- [ ] Model loads successfully
- [ ] All endpoints respond correctly
- [ ] Form submissions work
- [ ] Analytics dashboard displays
- [ ] Error handling functions properly 