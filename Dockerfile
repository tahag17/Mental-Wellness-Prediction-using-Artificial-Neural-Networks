# Use an official Python image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project into the container
COPY . .

# Expose the port your app runs on
EXPOSE 8080

# Run the FastAPI app
CMD ["uvicorn", "pyapi.api:app", "--host", "0.0.0.0", "--port", "8080"]
