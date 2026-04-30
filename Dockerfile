FROM python:3.10-slim

COPY ./src/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./src/ ./
