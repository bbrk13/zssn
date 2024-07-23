# Existing Dockerfile content
FROM python:3.8

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]