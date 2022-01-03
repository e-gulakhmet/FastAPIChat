FROM python:3.9-buster

LABEL maintainer="Enes Gulakhmet <wwho.mann.3@gmail.com>"

RUN apt-get update -y

# create the appropriate directories
ENV HOME=/usr/src/app
WORKDIR $HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY requirements.txt /usr/src/app/requirements.txt

# install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /usr/src/app/requirements.txt

# copy project
COPY . /usr/src/app

EXPOSE 80
