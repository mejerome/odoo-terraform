FROM docker.io/bitnami/odoo:15
RUN /opt/bitnami/python/bin/pip install --upgrade pip; /opt/bitnami/python/bin/pip install paramiko dropbox
COPY ./custom_addons /opt/bitnami/odoo/custom_addons
COPY ./config/odoo.conf /opt/bitnami/odoo/conf/odoo.conf