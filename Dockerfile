FROM python:3.9
RUN mkdir /code
RUN apt-get update -y
RUN apt-get upgrade -y
COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code
CMD gunicorn website.wsgi:application --bind 0.0.0.0:8000