FROM python:3.8-rc-alpine

LABEL maintainer="Lauri Elias <lauri.elias@indoorsman.ee>"

RUN apk add build-base openldap-dev

WORKDIR /home/docker/eesti_ldap

COPY manage.py requirements.txt ./

RUN pip install --upgrade setuptools pip && \
    pip install -r requirements.txt

COPY eesti_ldap ./eesti_ldap

COPY templates ./templates

COPY docker-entrypoint-dev.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint-dev.sh

EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
