FROM odoo:15.0
RUN pip3 install --upgrade pip; pip3 install paramiko dropbox


# RUN /opt/bitnami/python/bin/pip install --upgrade pip; /opt/bitnami/python/bin/pip install paramiko dropbox
# COPY ./custom_addons /opt/bitnami/odoo/custom_addons
# RUN mv /opt/bitnami/odoo/conf /opt/bitnami/odoo/conf.bak
# ADD ./config /opt/bitnami/odoo/conf
