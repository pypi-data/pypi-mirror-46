#!/bin/bash
mkdir ~/.pacifica-policy/
cp /usr/src/app/server.conf ~/.pacifica-policy/cpconfig.ini
touch ~/.pacifica-policy/config.ini
uwsgi \
  --http-socket 0.0.0.0:8181 \
  --master \
  --die-on-term \
  --module pacifica.policy.wsgi "$@"
