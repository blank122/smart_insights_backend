import pandas as pd
from db.database import engine
from models.habit_logs import HabitLog, Base

# 1. Create the tables in SQLite
Base.metadata.create_all(bind=engine)

# 2. Load the CSV
df = pd.read_csv('data/smart_habit_data.csv')

# 3. Push the CSV data into the SQLite table
df.to_sql('habit_logs', con=engine, if_exists='append', index=False)

print("SQLite database initialized and CSV data imported!")