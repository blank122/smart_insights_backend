import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from models.habit_logs import HabitLog

class ClusteringService:
    def __init__(self, db_session):
        self.features = ['Sleep_Hours', 'Steps', 'Screen_Time', 'Mood', 'Productivity']
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.db = db_session
        self._train_from_db()

    def _train_from_db(self):
        # 1. Query all history from the SQLite table
        query = self.db.query(HabitLog).statement
        df = pd.read_sql(query, self.db.bind)

        if df.empty:
            print("⚠️ Database is empty. Model cannot be trained.")
            return

        # 2. Train on the full history (CSV data + any new logs)
        X_scaled = self.scaler.fit_transform(df[self.features])
        self.model.fit(X_scaled)

    def predict(self, data_dict):
        # The prediction logic remains the same
        input_data = np.array([[
            data_dict['sleep'], data_dict['steps'], 
            data_dict['screen'], data_dict['mood'], data_dict['prod']
        ]])
        scaled_input = self.scaler.transform(input_data)
        cluster_id = int(self.model.predict(scaled_input)[0])
        
        cluster_map = {0: "Burnout Risk", 1: "Healthy/Balanced", 2: "High-Productivity"}
        return cluster_map.get(cluster_id)

    def get_training_stats(self):
        """Returns the centroids and quality metrics of the model."""
        # The centroids are the 'prototypes' for each cluster
        centroids = self.scaler.inverse_transform(self.model.cluster_centers_)
        
        stats = {
            "inertia": float(self.model.inertia_),
            "n_features": self.model.n_features_in_,
            "clusters": {}
        }

        cluster_map = {0: "Burnout Risk", 1: "Healthy/Balanced", 2: "High-Productivity"}

        for i, center in enumerate(centroids):
            stats["clusters"][cluster_map[i]] = {
                "avg_sleep": round(center[0], 2),
                "avg_steps": round(center[1], 0),
                "avg_screen_time": round(center[2], 2),
                "avg_mood": round(center[3], 1),
                "avg_productivity": round(center[4], 1)
            }
        
        return stats