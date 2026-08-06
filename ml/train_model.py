# ml/train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from pathlib import Path

def load_data(csv_path: str):
    df = pd.read_csv(csv_path)
    feature_df = df.drop(columns=['url', 'label'])
    numeric_cols = feature_df.select_dtypes(include=[np.number]).columns.tolist()
    X = feature_df[numeric_cols].values
    y = (df['label'] == 'bad').astype(int).values
    return X, y, numeric_cols

def main():
    csv_path = Path(__file__).parent / "data" / "urlset.csv"
    print(f"Loading data from {csv_path}...")
    X, y, feature_names = load_data(csv_path)
    print(f"Feature matrix shape: {X.shape}, Labels shape: {y.shape}")
    print(f"Using features: {feature_names}")

    # Split data (stratify to keep class balance)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train Decision Tree
    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.2f}")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))

    # Save model and feature names
    model_path = Path(__file__).parent / "models" / "phishing_model.joblib"
    joblib.dump({'model': clf, 'feature_names': feature_names}, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()
