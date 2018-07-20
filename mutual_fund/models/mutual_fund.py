# -*- coding: utf-8 -*-
import requests
from datetime import datetime

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class Mutualfund(models.Model):
    _name = 'mutual.fund'

    name = fields.Char(required=True)
    amfi_code = fields.Char(string="AMFI Code", required=True)
    date = fields.Date(string="Date", readonly=True)
    current_nav = fields.Float(string="Current NAV", readonly=True, digits=(16, 4))

    @api.model
    def fetch_latest_nav(self):
        for mf in self.search([]):
            res = requests.get('https://www.amfiindia.com/spages/NAVAll.txt')
            for i in [i.split(';') for i in res.text.strip().split('\n')]:
                if len(i) == 6:
                    if mf.amfi_code == i[0].strip():
                        mf.current_nav = float(i[4].strip())
                        mf.date = datetime.strptime(i[5].strip(), '%d-%b-%Y').strftime(DF)
