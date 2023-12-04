ARG DOCKER_PLATFORM=$TARGETPLATFORM
FROM --platform=$DOCKER_PLATFORM python:3.11.4-bookworm

ENV PYTHONBUFFERED 1

# Create directory
RUN mkdir /code

# Set the working directory to /code
WORKDIR /code

# Mirror the current directory to the working directory for hotreloading
ADD . /code/

# Install pipenv
RUN pip install --no-cache-dir -r requirements.txt

# Make migrations
RUN python equipment_tracker/manage.py makemigrations

# Run custom migrate
RUN python equipment_tracker/manage.py migrate

# Generate DRF Spectacular Documentation
RUN python equipment_tracker/manage.py spectacular --color --file equipment_tracker/schema.yml

# Expose port 8000 for the web server
EXPOSE 8000
