import pandas as pd
import numpy as np
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --- FIXED IMPORTS BASED ON YOUR FOLDERS ---
from db.database import SessionLocal, engine
from models.habit_logs import HabitLog, Base # Corrected path to habit_logs.py

# --- DATABASE CREATION ---
# This ensures the habits.db is created using the Base from your models folder
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ML INITIALIZATION ---
# Fixed the path to look inside the /data folder
csv_path = 'data/smart_habit_data.csv'
df_initial = pd.read_csv(csv_path)

features = ['Sleep_Hours', 'Steps', 'Screen_Time', 'Mood', 'Productivity']
X = df_initial[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = KMeans(n_clusters=3, random_state=42, n_init=10)
model.fit(X_scaled)

# --- API ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "Online", "database": "SQLite Connected"}

@app.post("/log-habit/")
def create_habit_entry(
    sleep: float,
    steps: int,
    screen: float,
    mood: int,
    prod: int,
    db: Session = Depends(get_db)
):
    # 1. ML Prediction Logic
    input_data = np.array([[sleep, steps, screen, mood, prod]])
    scaled_input = scaler.transform(input_data)
    cluster_id = int(model.predict(scaled_input)[0])

    cluster_map = {
        0: "Burnout Risk",
        1: "Healthy/Balanced",
        2: "High-Productivity"
    }
    cluster_name = cluster_map.get(cluster_id)

    # 2. SAVE TO SQLITE
    # Note: Use HabitLog (the class name) imported from models.habit_logs
    new_entry = HabitLog(
        sleep_hours=sleep,
        steps=steps,
        screen_time=screen,
        mood=mood,
        productivity=prod,
        cluster_label=cluster_name
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "message": "Habit logged and analyzed!",
        "analysis": {
            "cluster": cluster_name,
            "id": new_entry.id
        }
    }

@app.get("/history/")
def get_history(db: Session = Depends(get_db)):
    return db.query(HabitLog).all()