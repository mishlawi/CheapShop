FROM mysql:8

MAINTAINER me

COPY db_deployment/db_schema.sql /tmp/

EXPOSE 3300

CMD [ "mysqld", "--init-file=/tmp/db_schema.sql" ]

