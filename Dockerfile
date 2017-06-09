# Use an official Python runtime as a base image
FROM python:latest

RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN apt-get update && apt-get install -y cron


# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# run scrapper every *n 
RUN echo "starting Cron"

RUN echo "* * * * *  /app/cron.sh" | crontab -

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

