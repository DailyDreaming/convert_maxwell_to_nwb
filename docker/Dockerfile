FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ENDPOINT_URL="https://s3-west.nrp-nautilus.io"

RUN apt update && apt upgrade -y
RUN apt-get install python3 python3-dev python3-distutils python3-pip python3-apt -y
RUN python3 -m pip install neuroconv[maxwell]

COPY run.py /bin/run.py
