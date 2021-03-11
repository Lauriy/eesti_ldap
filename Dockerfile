FROM python:3.9 AS builder

RUN apt-get update && apt-get install libldap2-dev libsasl2-dev -y

WORKDIR /home/docker/eesti_ldap

COPY requirements.txt ./

RUN pip install --upgrade setuptools pip wheel && \
    pip wheel uwsgi --wheel-dir=./wheels/ && \
    pip wheel -r requirements.txt --wheel-dir=./wheels/

FROM python:3.9-slim AS deployer

LABEL maintainer='Lauri Elias <lauri.elias@indoorsman.ee>'

WORKDIR /home/docker/eesti_ldap

COPY --from=builder /home/docker/eesti_ldap/wheels ./wheels

COPY requirements.txt manage.py uwsgi.ini ./

COPY docker-entrypoint.sh docker-entrypoint-dev.sh /usr/bin/

COPY eesti_ldap ./eesti_ldap

COPY templates ./templates

RUN apt-get update && apt-get install ldap-utils uwsgi --no-install-recommends -y && \
    pip install --no-index --find-links=wheels -r requirements.txt && \
    pip install --no-index --find-links=wheels uwsgi && \
    chmod +x /usr/bin/docker-entrypoint.sh && \
    chmod +x /usr/bin/docker-entrypoint-dev.sh && \
    rm -rf requirements.txt wheels && \
    apt-get autoremove -y && apt-get autoclean && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# No single quotes!
ENTRYPOINT ["docker-entrypoint.sh"]
