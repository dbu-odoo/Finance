# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mashape_key = fields.Char(string="Mashape Key")
    module_mutual_fund = fields.Boolean("Mutual Fund")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            mashape_key=get_param('mutual_fund_mashape_key', default='')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('mutual_fund_mashape_key', (self.mashape_key or '').strip())
