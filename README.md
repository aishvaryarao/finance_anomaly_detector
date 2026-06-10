# Finance Anomaly Detector

## Overview

Finance Anomaly Detector is a full-stack data analytics application that helps users identify unusual financial transactions from bank statements. The system automatically processes transaction data, categorizes spending, detects anomalies using machine learning, stores results in a MySQL database, and visualizes insights through an interactive dashboard.

## Features

* Upload bank statements in CSV format
* Automatic transaction categorization
* Anomaly detection using machine learning techniques
* MySQL database integration
* Interactive dashboard built with Dash and Plotly
* Spending trend analysis
* Category-wise expense breakdown
* Real-time anomaly monitoring

## Tech Stack

### Frontend

* Dash
* Plotly
* HTML/CSS

### Backend

* FastAPI
* Python

### Database

* MySQL

### Data Processing

* Pandas
* Scikit-learn

## Project Structure

```text
finance_anomaly_detector/
│
├── backend/
│   ├── routes/
│   └── app.py
│
├── dashboard/
│   ├── assets/
│   └── app.py
│
├── database/
│   ├── connection.py
│   └── models.py
│
├── data_processing/
│   ├── parser.py
│   ├── categorizer.py
│   └── anomaly_detector.py
│
├── uploads/
├── .env
├── requirements.txt
└── README.md
```

## Workflow

1. User uploads a bank statement.
2. Backend parses transaction data.
3. Transactions are categorized automatically.
4. Machine learning model identifies unusual transactions.
5. Results are stored in MySQL.
6. Dashboard displays spending insights and detected anomalies.

## Installation

### Clone Repository

```bash
git clone https://github.com/aishvaryarao/finance_anomaly_detector.git
cd finance_anomaly_detector
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Setup

Create a MySQL database:

```sql
CREATE DATABASE finance_db;
```

Update the `.env` file:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=finance_db
```

## Running the Application

### Start Backend

```bash
python -m backend.app
```

Backend runs at:

```text
http://localhost:8000
```

API Documentation:

```text
http://localhost:8000/docs
```

### Start Dashboard

```bash
python dashboard/app.py
```

Dashboard runs at:

```text
http://localhost:8050
```

## Sample Output

The dashboard provides:

* Total Transactions
* Total Spending
* Detected Anomalies
* Category Breakdown Chart
* Spending Trend Visualization
* Recent Anomalies Table

## Future Enhancements

* PDF bank statement support
* User authentication system
* Advanced anomaly detection models
* Export reports to PDF and Excel
* Multi-user support
* Cloud deployment

## Author

**Aishvarya V**

