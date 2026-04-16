#1. Python's base image is perfect.
FROM python:3.10-slim

# 2. 🚀 Special part: Installing Docker CLI inside the container 
# (so your Django code can run Docker commands from inside)
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean

# 3. Python settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Create directory for the project
WORKDIR /app

# 5. Copy requirements and install all dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Copy all project code
COPY . /app/

# 7. Expose the port
EXPOSE 8000

# 8. Command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]