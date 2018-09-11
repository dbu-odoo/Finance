# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class Expense(models.Model):
    _name = 'expense.expense'

    years = [
        ('2017', '2017'),
        ('2018', '2018'),
        ('2019', '2019'),
        ('2020', '2020'),
    ]

    year = fields.Selection(years, string='Year', required=True)
    month = fields.Char(string='Month', required=True)
    expense_lines = fields.One2many('daily.expense', 'expense', string='Daily Expense')
    amount_total = fields.Monetary(compute='comupte_amount_total', string='Amount Total')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)

    @api.depends('expense_lines.amount')
    def comupte_amount_total(self):
        for expense in self:
            if expense.expense_lines:
                expense.amount_total = sum(expense.expense_lines.mapped('amount'))

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.month and record.year:
                name = "%s - %s" % (record.year, record.month)
            result.append((record.id, name))
        return result


class DailyExpense(models.Model):
    _name = 'daily.expense'
    _rec_name = 'expense_category'
    _order = 'date'

    expense_category = fields.Many2one('expense.category', string="Expense Category", required=True)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    date = fields.Date(required=True, default=fields.Date.context_today)
    amount = fields.Float(required=True)
    mode = fields.Selection([('offline', 'Offline'), ('online', 'Online')], string="Mode", required=True, default='offline')
    bank = fields.Many2one('bank.account')
    note = fields.Char()
    expense = fields.Many2one('expense.expense', string='Expense')


class ExpenseCategory(models.Model):
    _name = 'expense.category'

    name = fields.Char(required=True)