FROM python:3.13.2-alpine3.21

WORKDIR '/app'

RUN apk add --no-cache linux-headers g++

RUN pip install requirements.txt

COPY ./ ./

RUN addgroup -S uwsgi && adduser -S uwsgi -G uwsgi

USER uwsgi

CMD ["uwsgi", "--ini", "app.ini"]