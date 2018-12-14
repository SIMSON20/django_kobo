#!/bin/bash

source ./app/.env
export PG_USER=$DB_USER
export PG_DB=$DB_NAME
export PG_PW=$DB_PASSWORD

case "$1" in
    init)
        type docker-compose >/dev/null 2>&1 || { echo >&2 "docker-compose is required but it's not installed.  Aborting."; exit 1; }
        docker-compose -f docker-compose.yml build && docker-compose -f docker-compose.yml up \
        && docker-compose exec web /bin/bash -c "python /home/docker/code/app/manage.py migrate && python /home/docker/code/app/manage.py collectstatic --noinput && python /home/docker/code/app/manage.py createsuperuser"
        ;;

    develop)
        type docker-compose >/dev/null 2>&1 || { echo >&2 "docker-compose is required but it's not installed.  Aborting."; exit 1; }
        docker-compose -f docker-compose-develop.yml build && docker-compose -f docker-compose-develop.yml up
        ;;

    start)
        type docker-compose >/dev/null 2>&1 || { echo >&2 "docker-compose is required but it's not installed.  Aborting."; exit 1; }
        docker-compose -f docker-compose.yml build && docker-compose -f docker-compose.yml up
        ;;

    *)
     echo "Usage: django_kobo.sh {init|develop|start}" >&2
        exit 1
        ;;
esac

exit 0