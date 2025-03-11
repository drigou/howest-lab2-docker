FROM python:3.12.9-alpine3.21 as build-image

WORKDIR '/app'

RUN apk add --no-cache linux-headers g++

COPY ./requirements.txt ./

RUN pip wheel --wheel-dir=/root/wheels -r requirements.txt

# In your Dockerfile, you can now define a production-ready image by utilizing 
# the intermediate build image in the following manner:

FROM python:3.12.9-alpine3.21 as production-image

WORKDIR '/app'

COPY --from=build-image /root/wheels /root/wheels

COPY --from=build-image /app/requirements.txt ./

RUN pip install --no-index --find-links=/root/wheels -r requirements.txt

COPY ./ ./

#Hmmmmm?

RUN addgroup -S uwsgi && adduser -S uwsgi -G uwsgi

USER uwsgi

CMD ["uwsgi", "--ini", "app.ini"]