# -*- coding: utf-8 -*-
import unirest
from odoo import api, fields, models


class Mutualfund(models.Model):
    _name = 'mutual.fund'

    name = fields.Char(required=True)
    amfi_code = fields.Char(string="AMFI Code", required=True)
    date = fields.Date(string="Date", readonly=True)
    current_nav = fields.Float(string="Current NAV", readonly=True, digits=(16, 4))

    @api.model
    def fetch_latest_nav(self):
        for mf in self.search([]):
            url = 'https://mutualfundsnav.p.mashape.com/'
            mashape_key = self.env['ir.config_parameter'].sudo().get_param('mutual_fund_mashape_key')
            headers = {
                "X-Mashape-Key": mashape_key,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            params=("{\"scodes\":[%s]}" % mf.amfi_code)

            response = unirest.post(url, headers=headers, params=params)
            if response and response.body:
                mf.current_nav = float((response.body)[0].get('nav'))
                mf.date = str((response.body)[0].get('date'))
