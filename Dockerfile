FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8080

# Run the application with Gunicorn
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:${PORT:-8080}", "app:app"]
