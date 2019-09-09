FROM ubuntu:18.04

MAINTAINER German Novikov <german.novikov@phystech.edu>

## Base packages for ubuntu
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        wget \
        make \
        python3-pip \
        python3-setuptools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir --requirement /tmp/requirements.txt

COPY ./ /root/shared/open_data/

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

