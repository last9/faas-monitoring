# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./functions/ /app/functions/

# Install any needed packages specified in requirements.txt
RUN cd /app/functions/auto_debit && pip install --no-cache-dir -r requirements.txt

# Define environment variables if needed
# ENV VAR_NAME=VAR_VALUE

# Run your Python script
CMD [ "python", "/app/functions/auto_debit/main.py" ]
