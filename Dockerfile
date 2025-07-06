# Use official Python image
FROM python:3.12-slim

# Set working dir
WORKDIR /app

# Copy dependency requirements file and install them
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose Flask port
EXPOSE 5000

# Start Flask app via Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]

