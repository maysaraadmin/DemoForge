#!/usr/bin/env python3
"""
BentoML Service Definition
Demo machine learning service for prediction
"""
import numpy as np
import bentoml
from bentoml.io import JSON

# Load the trained model (this would normally be done automatically by BentoML)
@bentoml.service()
class MLService:

    @bentoml.api
    def predict(self, input_data: JSON) -> JSON:
        """Make predictions on input data"""
        # Convert input to numpy array
        data = np.array(input_data.get('data', []))

        if len(data) == 0:
            return {"error": "No data provided", "example": {"data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}}

        # Reshape if needed
        if len(data.shape) == 1:
            data = data.reshape(1, -1)

        # Simple demo prediction logic (replace with actual model)
        prediction = (data.sum(axis=1) > 0).astype(int)

        return {
            "prediction": prediction.tolist(),
            "confidence": np.abs(data.sum(axis=1)).tolist(),
            "model": "demo_model_v1.0",
            "input_shape": data.shape
        }

    @bentoml.api
    def health(self) -> JSON:
        """Health check endpoint"""
        return {
            "status": "healthy",
            "model": "demo_model",
            "version": "1.0.0"
        }

    @bentoml.api
    def info(self) -> JSON:
        """Model information endpoint"""
        return {
            "name": "Demo ML Service",
            "description": "A sample BentoML service for demonstration",
            "input_format": "JSON with 'data' array",
            "output_format": "JSON with prediction results",
            "endpoints": {
                "predict": "POST /predict",
                "health": "GET /health",
                "info": "GET /info"
            }
        }
