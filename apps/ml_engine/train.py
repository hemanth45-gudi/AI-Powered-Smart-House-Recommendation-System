import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, accuracy_score, classification_report
from data_pipeline import HouseDataPipeline

class ModelTrainer:
    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        self.model_path = os.path.join(model_dir, "recommender.joblib")
        self.pipeline = HouseDataPipeline()
        
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

    def train_and_evaluate(self):
        """
        Runs the full training pipeline:
        1. Process data from the pipeline.
        2. Train a Random Forest model.
        3. Evaluate performance metrics.
        4. Persist the model.
        """
        print("--- Starting ML Training & Evaluation Pipeline ---")
        
        # 1. Get processed data
        X_train, X_test, y_train, y_test = self.pipeline.process()
        
        print(f"Training on {X_train.shape[0]} samples...")
        
        # 2. Initialize and train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # 3. Make predictions
        y_pred = model.predict(X_test)
        
        # 4. Calculate metrics
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        accuracy = accuracy_score(y_test, y_pred)
        
        print("\n--- Performance Metrics ---")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"Accuracy:  {accuracy:.4f}")
        
        print("\nDetailed Classification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        # 5. Persist the model
        joblib.dump(model, self.model_path)
        print(f"\nModel successfully saved to: {self.model_path}")
        
        return {
            "precision": precision,
            "recall": recall,
            "accuracy": accuracy
        }

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train_and_evaluate()
