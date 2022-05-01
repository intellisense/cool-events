# Pull official base image
FROM python:latest

ENV APP_HOME=/usr/src/app

# Set work directory
WORKDIR $APP_HOME

# Installing build dependencies
RUN apt-get update && apt-get install -y netcat

# Upgrade pip
RUN pip install --upgrade pip

# Copy project
COPY . $APP_HOME

RUN chmod +x $APP_HOME/bin/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/app/bin/entrypoint.sh"]
