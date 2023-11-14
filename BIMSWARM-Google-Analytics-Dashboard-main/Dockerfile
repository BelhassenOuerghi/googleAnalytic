FROM python:latest
LABEL authors="essam"
RUN apt-get update

RUN apt-get install -y libgdal-dev
RUN  apt install gdal-bin python3-gdal -y
COPY . .
EXPOSE 8050
RUN pip3 install -r requirements.txt
ENTRYPOINT python main.py