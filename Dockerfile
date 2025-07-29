# Build stage
FROM python:3.13-slim

WORKDIR /app

# Installing Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY src/ src/

# Expose Port On FastAPI Running
EXPOSE 8000

# Run the FastAPI Application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]