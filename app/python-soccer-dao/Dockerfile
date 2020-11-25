FROM python:3.8-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev bash

COPY requirements.txt ./
COPY config/config.ini /usr/app/config/config.ini
COPY queries/* /usr/app/queries/

RUN pip install -r requirements.txt

WORKDIR /usr/app/src
COPY src/* ./
COPY entrypoint.sh ./

ENTRYPOINT []
# By default run entrypoint.sh, but if command-line arguments
# are given run those instead:
CMD ["./entrypoint.sh"]