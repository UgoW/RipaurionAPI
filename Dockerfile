FROM python:3.12.11-alpine3.21

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

# Use uvicorn to run RipaurionAPI 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]