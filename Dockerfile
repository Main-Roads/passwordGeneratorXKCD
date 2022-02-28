# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./services/web .


# Copy the VERSION file
COPY VERSION project/
COPY config.yaml project/
HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost:5000/version || exit 1

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
