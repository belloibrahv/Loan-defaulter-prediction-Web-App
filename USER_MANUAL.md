# Loan Defaulter Prediction Web Application User Manual

This manual provides step-by-step instructions for setting up, running, and using the loan defaulter prediction web application. It covers both technical setup and user interface navigation.

## 1. System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- A web browser (Chrome, Firefox, Safari, or Edge)
- Git (for cloning the repository)

## 2. Installation Guide

### 2.1 Cloning the Repository

1. Open a terminal/command prompt
2. Navigate to your desired directory
3. Run the following command:
   ```bash
   git clone <repository-url>
   cd Loan-defaulter-prediction-Web-App
   ```

### 2.2 Setting Up Python Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### 2.3 Installing Dependencies

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Verify installation:
   ```bash
   pip list
   ```

### 2.4 Model Setup

1. Ensure the model files are present in the `Final_predictive_model` directory:
   - `finalized_model.sav`
   - `scaler.pkl`
   - `encoder.pkl`

2. Verify the training data is present in the `ModelData` directory:
   - `cs-training.csv`

## 3. Running the Application

### 3.1 Starting the Server

1. Navigate to the project directory:
   ```bash
   cd Loan-defaulter-prediction-Web-App
   ```

2. Start the Flask server:
   ```bash
   python app.py
   ```

3. The application will start and be accessible at `http://localhost:5000` by default.

### 3.2 Accessing the Application

1. Open your web browser
2. Navigate to `http://localhost:5000`
3. The home page will load with the loan prediction interface

## 4. Using the Application

### 4.1 Home Page

The home page provides a user-friendly interface for loan prediction:

1. **Input Fields**:
   - Age
   - Monthly Income
   - Number of Dependents
   - Revolving Utilization of Unsecured Lines
   - Number of Time 30-59 Days Past Due Not Worse
   - Number of Open Loans
   - Number of Times 90 Days Late
   - Number of Real Estate Loans or Lines
   - Number of Time 60-89 Days Past Due Not Worse

2. **Prediction Button**:
   - Click "Predict" to get the loan default risk prediction

### 4.2 Prediction Results

After submitting the form:
1. The application will process the input data
2. The prediction result will be displayed:
   - Risk score (0-1)
   - Prediction status (Low Risk/High Risk)
   - Confidence score

## 5. Troubleshooting

### Common Issues and Solutions

1. **Server Not Starting**
   - Ensure all dependencies are installed
   - Check if port 5000 is not in use
   - Verify model files are present

2. **Prediction Errors**
   - Check input values are within valid ranges
   - Ensure no missing values in input fields
   - Verify data types match expected format

3. **Performance Issues**
   - Close unnecessary browser tabs
   - Ensure sufficient system resources
   - Consider running on a more powerful machine if needed

## 6. Technical Details

### Project Structure
```
Loan-defaulter-prediction-Web-App/
├── Final_predictive_model/         # Trained model files
├── ModelData/                     # Training data
├── static/                        # Static files (CSS, JS, images)
├── templates/                     # HTML templates
├── app.py                         # Main Flask application
├── train_model.py                 # Model training script
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

### Key Files
- `app.py`: Main application file containing Flask routes and prediction logic
- `train_model.py`: Script for training and saving the prediction model
- `requirements.txt`: List of required Python packages
- `Final_predictive_model/finalized_model.sav`: Trained machine learning model

## 7. Security Considerations

1. **Data Privacy**:
   - Do not enter real personal information
   - The application does not store user input data

2. **API Security**:
   - The application uses local-only access by default
   - No external API keys required

## 8. Contact Information

For technical support or questions, please contact:
- Project Maintainer: [Your Name]
- Email: [Your Email]
- GitHub: [Your GitHub Profile]

## 9. Version History

1.0.0 - Initial release
- Basic loan prediction functionality
- User-friendly interface
- Local model deployment
