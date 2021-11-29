FROM docker.io/bitnami/odoo:15
RUN pip3 install --upgrade pip; pip3 install paramiko dropbox
RUN mkdir -p /opt/bitnami/odoo/custom_addons
COPY ./custom_addons/* /opt/bitnami/odoo/custom_addons/
RUN sed -i 's/^addons_path.*/addons_path = /opt/bitnami/odoo/addons,/opt/bitnami/odoo/custom_addons/' /opt/bitnami/odoo/conf/odoo.conf

