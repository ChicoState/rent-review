# syntax=docker/dockerfile:1.4

FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /rentreview
COPY requirements.txt /rentreview
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . /rentreview
