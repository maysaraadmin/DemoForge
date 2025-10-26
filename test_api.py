#!/usr/bin/env python3
"""
Test Flask ML API
"""
import requests
import json

def test_api():
    print("🧪 Testing Flask ML API...")

    # Test health endpoint
    try:
        response = requests.get('http://localhost:5002/health', timeout=10)
        print(f"✅ Health Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        # Test prediction endpoint
        test_data = {'data': [1, 2, 3, 4, 5]}
        response = requests.post('http://localhost:5002/predict', json=test_data, timeout=10)
        print(f"✅ Prediction Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        # Test info endpoint
        response = requests.get('http://localhost:5002/info', timeout=10)
        print(f"✅ Info Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        print("\n🎉 Flask ML API is working perfectly!")

    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    test_api()
