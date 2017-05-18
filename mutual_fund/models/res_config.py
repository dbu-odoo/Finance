# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MutualfundConfiguration(models.TransientModel):
    _name = 'mutual.fund.config.settings'
    _inherit = 'res.config.settings'

    mashape_key = fields.Char(string="Mashape Key")

    @api.multi
    def set_mashape_key(self):
        self.env['ir.config_parameter'].set_param('mashape_key', (self.mashape_key or '').strip())

    @api.model
    def get_default_mashape_key(self, fields):
        mashape_key = self.env['ir.config_parameter'].get_param('mashape_key', default='')
        return {'mashape_key': mashape_key}