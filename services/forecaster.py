import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from models.habit_logs import HabitLog
from datetime import datetime, timedelta

class ForecasterService:
    def __init__(self, db_session):
        self.db = db_session
        self.metrics = ['Sleep_Hours', 'Steps', 'Screen_Time', 'Mood', 'Productivity']

    def forecast_trends(self, days_ahead=90):
        # 1. Pull data from DB
        query = self.db.query(HabitLog).statement
        df = pd.read_sql(query, self.db.bind)

        if len(df) < 14: # Need at least 2 weeks of data for a meaningful trend
            return {"error": "Not enough data to forecast. Please log at least 14 days."}

        # Convert Date to ordinal (numeric) for regression
        df['Date_Ordinal'] = pd.to_datetime(df['Date']).map(datetime.toordinal)
        X = df[['Date_Ordinal']].values
        
        predictions = {}
        forecast_date = datetime.now() + timedelta(days=days_ahead)
        forecast_date_ordinal = np.array([[forecast_date.toordinal()]])

        for metric in self.metrics:
            y = df[metric].values
            
            # 2. Train a simple Linear Regression for this metric
            model = LinearRegression()
            model.fit(X, y)
            
            # 3. Predict the value X days in the future
            future_val = model.predict(forecast_date_ordinal)[0]
            
            # Calculate the "Slope" (change per day)
            slope = model.coef_[0]
            
            predictions[metric] = {
                "current_avg": round(float(y[-7:].mean()), 2), # Last 7 days avg
                "projected_val": round(float(future_val), 2),
                "trend": "increasing" if slope > 0 else "decreasing",
                "slope_per_month": round(float(slope * 30), 2)
            }

        return {
            "forecast_date": forecast_date.strftime('%Y-%m-%d'),
            "days_ahead": days_ahead,
            "metrics": predictions,
            "summary": self._generate_summary(predictions)
        }

    def _generate_summary(self, preds):
        # Logic to create a human-readable warning
        if preds['Sleep_Hours']['projected_val'] < 5.5:
            return "CRITICAL: If your current trend continues, your sleep will drop to dangerous levels in 3 months."
        if preds['Screen_Time']['projected_val'] > 13:
            return "WARNING: Your screen time is trending toward extreme levels. Risk of severe eye strain."
        return "Your habits are currently stable. Keep maintaining your routine!"