FROM python:3.7-alpine

LABEL maintainer="andre@tenforward.io"

ARG FS_RELOAD_BUILD_ARG


ENV LANGUAGE=en_US:en \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    FS_RELOAD=${FS_RELOAD_BUILD_ARG:-} \
    PIPENV_COLORBLIND=1

WORKDIR /usr/src/app

COPY sla/ sla/

COPY sla/Pipfile* /usr/src/app/

# Add run dependencies
RUN apk add --no-cache \
    curl \
    freetds \
    libffi \
    libxslt \
    libressl \
    libpq \
    libstdc++

# Add build dependencies
RUN apk add --no-cache --virtual .build-deps \
    python3-dev \
    git \
    g++ \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    libressl-dev \
    unixodbc-dev \
    freetds-dev \
    postgresql-dev && \
    python3 -m pip install --upgrade pip pipenv cython && \
    # Install pip dependencies, and do some cleanup
    python3 -m pip install --no-color pipenv cython && \
    pipenv lock --pre -r > requirements.txt && \
    python3 -m pip install --no-cache-dir --no-color -r requirements.txt && \
    python3 -m pip uninstall -y --no-color pipenv cython && \
    rm -rf /root/.local/share/virtualenvs Pipfile* requirements.txt && \
    # Remove build dependencies
    apk del .build-deps

ENV PYTHONPATH=/usr/src/app

CMD ["python3.7","./mqtt_msg_parser.py"]

# HEALTHCHECK --interval=15s CMD echo "True"
