# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class PiggyBank(models.Model):
    _name = 'piggy.bank'
    _rec_name = 'bank'

    bank = fields.Many2one('bank.account')
    month = fields.Char(string='Month', required=True)
    year = fields.Char(string='Year', required=True)
    deposite_lines = fields.One2many('deposite.lines', 'piggy_bank', string='Deposite Lines')
    amount_total = fields.Monetary(compute='comupte_amount_total', string='Amount Total')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)

    @api.depends('deposite_lines.amount')
    def comupte_amount_total(self):
        for deposite in self:
            if deposite.deposite_lines:
                deposite.amount_total = sum(deposite.deposite_lines.mapped('amount'))


class DepositeLines(models.Model):
    _name = 'deposite.lines'
    _order = 'date'

    date = fields.Date(required=True, default=fields.Date.context_today)
    amount = fields.Float(required=True)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    piggy_bank = fields.Many2one('piggy.bank', string='Piggy Bank')
