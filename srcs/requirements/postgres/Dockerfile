FROM postgres:15.3-alpine3.18

COPY tools/docker-entrypoint.sh /docker-entrypoint-initdb.d/
COPY tools/create_tables.sh /tmp
