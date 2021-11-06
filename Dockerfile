FROM odoo:latest

ENV HOST=192.168.0.2
ENV USER=odoo
ENV PASSWORD=odoo
COPY ../lightsail/custom_addons /mnt/custom_addons
COPY ../config /etc/odoo
RUN pip3 install paramiko dropbox --upgrade pip
ENTRYPOINT [ "executable" ]