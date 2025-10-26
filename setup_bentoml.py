#!/usr/bin/env python3
"""
BentoML Service Initialization Script
Sets up and starts the BentoML demo service
"""
import subprocess
import sys
import os

def build_bento_service():
    """Build the BentoML service"""
    print("🔨 Building BentoML service...")

    try:
        # Change to the project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Build the BentoML service
        result = subprocess.run([
            'bentoml', 'build',
            'demo_bentoml_service:latest',
            '--description', 'Demo BentoML service for ML predictions'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ BentoML service built successfully!")
            return True
        else:
            print(f"❌ Failed to build BentoML service: {result.stderr}")
            return False

    except FileNotFoundError:
        print("❌ BentoML not found. Please install: pip install bentoml")
        return False
    except Exception as e:
        print(f"❌ Error building service: {e}")
        return False

def start_bentoml_services():
    """Start BentoML services using docker-compose"""
    print("🚀 Starting BentoML services...")

    try:
        # Change to the project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Start services
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.bentoml.yml', 'up', '-d'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ BentoML services started successfully!")
            print("📊 Services available at:")
            print("  • BentoML API: http://localhost:5000")
            print("  • BentoML Dashboard: http://localhost:5001")
            print("  • Redis: localhost:6379")
            return True
        else:
            print(f"❌ Failed to start services: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error starting services: {e}")
        return False

def test_service():
    """Test the BentoML service"""
    print("🧪 Testing BentoML service...")

    try:
        import requests
        import json

        # Test health endpoint
        health_response = requests.get("http://localhost:5000/health", timeout=10)

        if health_response.status_code == 200:
            print("✅ Health check passed")

            # Test prediction endpoint
            test_data = {"data": [1, 2, 3, 4, 5]}
            predict_response = requests.post(
                "http://localhost:5000/predict",
                json=test_data,
                timeout=10
            )

            if predict_response.status_code == 200:
                result = predict_response.json()
                print(f"✅ Prediction test successful: {result}")
                return True
            else:
                print(f"❌ Prediction test failed: {predict_response.status_code}")
                return False
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Service test failed (service may still be starting): {e}")
        print("💡 Try again in a few moments...")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main initialization function"""
    print("🤖 DemoForge BentoML Setup")
    print("=" * 40)

    # Step 1: Build service
    if not build_bento_service():
        sys.exit(1)

    # Step 2: Start services
    if not start_bentoml_services():
        sys.exit(1)

    # Step 3: Wait a bit for services to start
    print("⏳ Waiting for services to initialize...")
    import time
    time.sleep(10)

    # Step 4: Test service
    test_service()

    print("\n🎉 BentoML setup complete!")
    print("You can now access your ML services:")
    print("  • http://localhost:5000 (API)")
    print("  • http://localhost:5001 (Dashboard)")

if __name__ == "__main__":
    main()
