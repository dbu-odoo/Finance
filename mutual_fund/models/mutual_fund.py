# -*- coding: utf-8 -*-
import requests
from datetime import datetime

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class Mutualfund(models.Model):
    _name = 'mutual.fund'
    _description = 'Mutual Fund'

    name = fields.Char(required=True)
    amfi_code = fields.Char(string="AMFI Code", required=True)
    date = fields.Date(string="Date", readonly=True)
    current_nav = fields.Float(string="Current NAV", readonly=True, digits=(16, 4))

    @api.model
    def fetch_latest_nav(self):
        res = requests.get('https://www.amfiindia.com/spages/NAVAll.txt')
        cnt = 0
        data = {}
        for i in [i.split(';') for i in res.text.strip().split('\n')]:
            cnt += 1
            if len(i) == 6 and cnt > 1:
                data.update({
                    str(i[0].strip()): [float(i[4].strip()) if i[4].strip() != 'N.A.' else 0.00, str(datetime.strptime(i[5].strip(), '%d-%b-%Y').strftime(DF))]
                })

        for mf in self.search([]):
            if data.get(mf.amfi_code):
                mf.current_nav = data.get(mf.amfi_code)[0]
                mf.date = data.get(mf.amfi_code)[1]
