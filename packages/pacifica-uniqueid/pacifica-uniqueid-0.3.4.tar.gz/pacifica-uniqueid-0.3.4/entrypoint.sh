#!/bin/bash
if [[ -z $PEEWEE_DATABASE_URL ]] ; then
  if [[ $PEEWEE_USER && $PEEWEE_PASS ]]; then
    PEEWEE_USER_PART="${PEEWEE_USER}:${PEEWEE_PASS}@"
  fi
  if [[ $PEEWEE_PORT ]] ; then
    PEEWEE_ADDR_PART="${PEEWEE_ADDR}:${PEEWEE_PORT}"
  else
    PEEWEE_ADDR_PART=$PEEWEE_ADDR
  fi
  PEEWEE_DATABASE_URL="${PEEWEE_PROTO}://${PEEWEE_USER_PART}${PEEWEE_ADDR_PART}/${PEEWEE_DATABASE}"
fi
mkdir ~/.pacifica-uniqueid/
cp /usr/src/app/server.conf ~/.pacifica-uniqueid/cpconfig.ini
printf '[database]\npeewee_url = '${PEEWEE_DATABASE_URL}'\n' > ~/.pacifica-uniqueid/config.ini
pacifica-uniqueid-cmd dbsync
uwsgi \
  --http-socket 0.0.0.0:8051 \
  --master \
  --die-on-term \
  -p 1 \
  --module pacifica.uniqueid.wsgi "$@"
