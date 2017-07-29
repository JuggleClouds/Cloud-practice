FROM python:2.7-alpine

# Variables
ENV home /home/httpd
ENV user httpd

# Training home directory
RUN sh -c 'mkdir -pv $home/{conf,logs,bin,app,run}'  && \
    adduser -D -h $home $user

# Instaling packages
RUN apk update && apk add --no-cache libpq tini uwsgi uwsgi-python openssl-dev openssl libffi-dev libffi sudo bash nginx \
    gcc python-dev postgresql-dev postgresql-libs py-lxml postgresql-client build-base 

# set workdir for copy
WORKDIR $home

# Copy app, configs and necessary scripts
COPY ./src/ $home/app/src/
COPY ./nginx/nginx.conf /etc/nginx/
COPY ./nginx/exampleapp.conf /etc/nginx/conf.d/
COPY ./templates/ ./
COPY ./bin/ /usr/bin/

# set workdir
WORKDIR $home/app/src/

# Instaling pip packages
RUN pip install  -r requirements.txt

## Change rights
RUN chown -R $user:$user $home/

# clean tmp
RUN rm -rf /var/cache/apk/* /var/tmp/* /tmp/*

ENTRYPOINT ["tini", "--"]
