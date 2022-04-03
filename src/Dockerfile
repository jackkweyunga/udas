##### Django docker file template


FROM python:3.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY . /app

WORKDIR app

# installing dev dependencies
RUN python3 -m venv env \
    && . ./env/bin/activate \
    && pip3 install --upgrade --user pip \
    && pip3 install --no-cache-dir --user psycopg2-binary \
    && pip3 install --no-cache-dir --user -r requirements.txt

# chown all the files to the app user
RUN chown -R janjas:janjas .

# change to the app user
USER janjas

# initial commands
# depend on the database --> never to be run alone. use docker-compose

CMD . ./env/bin/activate \
    && python manage.py collectstatic -v 2 --noinput \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python csu.py \
    && daphne -b 0.0.0.0 -p 8000 auth.asgi:application


# jek
