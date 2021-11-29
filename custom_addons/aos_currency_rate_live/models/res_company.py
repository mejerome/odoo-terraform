# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from lxml import etree, objectify
from odoo.addons.web.controllers.main import xml2json_from_elementtree
import time

import json
import requests

import logging
from wsgiref.simple_server import server_version
_logger = logging.getLogger(__name__)
  
class ResCompany(models.Model):
    _inherit = "res.company"
    
    currency_id_next_execution_date = fields.Date(string="Next Execution Date")
    currency_id_provider = fields.Selection([
        ('kmk', 'KMK'),
        #('bi','BI'),
        ('bca', 'BCA'),
        ('bni', 'BNI'),
        ('bri', 'BRI'),
        ('cimb', 'CIMB'),
    ], default='bca', string='Link Rate Currency')
                     
                   
#     def get_token(self):
#         get_param = self.env["ir.config_parameter"].sudo().get_param
#         url = get_param('aos_klikapi.server_gateway') + '/api/aos/authorize'
#         secret = get_param('aos_klikapi.server_secret_key')
#         client_id = get_param('aos_klikapi.server_client_id')
#         djson = {
#             "params": {
#                 "secret_key": secret,
#                 "client_id" : client_id
#             }
#         }
#         auth = requests.post(url, json=djson)
#         gw = auth.json()['result']
#         #print ('---auth--',gw,url,djson)
#         if gw['status'] == 'success':
#             param = self.env["ir.config_parameter"].sudo()
#             param.set_param('aos_klikapi.server_token', gw['token'])
#         return True
    
                     
    def update_currency_id_rates(self):
        ''' This method is used to update currencies given on bank '''
        res = True
        for company in self:
            res = company._update_currency_id()
            if not res:
                raise UserError(_('Unable to connect to the online exchange rate platform. The web service may be temporary down. Please try again in a moment.'))
    
    def _update_currency_id(self):
        Currency = self.env['res.currency']
        CurrencyRate = self.env['res.currency.rate']
        get_param = self.env["ir.config_parameter"].sudo().get_param
        get_version = self.env["ir.module.module"].sudo().search([('name','=','base')], limit=1)
        #print ('--s---',get_version.latest_version)
        #KLIKODOO  
        #SECRET TOKEN & CLIENT
        for company in self:
            #gateway_url = 'https://klikodoo.id'
            retry = 1
            gateway_url = get_param('aos_klikapi.server_gateway')
            gateway_client = get_param('aos_klikapi.server_client_id')
            gateway_secret = get_param('aos_klikapi.server_secret_key')
            gateway_token = get_param('aos_klikapi.server_token')
            url = gateway_url + '/api/rate/connection/open'
            if not gateway_url:
                raise UserError(_('Cannot find a Server Gateway, You must define one on General Settings'))
            if not gateway_secret:
                raise UserError(_('No Secret Gateway, You must define one on General Settings'))
            if not gateway_client:
                raise UserError(_('No Key Gateway, You must define one on General Settings'))
            url = gateway_url + '/api/rate/connection/open'
            #print ('--gateway_secret--',gateway_url,gateway_secret,gateway_token)
            while True:
                token = gateway_token
                header = {'Authorization': 'Bearer ' + token}
                djson = {
                    "params":{
                        "get_version": get_version and get_version.latest_version,
                        "key": gateway_client,
                        "secret_key": gateway_secret,
                        "function_call": "getrateid",
                        "currency_id_provider": company.currency_id_provider,
                    }
                }
                #response_gateway = requests.get(gateway_url)
                #print ('--OPEN_CONNECTION=sendToPo-11-',url,header,djson)
                gateway = requests.post(url, headers=header, json=djson)
                #print ('--OPEN_CONNECTION=sendToPo-22-',gateway.json())
                if str(gateway) == '<Response [502]>':
                    raise UserError(_('Unable to connect to the Gateway. The web service may be temporary down. Please try again in a moment.'))
                response = []
                results = gateway.json()#['result']
                #print ('===response===',results)
                if not results.get('error'):
                    if results['result']['success']:
                        response = results['result']['response']
                else:
                    company.get_token()
                if retry == 1:
                    _logger.warning('Not Connected to Gateway')
                    #raise UserError(_('Not Connected to Gateway'))
                    break
                retry += 1
            try:
                #print ('===response====',response)
                #'response': [{'name': 'USD', 'rate_sell': 14080.0, 'rate_buy': 13940.0, 'rate_avg': 14010.0}, {'name': 'SGD', 'rate_sell': 10621.03, 'rate_buy': 10499.0, 'rate_avg': 10560.015}]
                for curr in response:
                    currency = Currency.search([('active','=',True),('name','=',curr['name'])], limit=1)
                    if currency.name == curr['name']:
                        today = fields.Date.today()
                        already_existing_rate = CurrencyRate.search([('currency_id', '=', currency.id), ('name', '=', today), ('company_id', '=', company.id)])
                        if already_existing_rate:
                            already_existing_rate.rate = curr['rate_avg']
                        else:
                            CurrencyRate.create({'currency_id_provider': curr['provider'],'currency_id': currency.id, 'rate': curr['rate_avg'], 'name': fields.Datetime.now(), 'company_id': company.id})
            except:
                _logger.warning('Error Cannot update currency rate.')
        return True
    
    @api.model
    def run_update_currency_id(self):
        ''' This method is called from a cron job. Depending on the selection call _update_currency_bi. '''
        records = self.search([('currency_id_next_execution_date', '<=', fields.Date.today())])
        if records:
            records.update_currency_id_rates()
          
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
 
    currency_id_next_execution_date = fields.Date(related="company_id.currency_id_next_execution_date", readonly=False)
    currency_id_provider = fields.Selection(related="company_id.currency_id_provider", readonly=False)

    def update_currency_id_rates_manually(self):
        self.ensure_one()
        res = self.company_id._update_currency_id()
        #print ('==_update_currency_id==',res)
        if not res:
            raise UserError(_('Unable to connect to the online exchange rate platform. The web service may be temporary down. Please try again in a moment.'))

class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'
    
    currency_id_provider = fields.Selection([
        ('kmk', 'KMK'),
        #('bi','BI'),
        ('bca', 'BCA'),
        ('bni', 'BNI'),
        ('bri', 'BRI'),
        ('cimb', 'CIMB'),
    ], default='bca', string='Link Rate Currency')