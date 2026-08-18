# backend/infrastructure/ml_predictor.py
from pathlib import Path
from typing import Dict, Optional

import joblib

MODEL_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "ml"
    / "models"
    / "phishing_model.joblib"
)


class MLPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.load_model()

    def load_model(self):
        if MODEL_PATH.exists():
            data = joblib.load(MODEL_PATH)
            self.model = data["model"]
            self.feature_names = data["feature_names"]
        else:
            self.model = None

    def predict_proba(self, features: Dict) -> Optional[float]:
        """Return probability of phishing (0-1) or None if model unavailable."""
        if self.model is None:
            return None
        # Extract only the features the model was trained on, in correct order
        X = [[features.get(f, 0) for f in self.feature_names]]
        proba = self.model.predict_proba(X)
        return proba[0][1]  # probability of class 1 (phishing)


# Singleton instance
ml_predictor = MLPredictor()
