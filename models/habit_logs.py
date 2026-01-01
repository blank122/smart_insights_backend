from sqlalchemy import Column, Integer, Float, String
from db.database import Base

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    Date = Column(String)  # Match the CSV header case
    Sleep_Hours = Column(Float)
    Steps = Column(Integer)
    Screen_Time = Column(Float)
    Workout = Column(Integer)  # <--- Added this
    Mood = Column(Integer)
    Productivity = Column(Integer)
    Salary_In = Column(Float)   # <--- Added this
    Exp_Transport = Column(Float)
    Exp_Groceries = Column(Float)
    Exp_Leisure = Column(Float)
    Exp_Rent = Column(Float)
    Exp_Insurance = Column(Float)
    cluster_label = Column(String, nullable=True)