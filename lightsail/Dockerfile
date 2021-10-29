FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get update && apt-get upgrade -y
RUN adduser -system -home=/opt/odoo -group odoo
RUN apt-get install -y git python3-pip build-essential wget python3-dev python3-venv \
    python3-wheel libfreetype6-dev libxml2-dev libzip-dev libldap2-dev libsasl2-dev \
    python3-setuptools node-less libjpeg-dev zlib1g-dev libpq-dev \
    libxslt1-dev libldap2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
    liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev fontconfig libxrender1

# RUN npm install -g rtlcss -y
RUN apt-get install xfonts-75dpi xfonts-base -y
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb
RUN dpkg -i ./wkhtmltox_0.12.6-1.bionic_amd64.deb
RUN cp /usr/local/bin/wkhtmltoimage  /usr/bin/wkhtmltoimage
RUN cp /usr/local/bin/wkhtmltopdf  /usr/bin/wkhtmltopdf
RUN mkdir /var/log/odoo && chown odoo:odoo /var/log/odoo

RUN git clone --depth 1 --branch 15.0 https://www.github.com/odoo/odoo /odoo/odoo-server
RUN chown -R odoo:odoo /odoo/*
RUN pip3 install setuptools wheel
RUN pip3 install -r /odoo/odoo-server/requirements.txt

COPY ./config/odoo.conf /etc/odoo.conf

COPY ./custom_addons /opt/odoo/custom_addons/
EXPOSE 8069
WORKDIR /odoo/odoo-server
USER odoo
# CMD ["./odoo-bin", "-c", "/etc/odoo.conf"]
