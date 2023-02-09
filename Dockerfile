# syntax=docker/dockerfile:1.4

FROM python:3.8-slim-buster
EXPOSE 8000
WORKDIR /rentreview
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /rentreview
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
