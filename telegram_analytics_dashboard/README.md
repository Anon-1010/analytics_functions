# Telegram Analytics Dashboard

## Problem Statement
This project proposes 20 analytics for Telegram group data and 30 dashboard visualizations for admins. The Flask app serves as the backend for the dashboard.

## Steps to Run the Code
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project folder:
   ```bash
   cd telegram-analytics-dashboard
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```bash
   python app.py
   ```
5. Access the app at `http://127.0.0.1:5000`.

## Input and Output
- Input: Telegram group data (schema provided).
- Output: Analytics and visualizations for admin dashboard.

## Docker Instructions
1. Build the Docker image:
   ```bash
   docker build -t telegram-analytics .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 telegram-analytics
   ```