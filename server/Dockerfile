FROM python:3.6
ENV ACCEPT_EULA=Y
RUN apt-get update -y

RUN apt-get install -y libpq-dev python3-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev
RUN apt-get -y install binutils libproj-dev gdal-bin

RUN mkdir /server
WORKDIR /server
ADD ./requirements.txt /server/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
