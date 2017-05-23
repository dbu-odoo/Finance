# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


class FixedDeposite(models.Model):
    _name = 'fixed.deposite'

    name = fields.Char(required=True)
    duration = fields.Integer(string="Duration (Days)", required=True)
    date_from = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    date_to = fields.Date(compute="compute_date_to", string="Maturity Date", readonly=True)
    bank_account = fields.Many2one('bank.account', string="Bank Account", required=True)
    interest_rate = fields.Float(string='Interest Rate', required=True)
    amount = fields.Float(required=True)
    maturity_amount = fields.Float(string="Matured Amount", required=True)
    active = fields.Boolean(default=True)

    @api.depends('duration', 'date_from')
    def compute_date_to(self):
        for rec in self:
            if rec.duration and rec.date_from:
                rec.date_to = datetime.strptime(rec.date_from, "%Y-%m-%d") + relativedelta(days=rec.duration)

