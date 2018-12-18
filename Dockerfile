FROM tmaschler/python-gdal:latest
MAINTAINER Thomas Maschler thomas.maschler@wri.org

ENV NAME django
ENV USER django

RUN apk update && apk upgrade && \
   apk add --no-cache --update nginx supervisor gettext

RUN addgroup $USER \
    && adduser -s /bin/bash -D -G $USER $USER \
    && mkdir -p /opt/$NAME \
    && cd /opt/$NAME \
    && pip install uwsgi

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.

COPY app/requirements.txt /home/docker/code/app/
RUN pip  install -r /home/docker/code/app/requirements.txt

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/conf.d/default.conf
COPY supervisor-app.conf /etc/supervisor.d/django_project.ini


# Copy certificate files
ENV CRT_FILE certificate.crt
ENV KEY_FILE certificate.key

COPY certificate.crt /etc/ssl/certs/$CRT_FILE
COPY certificate.key /etc/ssl/private/$KEY_FILE

# update hostname in nginx-app.conf
#configure SSL certificates
COPY ./app/.env /home/docker/code/app/.env
RUN source /home/docker/code/app/.env \
    && sed -i "s/SERVER_URL/$SERVER_URL/g" /etc/nginx/conf.d/default.conf \
    && sed -i "s/SERVER_IP/$SERVER_IP/g" /etc/nginx/conf.d/default.conf \
    && sed -i "s/URI_PREFIX/$URI_PREFIX/g" /etc/nginx/conf.d/default.conf \
    && sed -i "s/KEY_FILE/$KEY_FILE/g" /etc/nginx/conf.d/default.conf \
    && sed -i "s/CRT_FILE/$CRT_FILE/g" /etc/nginx/conf.d/default.conf


RUN mkdir -p /run/nginx

COPY uwsgi.ini /home/docker/code
COPY uwsgi_params /home/docker/code
COPY docker-compose.sh /home/docker/code
COPY docker-compose-develop.sh /home/docker/code

# update prefix in uwsgi.ini
RUN source /home/docker/code/app/.env \
    && sed -i "s/URI_PREFIX/$URI_PREFIX/g" /home/docker/code/uwsgi.ini

RUN mkdir /var/log/django
RUN mkdir /var/log/uwsgi

# expose port 80
EXPOSE 80
EXPOSE 443

# CMD ["supervisord", "-n"]
