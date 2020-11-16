FROM python:3.8-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt
WORKDIR /usr/app/src
COPY src/* ./
COPY queries/* ./

CMD ["python", "init.py"]
#CMD ["python", "src/init.py"]