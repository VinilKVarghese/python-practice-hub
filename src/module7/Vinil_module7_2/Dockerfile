# Use Python base image
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application
COPY Vinil_module7_2.py .

# Expose Streamlit port
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "Vinil_module7_2.py", "--server.address=0.0.0.0"]