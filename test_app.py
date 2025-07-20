#!/usr/bin/env python3
"""
Comprehensive test script for the Loan Assessment Application
Tests all endpoints, model functionality, and error handling
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:5001"
TEST_CASES = [
    {
        "name": "Low Risk Profile",
        "data": {
            "revolvingutilizationofunsecuredlines": "0.1",
            "age": "35",
            "numberoftime3059dayspastduenotworse": "0",
            "debtratio": "0.2",
            "monthlyincome": "80000",
            "numberofopencreditlinesandloans": "5",
            "numberoftimes90dayslate": "0",
            "numberrealestateloansorlines": "1",
            "numberoftime6089dayspastduenotworse": "0",
            "numberofdependents": "2"
        }
    },
    {
        "name": "Medium Risk Profile",
        "data": {
            "revolvingutilizationofunsecuredlines": "0.5",
            "age": "45",
            "numberoftime3059dayspastduenotworse": "1",
            "debtratio": "0.6",
            "monthlyincome": "50000",
            "numberofopencreditlinesandloans": "8",
            "numberoftimes90dayslate": "1",
            "numberrealestateloansorlines": "2",
            "numberoftime6089dayspastduenotworse": "1",
            "numberofdependents": "3"
        }
    },
    {
        "name": "High Risk Profile",
        "data": {
            "revolvingutilizationofunsecuredlines": "0.9",
            "age": "28",
            "numberoftime3059dayspastduenotworse": "3",
            "debtratio": "0.8",
            "monthlyincome": "30000",
            "numberofopencreditlinesandloans": "12",
            "numberoftimes90dayslate": "2",
            "numberrealestateloansorlines": "0",
            "numberoftime6089dayspastduenotworse": "2",
            "numberofdependents": "1"
        }
    }
]

def test_endpoint(url, name="Endpoint"):
    """Test if an endpoint is accessible"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {name}: Accessible")
            return True
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)}")
        return False

def test_model_endpoint():
    """Test the model endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/test_model", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('model_loaded'):
                print(f"✅ Model Endpoint: Working (Confidence: {data.get('confidence', 0):.1f}%)")
                return True
            else:
                print(f"❌ Model Endpoint: Model not loaded")
                return False
        else:
            print(f"❌ Model Endpoint: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model Endpoint: Error - {str(e)}")
        return False

def test_assessment_form():
    """Test the assessment form submission"""
    for test_case in TEST_CASES:
        print(f"\n🧪 Testing: {test_case['name']}")
        try:
            # Submit form
            response = requests.post(
                f"{BASE_URL}/assessment",
                data=test_case['data'],
                timeout=10,
                allow_redirects=False
            )
            
            if response.status_code == 302:  # Redirect to result page
                print(f"✅ Form submission successful for {test_case['name']}")
                
                # Follow redirect to result page
                result_url = response.headers.get('Location')
                if result_url:
                    result_response = requests.get(f"{BASE_URL}{result_url}", timeout=10)
                    if result_response.status_code == 200:
                        print(f"✅ Result page accessible for {test_case['name']}")
                    else:
                        print(f"❌ Result page error for {test_case['name']}: HTTP {result_response.status_code}")
                else:
                    print(f"❌ No redirect URL for {test_case['name']}")
            else:
                print(f"❌ Form submission failed for {test_case['name']}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing {test_case['name']}: {str(e)}")

def test_analytics_endpoints():
    """Test analytics dashboard endpoints"""
    endpoints = [
        ("/default/bygender", "Gender Analysis"),
        ("/default/sept_delays", "Payment Delays"),
        ("/api/age_bal", "Age Balance"),
        ("/population/summary", "Population Summary"),
        ("/bill/payment", "Bill Payment")
    ]
    
    print("\n📊 Testing Analytics Endpoints:")
    for endpoint, name in endpoints:
        test_endpoint(f"{BASE_URL}{endpoint}", name)

def test_error_handling():
    """Test error handling with invalid data"""
    print("\n🚨 Testing Error Handling:")
    
    # Test with missing required fields
    invalid_data = {
        "revolvingutilizationofunsecuredlines": "0.5",
        "age": "35"
        # Missing other required fields
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/assessment",
            data=invalid_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Error handling: Properly handles missing fields")
        else:
            print(f"❌ Error handling: Unexpected status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Application Test")
    print("=" * 50)
    
    # Test basic endpoints
    print("\n📍 Testing Basic Endpoints:")
    test_endpoint(f"{BASE_URL}/", "Welcome Page")
    test_endpoint(f"{BASE_URL}/assessment", "Assessment Form")
    test_endpoint(f"{BASE_URL}/visuals", "Analytics Dashboard")
    
    # Test model functionality
    print("\n🤖 Testing Model Functionality:")
    test_model_endpoint()
    
    # Test form submissions
    print("\n📝 Testing Assessment Form Submissions:")
    test_assessment_form()
    
    # Test analytics endpoints
    test_analytics_endpoints()
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("✅ Comprehensive testing completed!")
    print("If all tests passed, the application is ready for deployment.")

if __name__ == "__main__":
    main() 