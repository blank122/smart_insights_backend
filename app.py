from fastapi import FastAPI
from api.router import router as habit_router
from db.database import engine
from models.habit_logs import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Habit Insights API")

# Include the routes from the api folder
app.include_router(habit_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "Active", "version": "1.0.0"}