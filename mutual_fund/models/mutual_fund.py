# -*- coding: utf-8 -*-
import json
import http.client
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
            conn = http.client.HTTPSConnection("mutualfundsnav.p.mashape.com")
            mashape_key = self.env['ir.config_parameter'].sudo().get_param('mutual_fund_mashape_key')
            headers = {
                'x-mashape-key': mashape_key,
                'content-type': "application/x-www-form-urlencoded",
                'accept': "application/json",
            }

            payload = '{"scodes":[%s]}' % mf.amfi_code

            conn.request("POST", "/", payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            if data:
                mf.current_nav = float(json.loads(data)[0].get('nav'))
                mf.date = str(json.loads(data)[0].get('date'))
