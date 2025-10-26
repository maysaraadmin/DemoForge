#!/usr/bin/env python3
"""
Simple Flask-based ML Service
Alternative to BentoML for demo purposes
"""
from flask import Flask, request, jsonify
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

# Initialize Flask app
app = Flask(__name__)

# Simple trained model (for demo purposes)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(np.random.randn(100, 5), np.random.randint(0, 2, 100))

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "flask_ml_service",
        "model": "random_forest_demo"
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    try:
        data = request.get_json()

        if not data or 'data' not in data:
            return jsonify({
                "error": "No data provided",
                "example": {"data": [1, 2, 3, 4, 5]}
            }), 400

        input_data = np.array(data['data'])

        # Reshape if needed
        if len(input_data.shape) == 1:
            input_data = input_data.reshape(1, -1)

        # Make prediction
        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)

        return jsonify({
            "prediction": prediction.tolist(),
            "probability": probability.tolist(),
            "input_shape": input_data.shape,
            "model": "random_forest_demo"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/info', methods=['GET'])
def info():
    """Service information endpoint"""
    return jsonify({
        "name": "Flask ML Service",
        "description": "Simple Flask-based ML prediction service",
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /predict",
            "info": "GET /info"
        },
        "input_format": "JSON with 'data' array",
        "output_format": "JSON with prediction results"
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "message": "Flask ML Service",
        "status": "running",
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /predict",
            "info": "GET /info"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')

    print(f"🚀 Starting Flask ML Service on {host}:{port}")
    print("📊 Available endpoints:")
    print("  • GET  /health - Health check")
    print("  • POST /predict - Make predictions")
    print("  • GET  /info - Service information")
    print("  • GET  / - Service overview")

    app.run(host=host, port=port, debug=True)
