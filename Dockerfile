FROM python:3.7-alpine
MAINTAINER Thomas Maschler thomas.maschler@wri.org

ENV NAME django
ENV USER django
ENV GEOS http://download.osgeo.org/geos/geos-3.6.3.tar.bz2
ENV PROJ4 http://download.osgeo.org/proj/proj-5.1.0.tar.gz
ENV GDAL http://download.osgeo.org/gdal/2.3.2/gdal-2.3.2.tar.gz

RUN apk update && apk upgrade && \
   apk add --no-cache --update bash git libressl-dev build-base alpine-sdk \
   libffi-dev gcc python3-dev postgresql-dev musl-dev nginx supervisor linux-headers\
    && mkdir -p /usr/src \
    && curl -SL $GEOS | tar -xjC /usr/src \
    && curl -SL $PROJ4 | tar -xzC /usr/src \
    && curl -SL $GDAL | tar -xzC /usr/src

WORKDIR /usr/src/geos-3.6.3
RUN ./configure --enable-python \
    && make \
    && make install
RUN ldconfig /usr/src/geos-3.6.3
RUN geos-config --cflags

WORKDIR /usr/src/proj-5.1.0
RUN ./configure --enable-python \
    && make \
    && make install \
    && export PROJ_DIR=/usr/local/lib/

WORKDIR /usr/src/gdal-2.3.2
RUN ./configure \
    --with-geos \
    --with-geotiff=internal \
    --with-hide-internal-symbols \
    --with-libtiff=internal \
    --with-libz=internal \
    --with-threads \
    --without-bsb \
    --without-cfitsio \
    --without-cryptopp \
    --without-curl \
    --without-dwgdirect \
    --without-ecw \
    --without-expat \
    --without-fme \
    --without-freexl \
    --without-gif \
    --without-gif \
    --without-gnm \
    --without-grass \
    --without-grib \
    --without-hdf4 \
    --without-hdf5 \
    --without-idb \
    --without-ingres \
    --without-jasper \
    --without-jp2mrsid \
    --without-jpeg \
    --without-kakadu \
    --without-libgrass \
    --without-libkml \
    --without-libtool \
    --without-mrf \
    --without-mrsid \
    --without-mysql \
    --without-netcdf \
    --without-odbc \
    --without-ogdi \
    --without-openjpeg \
    --without-pcidsk \
    --without-pcraster \
    --without-pcre \
    --without-perl \
    --without-php \
    --without-png \
    --without-qhull \
    --without-sde \
    --without-sqlite3 \
    --without-webp \
    --without-xerces \
    --without-xml2 \
    && make \
    && make install
RUN ldconfig /usr/src/gdal-2.3.2
RUN export GDAL_LIBRARY_PATH=/usr/local/lib/libgdal.so

RUN addgroup $USER \
    && adduser -s /bin/bash -D -G $USER $USER \
    && easy_install pip \
    && pip install --upgrade pip \
    && pip install -U pip setuptools \
    && pip install cython gevent numpy \
    # pulling pyproj directly from github because of
    # https://github.com/jswhit/pyproj/issues/136
    && pip install git+https://github.com/jswhit/pyproj.git \
    && pip install uwsgi \
    && mkdir -p /opt/$NAME \
    && cd /opt/$NAME

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/conf.d/default.conf
COPY supervisor-app.conf /etc/supervisor.d/django_project.ini

RUN mkdir -p /run/nginx
# RUN mkdir -p /etc/nginx/sites-enabled/
# RUN ln -s /etc/nginx/sites-available/default.conf /etc/nginx/sites-enabled/


# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.

COPY app/requirements.txt /home/docker/code/app/
RUN pip  install -r /home/docker/code/app/requirements.txt

# add (the rest of) our code
# COPY . /home/docker/code/

COPY uwsgi.ini /home/docker/code
COPY uwsgi_params /home/docker/code
RUN mkdir /var/log/django
RUN apk add gettext

# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
# RUN django-admin.py startproject website /home/docker/code/app/
EXPOSE 80

# CMD ["supervisord", "-n"]
