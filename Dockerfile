# pull official base image
FROM python:3.9-buster

LABEL maintainer="Enes Gulakhmet <wwho.mann.3@gmail.com>"

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN pip install pipenv --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY Pipfile .
COPY Pipfile.lock .

RUN if [ "$INSTALL_DEV_REQUIREMENTS" = "false" ]; then \
      pipenv install --system --deploy; \
    else \
      pipenv install --dev --system --deploy; \
    fi

# add app
COPY . .
