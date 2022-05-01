# Pull official base image
FROM node:17-alpine

ENV APP_HOME=/usr/src/app

# Set work directory
WORKDIR $APP_HOME

# Copy project
COPY . $APP_HOME

RUN chmod +x $APP_HOME/bin/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/app/bin/entrypoint.sh"]
