FROM python:3.11-alpine

WORKDIR /usr/src

RUN pip install pipenv
COPY Pipfile ./
COPY Pipfile.lock ./

RUN apk update \
    && apk add --virtual build_deps gcc g++ make musl-dev libffi-dev postgresql-dev

RUN pipenv install --system --dev --deploy

COPY .. .

CMD gunicorn -w 4 --reload 'app:app'