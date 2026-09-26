FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY Vinil_module7_6.py .

EXPOSE 8501

CMD ["streamlit", "run", "Vinil_module7_6.py", "--server.address=0.0.0.0"]

