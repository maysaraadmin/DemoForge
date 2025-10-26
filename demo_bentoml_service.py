#!/usr/bin/env python3
"""
BentoML Demo Service
Simple ML service for testing BentoML functionality
"""
import bentoml
from bentoml.io import JSON
import numpy as np

@bentoml.service()
class DemoMLService:

    @bentoml.api
    def predict(self, input_data: JSON) -> JSON:
        """Make predictions on input data"""
        data = np.array(input_data.get('data', []))

        if len(data) == 0:
            return {"error": "No data provided", "example": {"data": [1, 2, 3, 4, 5]}}

        # Simple demo prediction (sum > 0 = class 1, else class 0)
        prediction = (data.sum() > 0).astype(int)

        return {
            "prediction": int(prediction),
            "confidence": float(abs(data.sum())),
            "input_sum": float(data.sum()),
            "model": "demo_model_v1.0"
        }

    @bentoml.api
    def health(self) -> JSON:
        """Health check endpoint"""
        return {"status": "healthy", "model": "demo_model"}

    @bentoml.api
    def info(self) -> JSON:
        """Model information"""
        return {
            "name": "Demo ML Service",
            "type": "binary_classification",
            "input_format": "JSON array of numbers",
            "output_format": "prediction probability"
        }
