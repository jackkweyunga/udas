##### Django docker file template


FROM python:3.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY . /app

WORKDIR app

# installing dev dependencies
RUN apt-get update \
    && apt-get install -y \
        libpq-dev \
        gcc \
    && apt-get clean \
    && python3 -m venv env \
    && . ./env/bin/activate \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt

CMD . ./env/bin/activate \
    && python manage.py collectstatic -v 2 --noinput \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python csu.py \
    && daphne -b 0.0.0.0 -p 8000 auth.asgi:application


# jek
