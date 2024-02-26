FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ENDPOINT_URL="https://s3-west.nrp-nautilus.io"

RUN python -m pip install braingeneerspy neuroconv boto3

COPY run.py /tmp/run.py

ENTRYPOINT ['python3', '/tmp/run.py']
