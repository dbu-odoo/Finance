# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


class Loan(models.Model):
    _name = 'loan.loan'
    _description = 'Loan'

    name = fields.Char(string="Loan Name", required=True)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user, copy=False)
    product = fields.Many2one('product.product', string="Product", required="True")
    start_date = fields.Date(string="Start Date", required=True)
    duration = fields.Integer(string="Duration(Month)", required=True)
    remaining_duration = fields.Integer(compute="compute_remaining_duration", string="Remaining Duration", copy=False)
    amount = fields.Float(string="Loan Amount", required=True)
    interest_rate = fields.Float(string="Interest Rate")
    emi = fields.Float(compute="compute_emi", string="EMI")
    maturity_date = fields.Date(compute="compute_maturity_date", string="Maturity Date", readonly=True, copy=False)
    loan_installments_ids = fields.One2many('loan.installments', 'loan_id', string="Loan Installments", copy=False)
    installment_button_click = fields.Boolean(copy=False)
    active = fields.Boolean(default=True)

    total_amount = fields.Float(compute="compute_amount", string="Loan Amount", readonly=True)
    total_paid_amount = fields.Float(compute="compute_amount", string="Paid Amount", readonly=True)
    remaining_amount = fields.Float(compute="compute_amount", string="Remaining Amount", readonly=True)
    note = fields.Text(copy=False)

    @api.depends('duration', 'loan_installments_ids.paid')
    def compute_remaining_duration(self):
        for rec in self:
            if rec.duration:
                rec.remaining_duration = rec.duration - int(len(rec.loan_installments_ids.filtered(lambda b: b.paid == True)))

    @api.depends('start_date', 'duration')
    def compute_maturity_date(self):
        for rec in self:
            if rec.start_date and rec.duration:
                rec.maturity_date = datetime.strptime(rec.start_date,'%Y-%m-%d') + relativedelta(months=rec.duration - 1)

    @api.depends('interest_rate', 'amount', 'duration')
    def compute_emi(self):
        for loan in self:
            if loan.interest_rate > 0.00 and loan.amount and loan.duration:
                P = loan.amount
                r = loan.interest_rate/12/100
                n = loan.duration
                loan.emi = P * r * (((1 + r) ** n) / (((1 + r) ** n) - 1))
            if loan.interest_rate == 0.00 and loan.amount and loan.duration:
                loan.emi = loan.amount / loan.duration

    @api.depends('amount', 'loan_installments_ids')
    def compute_amount(self):
        for loan in self:
            if loan.amount and loan.loan_installments_ids:
                total = 0.00
                for line in loan.loan_installments_ids:
                    if line.paid:
                        total += line.installment_amount
                loan.total_amount = loan.amount
                loan.total_paid_amount = total
                loan.remaining_amount = loan.amount - total

    @api.multi
    def calculate_installments(self):
        loan_installments = self.env['loan.installments']
        loan_installments.search([('loan_id', '=', self.id)]).unlink()
        for loan in self:
            date = datetime.strptime(loan.start_date, '%Y-%m-%d')
            counter = 1
            for i in range(1, loan.duration + 1):
                loan_installments.create({
                    'installment_date': date, 
                    'installment_amount': loan.emi,
                    'loan_id': loan.id
                })
                counter += 1
                date = date + relativedelta(months = 1)
            loan.installment_button_click = True
        return True

    @api.multi
    def remove_installments(self):
        for loan in self:
            loan_installments = self.env['loan.installments']
            loan_installments.search([('loan_id', '=', loan.id)]).unlink()
            loan.installment_button_click = False
        return True


class LoanInstallments(models.Model):
    _name = 'loan.installments'
    _description = 'Loan Installments'

    installment_date = fields.Date(string="Installment Date", required=True)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    installment_amount = fields.Float(string="Installment Amount", required=True)
    paid = fields.Boolean(string="Paid")
    loan_id =fields.Many2one('loan.loan', string="Loan", ondelete='cascade')
    line_no = fields.Integer(compute='_get_line_numbers', string='No', readonly=True, default=False)

    def _get_line_numbers(self):
        line_num = 1    
        if self.ids:
            first_line_rec = self.browse(self.ids[0])

            for line_rec in first_line_rec.loan_id.loan_installments_ids:
                line_rec.line_no = line_num
                line_num += 1