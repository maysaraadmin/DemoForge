import bentoml
from bentoml.io import JSON
import numpy as np

# Create a simple BentoML service
@bentoml.service()
class DemoService:

    @bentoml.api
    def predict(self, input_data: JSON) -> JSON:
        """Simple prediction service for demo purposes"""
        return {"result": "Hello from BentoML!", "input": input_data}

# Save the service to create a bento
if __name__ == "__main__":
    # Create a simple bento for serving
    bentoml.build(
        "demo_service:latest",
        labels={"demo": "true"},
        description="Demo BentoML service"
    )
