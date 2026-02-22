"""
Model Retraining & Versioning Pipeline
=======================================
- Trains a new RandomForest model from fresh data.
- Evaluates precision, recall, accuracy, and F1-score.
- Saves the new model with a timestamped version tag.
- Updates the model registry (model_registry.json).
- Only promotes the new model to 'production' if it improves on the previous best.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score, recall_score, accuracy_score,
    f1_score, classification_report
)
from .data_pipeline import HouseDataPipeline

MODELS_DIR = "models"
REGISTRY_PATH = os.path.join(MODELS_DIR, "model_registry.json")
PRODUCTION_SYMLINK = os.path.join(MODELS_DIR, "recommender.joblib")


def load_registry() -> dict:
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)
    return {"versions": [], "production": None}


def save_registry(registry: dict):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def retrain_and_version() -> dict:
    """
    Full retraining pipeline with versioning:
    1. Fetch & process data.
    2. Train RandomForestClassifier.
    3. Evaluate against test split.
    4. Save versioned model artifact.
    5. Promote to production if metrics improve.
    6. Return evaluation report.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)
    registry = load_registry()

    print("=" * 50)
    print("  ML Retraining & Versioning Pipeline")
    print("=" * 50)

    # --- 1. Data ---
    pipeline = HouseDataPipeline()
    X_train, X_test, y_train, y_test = pipeline.process()
    print(f"[Data]     Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")

    # --- 2. Train ---
    model = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    print("[Training] RandomForest fit complete.")

    # --- 3. Evaluate ---
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy":  round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall":    round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1_score":  round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
    }
    print("\n[Metrics]")
    for k, v in metrics.items():
        print(f"  {k:<12}: {v}")
    print("\n" + classification_report(y_test, y_pred, zero_division=0))

    # --- 4. Save versioned artifact ---
    version_tag = datetime.utcnow().strftime("v%Y%m%d_%H%M%S")
    versioned_path = os.path.join(MODELS_DIR, f"recommender_{version_tag}.joblib")
    joblib.dump(model, versioned_path)
    print(f"[Saved]    {versioned_path}")

    version_entry = {
        "version": version_tag,
        "path": versioned_path,
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "metrics": metrics,
        "promoted": False
    }

    # --- 5. Promote to production if best F1 ---
    current_best_f1 = 0.0
    if registry["production"]:
        for v in registry["versions"]:
            if v["version"] == registry["production"]:
                current_best_f1 = v["metrics"].get("f1_score", 0.0)
                break

    if metrics["f1_score"] >= current_best_f1:
        # Replace the production model symlink/file
        if os.path.exists(PRODUCTION_SYMLINK):
            os.remove(PRODUCTION_SYMLINK)
        joblib.dump(model, PRODUCTION_SYMLINK)
        registry["production"] = version_tag
        version_entry["promoted"] = True
        print(f"[Promoted] {version_tag} → production (F1: {metrics['f1_score']} ≥ {current_best_f1})")
    else:
        print(f"[Skipped]  Not promoted — current F1 {metrics['f1_score']} < best {current_best_f1}")

    registry["versions"].append(version_entry)
    save_registry(registry)

    return {
        "version": version_tag,
        "promoted": version_entry["promoted"],
        "metrics": metrics,
        "registry_path": REGISTRY_PATH
    }


if __name__ == "__main__":
    result = retrain_and_version()
    print("\n[Done]", result)
