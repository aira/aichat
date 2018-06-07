FROM nginx:1.13.12 as base

MAINTAINER Hobson Lane

# Set env variables used in this Dockerfile (use a unique prefix, such as "AICHAT")
# Relative path to local directory with project source code files
ENV PROJECT_NAME="aichat"
ENV AICHAT_SRC="."
ENV AICHAT_DEPLOY="$AICHAT_SRC/deploy"
# ENV CENV_NAME=$PROJECT_NAME"_cenv"
ENV VENV_NAME=$PROJECT_NAME"_venv"
# Directory in container for all project source code files
ENV AICHAT_SRVHOME=/srv

ENV AICHAT_SRVPROJ="$AICHAT_SRVHOME/$PROJECT_NAME"
ENV AICHAT_SRVVENV="$AICHAT_SRVHOME/$VENV_NAME"
ENV AICHAT_SRVDEPLOY="$AICHAT_SRVPROJ/deploy"
ENV AICHAT_SRVMANAGEPY="$AICHAT_SRVPROJ/website"
ENV AICHAT_SRVSTATIC="$AICHAT_SRVHOME/static"
ENV AICHAT_SRVSOCK="$AICHAT_SRVPROJ/gunicorn-nginx.sock"
ENV ANACONDA_BIN="/root/anaconda3/bin"

ENV AICHAT_SRVREQ="$AICHAT_SRVPROJ/requirements-base.txt"

RUN apt-get update && apt-get install -y python3 python3-pip python-pyaudio python3-pyaudio python-dev nano tmux git nginx

# Create application subdirectories
WORKDIR $AICHAT_SRVHOME
RUN mkdir -p media static logs
#read
VOLUME ["$AICHAT_SRVHOME/media/", "$AICHAT_SRVHOME/logs/"]

# Copy application source code to SRCDIR
COPY $AICHAT_SRC $AICHAT_SRVPROJ
# RUN envsubst < $AICHAT_SRVDEPLOY/nginx.conf.envsubst > /etc/nginx/nginx.conf
# RUN envsubst < $AICHAT_SRVDEPLOY/flask.conf.envsubst > /etc/nginx/conf.d/flask.conf
# RUN envsubst < $AICHAT_SRVDEPLOY/supervisord.conf.envsubst >> /etc/supervisord.conf

# RUN python3 -m venv "${AICHAT_SRVVENV}"
# ENV PATH="${AICHAT_SRVVENV}:$PATH"
RUN pip3 install -r "$AICHAT_SRVREQ"

FROM base

WORKDIR $AICHAT_SRVMANAGEPY

# CMD python3 manage.py runserver 0.0.0.0:8000
CMD gunicorn -b 0.0.0.0:80 website.wsgi --workers=3
# CMD ["/usr/bin/supervisord","-nc","/etc/supervisord.conf"]
