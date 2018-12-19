#!/usr/bin/env bash

python /home/docker/code/app/manage.py migrate
python /home/docker/code/app/manage.py crontab add
python /home/docker/code/app/manage.py collectstatic --noinput
python /home/docker/code/app/manage.py makemessages -l fr
python /home/docker/code/app/manage.py compilemessages -f
crond
supervisord -n -c /etc/supervisord.conf