##### Django docker file template

##### variables
# janjas --> the name of the user in the image os
# auth --> the name of your django project
# auth --> the name of your django project


FROM python:3.8.3-alpine AS base

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S janjas && adduser -S janjas -G janjas

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/src
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

COPY ./requirements.txt .

# installing dev dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add openssl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && python -m venv env \
    && source ./env/bin/activate \
    && pip install --upgrade pip  \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg libffi-dev \
    && pip install -r requirements.txt \
    && apk del build-deps

# copying the project folder into the image
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R janjas:janjas $APP_HOME

# change to the app user
USER janjas

# initial commands
# depend on the database --> never to be run alone. use docker-compose

CMD source ./env/bin/activate \
    && python manage.py collectstatic -v 2 --noinput \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python csu.py \
    && daphne -b 0.0.0.0 -p 8000 auth.asgi:application


# jek