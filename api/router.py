from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.habit_logs import HabitLog
from services.clustering_services import ClusteringService # Use your actual filename
from services.forecaster import ForecasterService

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/log-habit/")
def log_habit(sleep: float, steps: int, screen: float, mood: int, prod: int, db: Session = Depends(get_db)):
    # Initialize service by passing the DB session 'db'
    service = ClusteringService(db)
    
    category = service.predict({
        'sleep': sleep, 'steps': steps, 'screen': screen, 'mood': mood, 'prod': prod
    })

    # Save to DB logic...
    new_entry = HabitLog(
        Sleep_Hours=sleep, Steps=steps, Screen_Time=screen,
        Mood=mood, Productivity=prod, cluster_label=category
    )
    db.add(new_entry)
    db.commit()
    return {"category": category, "status": "saved"}

@router.get("/model-stats/")
def get_model_results(db: Session = Depends(get_db)):
    # Pass 'db' here too
    service = ClusteringService(db)
    return service.get_training_stats()

@router.get("/forecast/")
def get_habit_forecast(
    time_period: str = Query("3 months", description="Options: weekly, monthly, 3 months, 6 months, 1 year"),
    db: Session = Depends(get_db)
):
    # Mapping dropdown strings to actual days
    period_mapping = {
        "weekly": 7,
        "monthly": 30,
        "3 months": 90,
        "6 months": 180,
        "1 year": 365
    }
    
    # Default to 90 days if the input doesn't match
    days = period_mapping.get(time_period.lower(), 90)
    
    forecaster = ForecasterService(db)
    return forecaster.forecast_trends(days_ahead=days)