FROM python:3.7 AS builder

LABEL maintainer="Lauri Elias <lauri.elias@indoorsman.ee>"

RUN apt-get update && apt-get install libldap2-dev libsasl2-dev

WORKDIR /home/docker/eesti_ldap

COPY requirements.txt ./

RUN pip install --upgrade setuptools pip wheel && \
    pip wheel -r requirements.txt --wheel-dir=./wheels/

ENTRYPOINT ["pytest"]

FROM python:3.7-slim AS deployer

# TODO: Clean up junk
RUN apt-get update && apt-get install ldap-utils -y

WORKDIR /home/docker/eesti_ldap

COPY --from=builder /home/docker/eesti_ldap/wheels ./wheels

COPY requirements.txt manage.py ./

RUN pip install --no-index --find-links=wheels -r requirements.txt

COPY eesti_ldap ./eesti_ldap

COPY templates ./templates

COPY docker-entrypoint-dev.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint-dev.sh && \
    rm -rf requirements.txt wheels

EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
