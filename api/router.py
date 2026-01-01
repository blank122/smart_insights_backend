from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.habit_logs import HabitLog
from services.clustering_services import ClusteringService # Use your actual filename

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