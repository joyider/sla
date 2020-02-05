FROM timescale/timescaledb:latest-pg11

LABEL maintainer="andre@tenforward.io"

EXPOSE 5432

RUN apk add --no-cache bash

COPY docker/timescaledb/docker-entrypoint-initdb.d/* ./docker-entrypoint-initdb.d/

COPY docker/timescaledb/healthcheck.sh /usr/local/bin/docker-healthcheck

HEALTHCHECK --interval=15s CMD docker-healthcheck
