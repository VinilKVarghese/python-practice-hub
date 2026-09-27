# Use Python image
FROM python:3.14-slim

# Set the working directory
WORKDIR /app

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn

# Copy the Python program
COPY Vinil_module7_3.py .

# Start the FastAPI server
CMD ["uvicorn", "Vinil_module7_3:app", "--host", "0.0.0.0", "--port", "8000"]


