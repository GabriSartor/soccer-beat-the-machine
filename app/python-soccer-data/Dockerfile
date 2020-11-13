FROM python:3.8


COPY requirements.txt ./
RUN pip3 install -r requirements.txt
WORKDIR /usr/app/src
COPY src/* ./

CMD [ "python", "init.py" ]