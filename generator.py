import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Settings
start_date = datetime(2025, 10, 1)
days = 92 # Approx 3 months
data = []

for i in range(days):
    current_date = start_date + timedelta(days=i)
    is_weekend = current_date.weekday() >= 5
    day_of_month = current_date.day
    
    # --- HEALTH & HABITS ---
    if is_weekend:
        sleep = np.random.uniform(7.5, 8.5)
        steps = np.random.randint(4000, 6001)
        screen_time = np.random.uniform(6, 10)
        productivity = np.random.randint(2, 6) # Lower on weekends
        mood = np.random.randint(4, 6)         # Higher on weekends
    else:
        sleep = np.random.uniform(5.5, 6.5)
        steps = np.random.randint(10000, 15001)
        screen_time = np.random.uniform(9, 13) # Work + Personal
        productivity = np.random.randint(6, 10)
        mood = np.random.randint(3, 5)

    # Workout: 3 times a week (logic: Mon, Wed, Sat)
    workout = 1 if current_date.weekday() in [0, 2, 5] else 0

    # --- FINANCES ---
    salary_in = 32500 if day_of_month in [15, 30] else 0
    
    # Fixed daily averages or specific hit dates
    rent = 13000 if day_of_month == 1 else 0
    insurance = 5500 if day_of_month == 5 else 0
    savings = 10000 if day_of_month in [15, 30] else 0 # Split logic
    
    # Fluctuating expenses
    transport = np.random.uniform(145, 230) if not is_weekend else np.random.uniform(0, 100)
    groceries = np.random.uniform(500, 1200) if current_date.weekday() == 5 else 0 # Weekly shop
    leisure = np.random.uniform(500, 1500) if is_weekend else 0
    
    data.append([
        current_date.strftime('%Y-%m-%d'), round(sleep, 1), steps, round(screen_time, 1),
        workout, mood, productivity, salary_in, round(transport, 2), 
        round(groceries, 2), round(leisure, 2), rent, insurance
    ])

# Create DataFrame
columns = [
    'Date', 'Sleep_Hours', 'Steps', 'Screen_Time', 'Workout', 'Mood', 
    'Productivity', 'Salary_In', 'Exp_Transport', 'Exp_Groceries', 
    'Exp_Leisure', 'Exp_Rent', 'Exp_Insurance'
]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv('smart_habit_data.csv', index=False)
print("Dataset 'smart_habit_data.csv' created successfully!")