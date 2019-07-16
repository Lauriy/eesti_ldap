FROM python:3.7 AS builder

RUN apt-get update && apt-get install libldap2-dev libsasl2-dev

WORKDIR /home/docker/eesti_ldap

COPY requirements.txt ./

RUN pip install --upgrade setuptools pip wheel && \
    pip wheel -r requirements.txt --wheel-dir=./wheels/

ENTRYPOINT ["pytest"]

FROM python:3.7-slim AS deployer

LABEL maintainer="Lauri Elias <lauri.elias@indoorsman.ee>"

WORKDIR /home/docker/eesti_ldap

COPY --from=builder /home/docker/eesti_ldap/wheels ./wheels

COPY requirements.txt manage.py ./

COPY eesti_ldap ./eesti_ldap

COPY templates ./templates

COPY docker-entrypoint-dev.sh /usr/local/bin/

RUN apt-get update && apt-get install ldap-utils -y && \
    pip install --no-index --find-links=wheels -r requirements.txt && \
    chmod +x /usr/local/bin/docker-entrypoint-dev.sh && \
    rm -rf requirements.txt wheels && \
    apt-get autoremove -y && apt-get autoclean && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
