# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Run the application with waitress
CMD ["waitress-serve", "--port=8080", "app:app"]
