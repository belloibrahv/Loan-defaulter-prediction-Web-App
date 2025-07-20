#!/bin/bash

echo "🚀 Setting up deployment environment..."

# Create necessary directories
mkdir -p Final_predictive_model
mkdir -p static/css
mkdir -p static/js
mkdir -p static/img
mkdir -p templates

# Download model if not present
if [ ! -f "Final_predictive_model/finalized_model.sav" ]; then
    echo "📥 Downloading model file..."
    bash download_model.sh
else
    echo "✅ Model file already exists"
fi

# Check if model file is valid
if [ -f "Final_predictive_model/finalized_model.sav" ]; then
    echo "✅ Model file found and ready"
    ls -la Final_predictive_model/
else
    echo "❌ Model file not found after download attempt"
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Test model loading
echo "🧪 Testing model loading..."
python -c "
import joblib
import os
try:
    model = joblib.load('Final_predictive_model/finalized_model.sav')
    print('✅ Model loads successfully')
    print(f'Model type: {type(model)}')
    print(f'Has predict_proba: {hasattr(model, \"predict_proba\")}')
except Exception as e:
    print(f'❌ Model loading failed: {e}')
    exit(1)
"

# Test Flask app startup
echo "🌐 Testing Flask app startup..."
timeout 10s python -c "
from app import app
print('✅ Flask app imports successfully')
" || echo "❌ Flask app import failed"

echo "✅ Deployment setup completed successfully!"
echo "📋 Next steps:"
echo "   1. Push changes to GitHub"
echo "   2. Deploy to Render/Heroku"
echo "   3. Monitor deployment logs" 