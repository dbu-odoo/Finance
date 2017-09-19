# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class BankAccount(models.Model):
    _name = 'bank.account'

    name = fields.Char(string="Bank Name", required=True)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    beneficiary_name = fields.Char(string="Beneficiary Name", required=True)
    account_number = fields.Char(string='Account Number', required=True)
    branch_name = fields.Char(string="Branch Name", required=True)
    branch_code = fields.Char(string="Branch Code", required=True)
    ifsc_code = fields.Char(string="IFSC Code", required=True)
