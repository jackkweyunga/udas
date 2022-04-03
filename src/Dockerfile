##### Django docker file template

##### variables
# janjas --> the name of the user in the image os
# auth --> the name of your django project
# auth --> the name of your django project


FROM python:3.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY . /app

WORKDIR app

# installing dev dependencies
RUN python -m venv env \
    && source ./env/bin/activate \
    && pip install --upgrade pip \
    && pip install --no-cache-dir psycopg2-binary \
    && pip install --no-cache-dir --user -r requirements.txt

# chown all the files to the app user
RUN chown -R janjas:janjas .

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
