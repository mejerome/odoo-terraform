from odoo import models, fields, api


class RestControlSettings(models.TransientModel):
    _inherit = "res.config.settings"

    server_client_id = fields.Char(string="Client Key")
    server_secret_key = fields.Char(string="Client Secret")
    server_gateway = fields.Char(string="Gateway Server URL", default='https://klikodoo.id')
    server_token = fields.Char(string="Gateway Token")

    @api.model
    def get_values(self):
        res = super(RestControlSettings, self).get_values()
        res.update(
            server_secret_key=self.env['ir.config_parameter'].sudo(
            ).get_param('aos_klikapi.server_secret_key'),
            server_client_id=self.env['ir.config_parameter'].sudo(
            ).get_param('aos_klikapi.server_client_id'),
            server_gateway=self.env['ir.config_parameter'].sudo(
            ).get_param('aos_klikapi.server_gateway'),
            server_token=self.env['ir.config_parameter'].sudo(
            ).get_param('aos_klikapi.server_token'),
        )
        return res

    def set_values(self):
        super(RestControlSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        server_secret_key = self.server_secret_key or False
        server_client_id = self.server_client_id or False
        server_gateway = self.server_gateway or False

        param.set_param('aos_klikapi.server_secret_key', server_secret_key)
        param.set_param('aos_klikapi.server_client_id', server_client_id)
        param.set_param('aos_klikapi.server_gateway', server_gateway)
        param.set_param('aos_klikapi.server_token', 'trial')
