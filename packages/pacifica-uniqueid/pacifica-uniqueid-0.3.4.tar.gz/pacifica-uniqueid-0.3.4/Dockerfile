FROM python:3.6

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi pymysql psycopg2 cryptography
ENV PEEWEE_PROTO mysql
ENV PEEWEE_USER uniqueid
ENV PEEWEE_PASS uniqueid
ENV PEEWEE_PORT 3306
ENV PEEWEE_ADDR 127.0.0.1
ENV PEEWEE_DATABASE pacifica_uniqueid
COPY . .
RUN pip install .
EXPOSE 8051
ENTRYPOINT ["/bin/bash", "/usr/src/app/entrypoint.sh"]
