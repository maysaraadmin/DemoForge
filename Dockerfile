FROM python:3.9-slim

WORKDIR /app

# Copy the demo service
COPY demo_service.py .

# Install any required dependencies (none needed for this simple service)
# RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "demo_service.py"]
