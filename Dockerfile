FROM python:3.10.12

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt