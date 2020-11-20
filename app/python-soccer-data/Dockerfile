FROM python:3.8


COPY requirements.txt ./
COPY config/config.json /usr/app/config/soccer_data_config.json
COPY data/init/* /usr/app/data/init/
RUN pip3 install -r requirements.txt
WORKDIR /usr/app/src
COPY src/* ./

