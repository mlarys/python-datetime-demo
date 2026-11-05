
# Start with an image containing Python 3.12
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Ensure Python output appears immediately in Docker logs
ENV PYTHONUNBUFFERED=1

# Copy and install external Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our Python application
COPY main.py .

# Run the application as a non-root user
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Start the Python program
CMD ["python", "main.py"]
