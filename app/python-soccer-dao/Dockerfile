FROM python:3.8-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt ./
COPY config.ini /usr/app/config/soccer_dao_config.ini
RUN pip install -r requirements.txt
WORKDIR /usr/app/src
COPY src/* ./
COPY queries/* ./

#CMD ["python", "src/init.py"]