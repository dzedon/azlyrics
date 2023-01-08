FROM python:3.11-alpine
WORKDIR /usr/src
COPY requirements.txt ./
RUN apk update \
    && apk add --virtual build_deps gcc g++ make musl-dev libffi-dev postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD gunicorn -w 4 --reload 'app:app'