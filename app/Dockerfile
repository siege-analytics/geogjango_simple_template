FROM ubuntu:latest

# Environmental Variables
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV GDAL_VERSION=3.4.1

# set work directory
WORKDIR /usr/src/app

# Args


# Install the basics
RUN apt-get update
RUN apt-get install -y tzdata
RUN apt-get clean && apt-get install -y python3-pip \
    python3-pyproj \
    build-essential \
    wget \
    ca-certificates \
    postgresql \
    postgresql-contrib \
    postgis \
    vim \
    curl \
    zip \
    unzip \
    netcat

# RUN pip install GDAL==3.2.2.1
ADD requirements.txt /tmp/

# trying out GDAL fix
# https://gis.stackexchange.com/questions/28966/python-gdal-package-missing-header-file-when-installing-via-pip

RUN apt-get install -y --install-recommends libgdal-dev
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN pip3 install gdal==3.4.1


# Install PIP requirements
RUN pip3 install -r /tmp/requirements.txt

# copy code over

COPY . .

# run entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

