FROM python:3.10-slim

COPY ./src/ ./
RUN pip3 install -r requirements.txt
