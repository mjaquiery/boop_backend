FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install postgresql-client for healthchecking
RUN apt-get update && \
    apt-get install -y \
    	postgresql-client \
    	build-essential libssl-dev libffi-dev python3-dev python-dev-is-python3 && \
    apt-get autoremove && \
    apt-get autoclean

RUN mkdir -p /usr/app
WORKDIR /usr/app
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /usr/app
RUN cp -rf /usr/local/lib/python3.10/site-packages/rest_framework/static/* /static || true
