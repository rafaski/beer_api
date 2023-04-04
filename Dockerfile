FROM python:3.10

# Set the working directory to /app/app
WORKDIR /code

# Copy requirements.txt
COPY requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the entire app directory into the container
COPY ./app /code/app

# Define environment variable
ENV POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=postgres \
    POSTGRES_SERVER=host.docker.internal \
    POSTGRES_PORT=5432 \
    POSTGRES_DB=db

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8080"]