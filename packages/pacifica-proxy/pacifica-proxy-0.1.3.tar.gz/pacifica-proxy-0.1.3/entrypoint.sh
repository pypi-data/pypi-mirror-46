#!/bin/bash
mkdir ~/.pacifica-proxy
touch ~/.pacifica-proxy/config.ini
cp /usr/src/app/server.conf ~/.pacifica-proxy/cpconfig.ini
uwsgi \
  --http-socket 0.0.0.0:8180 \
  --master \
  --die-on-term \
  --module pacifica.proxy.wsgi "$@"
