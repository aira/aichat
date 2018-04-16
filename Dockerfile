# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:16.04
# FROM python:3
#  ENV PYTHONUNBUFFERED 1
#  RUN mkdir /code
#  WORKDIR /code
#  ADD twote_requirements.txt /code/
#  RUN pip install -r twote_requirements.txt
#  ADD . /code/
#  RUN python deploy/openchat/nltk_download.py
#  RUN echo "deb http://http.debian.net/debian jessie-backports main" | \
#       tee --append /etc/apt/sources.list.d/jessie-backports.list > /dev/null
#  RUN apt-get update && \
#   apt-get upgrade -y && \
#   apt-get install -y -t jessie-backports openjdk-8-jdk
# RUN apt-get install -y vim

MAINTAINER Hobson Lane

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
		git python3 python3-dev python3-setuptools python3-pip nginx supervisor sqlite3 \
		python3.5-dev python3-virtualenv build-essential gfortran \
		python-pyaudio python-pyaudio3 && \
	pip3 install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

# create directory for the source code
# RUN mkdir -p /home/docker/code/app/

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-sites-available-default.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.

COPY requirements_base.txt /home/docker/code/app/
RUN pip3 install -r /home/docker/code/app/requirements_base.txt

# add (the rest of) our code
# COPY . /home/docker/code/
COPY . ~/src/aichat

# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
RUN django-admin.py startproject website /home/docker/code/app/

EXPOSE 80
EXPOSE 8080
EXPOSE 443
CMD ["supervisord", "-n"]
