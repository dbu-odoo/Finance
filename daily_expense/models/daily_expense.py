# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Expense(models.Model):
    _name = 'expense.expense'
    _rec_name = 'month'

    month = fields.Char(required=True)
    expense_lines = fields.One2many('daily.expense', 'expense', string='Daily Expense')
    amount_total = fields.Float(compute='comupte_amount_total', string='Amount Total')

    @api.depends('expense_lines.amount')
    def comupte_amount_total(self):
        for expense in self:
            if expense.expense_lines:
                expense.amount_total = sum(expense.expense_lines.mapped('amount'))


class DailyExpense(models.Model):
    _name = 'daily.expense'

    name = fields.Char(required=True)
    expense_category = fields.Many2one('expense.category', string="Expense Category", required=True)
    date = fields.Date(required=True)
    amount = fields.Float(required=True)
    mode = fields.Selection([('offline', 'Offline'), ('online', 'Online')], string="Mode", required=True, default='offline')
    bank = fields.Many2one('bank.account')
    expense = fields.Many2one('expense.expense', string='Expense')


class ExpenseCategory(models.Model):
    _name = 'expense.category'

    name = fields.Char(required=True)