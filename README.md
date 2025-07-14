# Credit Risk Assessment System

A modern, AI-powered credit risk assessment web application that helps financial institutions evaluate loan applications with advanced machine learning algorithms.

## 🚀 Features

- **AI-Powered Risk Assessment**: Advanced machine learning algorithms trained on extensive financial data
- **Real-time Analysis**: Instant risk assessment with detailed analytics and visualizations
- **Modern UI/UX**: Professional, responsive design optimized for financial professionals
- **Comprehensive Analytics**: Interactive dashboard with multiple data visualizations
- **Secure & Reliable**: Enterprise-grade security ensuring data protection

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Machine Learning**: Scikit-learn, NumPy, Pandas
- **Database**: MySQL (optional)
- **Charts**: Chart.js
- **Deployment**: Render (Cloud Platform)

## 📊 Key Features

### Risk Assessment
- Age and demographic analysis
- Financial metrics evaluation (income, debt ratio, credit utilization)
- Payment history analysis
- Credit line and asset assessment
- Real-time prediction with confidence scores

### Analytics Dashboard
- Default rate by age group analysis
- Payment delay patterns
- Age vs credit balance correlation
- Population age distribution
- Bill vs payment analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/belloibrahv/Loan-defaulter-prediction-Web-App.git
   cd Loan-defaulter-prediction-Web-App
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Main application: http://localhost:5000
   - Analytics dashboard: http://localhost:5000/visuals

## 🗄️ Database Configuration (Optional)

The application can work with or without a MySQL database. To enable database functionality:

1. Create a `db.yaml` file in the root directory:
   ```yaml
   mysql_host: your_host
   mysql_user: your_username
   mysql_password: your_password
   mysql_db: your_database
   ```

2. The application will automatically detect the database configuration and store assessment data if available.

## 🎯 Usage

### Credit Risk Assessment
1. Navigate to the main page
2. Fill in the applicant's information:
   - Personal details (age, dependents)
   - Financial information (income, debt ratio, credit utilization)
   - Payment history (late payments)
   - Credit profile (open lines, real estate loans)
3. Submit the form to receive an instant risk assessment
4. View detailed results with confidence scores

### Analytics Dashboard
1. Click on "Analytics" in the navigation
2. Explore various data visualizations:
   - Default rate analysis
   - Payment pattern trends
   - Age-based credit correlations
   - Population demographics

## 🚀 Deployment on Render

### Automatic Deployment
1. Fork or clone this repository to your GitHub account
2. Sign up for a free account on [Render](https://render.com)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure the deployment:
   - **Name**: Credit Risk Assessment
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"

### Manual Deployment
1. Create a new Web Service on Render
2. Connect your repository
3. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**: Add any required environment variables

## 📁 Project Structure

```
Loan-defaulter-prediction-Web-App/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── Procfile                       # Render deployment configuration
├── db.yaml                        # Database configuration (optional)
├── templates/                      # HTML templates
│   ├── template.html              # Main application template
│   ├── home.html                  # Home page template
│   └── visuals.html               # Analytics dashboard template
├── static/                        # Static assets
│   ├── css/                       # Stylesheets
│   ├── js/                        # JavaScript files
│   └── img/                       # Images
├── ModelData/                     # Training data
├── Final_predictive_model/        # Trained ML model
└── analysis/                      # Data analysis scripts
```

## 🔧 Configuration

### Environment Variables
- `PORT`: Server port (default: 5000)
- `MYSQL_HOST`: Database host
- `MYSQL_USER`: Database username
- `MYSQL_PASSWORD`: Database password
- `MYSQL_DB`: Database name

### Model Configuration
The application uses a pre-trained machine learning model located in `Final_predictive_model/finalized_model.sav`. The model is trained on credit risk data and provides binary classification (approve/review).

## 📈 API Endpoints

- `GET /`: Main application page
- `POST /`: Submit assessment form
- `GET /visuals`: Analytics dashboard
- `GET /default/bygender`: Default rate by age group data
- `GET /default/sept_delays`: Payment delay data
- `GET /api/age_bal`: Age vs credit balance data
- `GET /population/summary`: Population age distribution
- `GET /bill/payment`: Bill vs payment analysis
- `GET /test_model`: Model testing endpoint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Flask and modern web technologies
- Machine learning powered by Scikit-learn
- UI/UX designed for financial professionals
- Deployed on Render cloud platform

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team

---

**Note**: This application is designed for educational and demonstration purposes. For production use in financial institutions, additional security measures and compliance requirements should be implemented.
