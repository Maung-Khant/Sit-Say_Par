# ml/train_model.py
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score, train_test_split


def load_data(csv_path: str):
    df = pd.read_csv(csv_path)
    feature_df = df.drop(columns=["url", "label"])
    numeric_cols = feature_df.select_dtypes(include=[np.number]).columns.tolist()
    X = feature_df[numeric_cols].values
    y = (df["label"] == "bad").astype(int).values
    return X, y, numeric_cols


def main():
    csv_path = Path(__file__).parent / "data" / "urlset.csv"
    print(f"Loading data from {csv_path}...")
    X, y, feature_names = load_data(csv_path)
    print(f"Feature matrix shape: {X.shape}, Labels shape: {y.shape}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Random Forest classifier
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced",  # helps with imbalanced dataset
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.2f}")
    print("Classification Report:")
    print(
        classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"])
    )

    # Cross-validation (5-fold)
    cv_scores = cross_val_score(clf, X, y, cv=5)
    print(
        f"Cross-validation Accuracy: {cv_scores.mean():.2f} (+/- {cv_scores.std() * 2:.2f})"
    )

    # Feature importance
    importances = clf.feature_importances_
    for name, importance in sorted(
        zip(feature_names, importances), key=lambda x: x[1], reverse=True
    ):
        print(f"{name}: {importance:.4f}")

    # Save model
    model_path = Path(__file__).parent / "models" / "phishing_model.joblib"
    joblib.dump({"model": clf, "feature_names": feature_names}, model_path)
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    main()
