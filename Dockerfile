# Use an official Python runtime as a base image
FROM python:3.10-slim

# Install Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Expose the port that Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["poetry", "run", "python3", "app.py"]