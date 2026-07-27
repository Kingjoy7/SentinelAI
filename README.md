# SentinelAI: AI-Powered Behavioral Anomaly Detection for Cybersecurity

## Overview

SentinelAI is an AI-driven cybersecurity solution that detects behavioral anomalies in enterprise environments using machine learning and explainable AI. The system generates synthetic enterprise activity logs, identifies anomalous user behavior, classifies attack types, and provides an interactive dashboard for security analysts.

---

## Features

- Synthetic enterprise user and activity generation
- Behavioral anomaly detection using Isolation Forest
- Attack classification using Random Forest
- Explainable AI for prediction transparency
- Interactive SOC Dashboard built with Streamlit
- Threat analytics and visualization
- Alert explorer with filtering capabilities

---

## Project Architecture

```
User Profiles
      │
      ▼
Behavior Simulation
      │
      ▼
Attack Injection
      │
      ▼
Feature Engineering
      │
      ▼
Isolation Forest
      │
      ▼
Random Forest
      │
      ▼
Explainability Engine
      │
      ▼
Interactive Dashboard
```

---

## Tech Stack

### Programming Language
- Python

### Machine Learning
- Scikit-learn
- Isolation Forest
- Random Forest

### Data Processing
- Pandas
- NumPy

### Visualization
- Plotly
- Streamlit

### Supporting Libraries
- Faker
- Joblib

---

## Folder Structure

```
SentinelAI
│
├── backend
│   ├── dashboard
│   ├── datasets
│   ├── trained_models
│   ├── feature_engineering.py
│   ├── attack.py
│   ├── eventgen.py
│   └── user_profiles.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Dataset

The project uses a synthetic enterprise dataset generated during runtime.

Dataset Statistics:

- 500 Employees
- 50,000 Security Events
- 6 Attack Categories

Attack Types:

- Data Exfiltration
- Credential Misuse
- Malware Execution
- Privilege Escalation
- Insider Threat
- Unauthorized Access

---

## Machine Learning Pipeline

1. Generate enterprise users
2. Simulate normal behavioral logs
3. Inject malicious attack patterns
4. Perform feature engineering
5. Detect anomalies using Isolation Forest
6. Classify attacks using Random Forest
7. Explain predictions
8. Visualize results on the dashboard

---

## Dashboard Features

- Executive Security Overview
- Threat Distribution
- Attack Analytics
- Alert Explorer
- AI Prediction Explanations
- User Risk Insights

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/SentinelAI.git
cd SentinelAI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run backend/dashboard/app.py
```

---

## Future Scope

- Real-time enterprise log ingestion
- SIEM integration
- Deep learning-based anomaly detection
- Cloud deployment
- Role-based authentication
- Real-time alert notifications

---

## Research References

- MITRE ATT&CK Framework
- NIST Cybersecurity Framework
- OWASP Security Guidelines
- Scikit-learn Documentation
- Streamlit Documentation
- Plotly Documentation
  
---

## License

This project is developed for educational purposes.
