# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests

class ResCompany(models.Model):
    _inherit = "res.company"
       
    def get_token(self):
        get_param = self.env["ir.config_parameter"].sudo().get_param
        url = get_param('aos_klikapi.server_gateway') + '/api/aos/authorize'
        secret = get_param('aos_klikapi.server_secret_key')
        client_id = get_param('aos_klikapi.server_client_id')
        djson = {
            "params": {
                "secret_key": secret,
                "client_id" : client_id
            }
        }
        auth = requests.post(url, json=djson)
        gw = auth.json()['result']
        #print ('---auth--',gw,url,djson)
        if gw['status'] == 'success':
            param = self.env["ir.config_parameter"].sudo()
            param.set_param('aos_klikapi.server_token', gw['token'])
        return True
    