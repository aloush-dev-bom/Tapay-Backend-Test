# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBUG=False \
    PORT=8000

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the project code into the container
COPY ./TapayBackend/ /code/

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose the port on which the app will run
EXPOSE ${PORT}

# Start the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "TapayBackend.wsgi"]