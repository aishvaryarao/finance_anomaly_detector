import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination, random_state=42)
    
    def detect(self, df: pd.DataFrame, amount_column: str = "amount") -> pd.DataFrame:
        """Detect anomalies in transaction amounts"""
        amounts = df[[amount_column]].values
        predictions = self.model.fit_predict(amounts)
        df["is_anomaly"] = predictions == -1
        return df
    
    def get_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get rows marked as anomalies"""
        return df[df["is_anomaly"] == True]