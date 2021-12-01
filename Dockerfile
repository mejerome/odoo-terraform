FROM odoo:15.0
COPY ./custom_addons /opt/custom_addons
COPY ./config/odoo.conf /etc/odoo/odoo.conf
