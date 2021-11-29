# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    currency_convert_method = fields.Selection([('verse','Verse'),('inverse','Inverse')], default='inverse', string='Convert Method')
    
class ResCurrency(models.Model):
    _inherit = 'res.currency'
    
    rounding = fields.Float(string='Rounding Factor', digits=(12, 10), default=0.01)
    
#     def _get_rates(self, company, date):
#         query = """SELECT c.id,
#                           COALESCE((SELECT r.rate FROM res_currency_rate r
#                                   WHERE r.currency_id = c.id AND r.name <= %s
#                                     AND (r.company_id IS NULL OR r.company_id = %s)
#                                ORDER BY r.company_id, r.name DESC
#                                   LIMIT 1), 1.0) AS rate
#                    FROM res_currency c
#                    WHERE c.id IN %s"""
#         self._cr.execute(query, (date, company.id, tuple(self.ids)))
#         currency_rates = dict(self._cr.fetchall())
#         return currency_rates
#     @api.model
#     def _get_conversion_rate(self, from_currency, to_currency):
#         if not self._context.get('force_rate'):
#             from_currency = from_currency.with_env(self.env).rate
#         else:
#             from_currency = self._context.get('force_rate')
#         to_currency = to_currency.with_env(self.env)
#         return from_currency / to_currency.rate
#     @api.model
#     def _get_conversion_rate(self, from_currency, to_currency):
#         if not self._context.get('force_rate'):
#             from_currency = from_currency.with_env(self.env).rate
#         else:
#             from_currency = self._context.get('force_rate')
#         to_currency = to_currency.with_env(self.env)
#         return from_currency / to_currency.rate
# 
#     @api.model
#     def _compute(self, from_currency, to_currency, from_amount, round=True):
#         if (to_currency == from_currency):
#             amount = to_currency.round(from_amount) if round else from_amount
#         else:
#             try:
#                 rate = self._context.get('force_rate')
#             except:
#                 rate = False
#             if not rate:
#                 rate = self._get_conversion_rate(from_currency, to_currency)
#             amount = to_currency.round(from_amount * rate) if round else from_amount * rate
#         return amount
    
#     @api.model
#     def _get_conversion_rate(self, from_currency, to_currency, company, date):
#         currency_rates = (from_currency + to_currency)._get_rates(company, date)
#         if self._context.get('force_rate'):
#             res = self._context.get('force_rate')
#         else:
#             res = currency_rates.get(from_currency.id) / currency_rates.get(to_currency.id)
#         return res

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        currency_rates = (from_currency + to_currency)._get_rates(company, date)
        #print ('-_get_conversion_rate--',self._context.get('force_rate'))
        if company.currency_convert_method == 'inverse':
            if self._context.get('force_rate'):            
                res = self._context.get('force_rate') / currency_rates.get(to_currency.id)
            else:
                res = currency_rates.get(from_currency.id) / currency_rates.get(to_currency.id)
        else:            
            if self._context.get('force_rate'):            
                res = currency_rates.get(to_currency.id) / self._context.get('force_rate')
            else:
                res = currency_rates.get(to_currency.id) / currency_rates.get(from_currency.id)
        return res
    
#     @api.model
#     def _get_conversion_rate(self, from_currency, to_currency, company, date):
#         currency_rates = (from_currency + to_currency)._get_rates(company, date)
#         res = currency_rates.get(to_currency.id) / currency_rates.get(from_currency.id)
#         return res
    
#     @api.model
#     def _get_conversion_rate(self, from_currency, to_currency, company, date):
#         currency_rates = (from_currency + to_currency)._get_rates(company, date)
#         res = currency_rates.get(to_currency.id) / currency_rates.get(from_currency.id)
#         return res

#     def _convert(self, from_amount, to_currency, company, date, round=True):
#         """Returns the converted amount of ``from_amount``` from the currency
#            ``self`` to the currency ``to_currency`` for the given ``date`` and
#            company.
# 
#            :param company: The company from which we retrieve the convertion rate
#            :param date: The nearest date from which we retriev the conversion rate.
#            :param round: Round the result or not
#         """
#         self, to_currency = self or to_currency, to_currency or self
#         assert self, "convert amount from unknown currency"
#         assert to_currency, "convert amount to unknown currency"
#         assert company, "convert amount from unknown company"
#         assert date, "convert amount from unknown date"
#         # apply conversion rate
#         if self == to_currency:
#             to_amount = from_amount
#         else:
#             try:
#                 to_amount = self._context.get('force_rate')
#             except:
#                 to_amount = False
#             if not to_amount:
#                 #rate = self._get_conversion_rate(from_currency, to_currency)
#                 to_amount = from_amount * self._get_conversion_rate(self, to_currency, company, date)
#             #amount = to_currency.round(from_amount * rate) if round else from_amount * rate
#         # apply rounding
#         print ('--_convert--',self._context)
#         return to_currency.round(to_amount) if round else to_amount
    
#     @api.model
#     def _compute(self, from_currency, to_currency, from_amount, round=True):
#         _logger.warning('The `_compute` method is deprecated. Use `_convert` instead')
#         print ('--_compute--',self._context)
#         date = self._context.get('date') or fields.Date.today()
#         company = self.env['res.company'].browse(self._context.get('company_id')) or self.env['res.users']._get_company()
#         return from_currency._convert(from_amount, to_currency, company, date)
#  
#     @api.multi
#     def compute(self, from_amount, to_currency, round=True):
#         _logger.warning('The `compute` method is deprecated. Use `_convert` instead')
#         print ('--compute--',self._context)
#         date = self._context.get('date') or fields.Date.today()
#         company = self.env['res.company'].browse(self._context.get('company_id')) or self.env['res.users']._get_company()
#         return self._convert(from_amount, to_currency, company, date)
    
#     @api.model
#     def _compute(self, from_currency, to_currency, from_amount, round=True):
#         if (to_currency == from_currency):
#             amount = to_currency.round(from_amount) if round else from_amount
#         else:
#             try:
#                 rate = self._context.get('force_rate')
#             except:
#                 rate = False
#             if not rate:
#                 rate = self._get_conversion_rate(from_currency, to_currency)
#             amount = to_currency.round(from_amount * rate) if round else from_amount * rate
#         return amount
    

class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    
    kmk_date = fields.Date('Date KMK')
    kmk_number = fields.Char('Number KMK', size=16)
    
# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'
#     
#     @api.model
#     def _compute_amount_fields(self, amount, src_currency, company_currency):
#         """ Helper function to compute value for fields debit/credit/amount_currency based on an amount and the currencies given in parameter"""
#         amount_currency = False
#         currency_id = False
#         date = self.env.context.get('date') or fields.Date.today()
#         company = self.env.context.get('company_id')
#         company = self.env['res.company'].browse(company) if company else self.env.user.company_id
#         if src_currency and src_currency != company_currency:
#             amount_currency = amount
#             amount = src_currency.with_context(force_rate=self.env.context.get('force_rate'))._convert(amount, company_currency, company, date)
#             currency_id = src_currency.id
#         debit = amount > 0 and amount or 0.0
#         credit = amount < 0 and -amount or 0.0
#         return debit, credit, amount_currency, currency_id
    