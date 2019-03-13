# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SIP(models.Model):
    _name = 'sip.sip'
    _description = 'SIP'

    name = fields.Many2one('mutual.fund', required=True)
    trading_account = fields.Char(string='Trading Account', required=True)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    amount = fields.Float(required=True)
    total_investment = fields.Float(compute='compute_amount', string='Total Investment')
    current_value = fields.Float(compute='compute_amount', string='Current Value')
    profit = fields.Float(compute='compute_amount', string='Profit/Loss')
    date_of_installment = fields.Integer(string='Installment Date', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    total_installments = fields.Integer(string='Total Installments', required=True)
    percentage = fields.Char(compute='compute_amount', string='Percentage', readonly=True)
    cagr = fields.Char(compute='compute_cagr', string='CAGR', readonly=True)
    note = fields.Text()
    active = fields.Boolean(default=True)
    sip_line_ids = fields.One2many('sip.lines', 'sip_id', string="SIP Lines")

    def xirr(self, transactions):
        years = [(ta[0] - transactions[0][0]).days / 365. for ta in transactions]
        residual = 1.0
        step = 0.05
        guess = 0.05
        epsilon = 0.0001
        limit = 10000
        while abs(residual) > epsilon and limit > 0:
            limit -= 1
            residual = 0.0
            for i, trans in enumerate(transactions):
                residual += trans[1] / pow(guess, years[i])
            if abs(residual) > epsilon:
                if residual > 0:
                    guess += step
                else:
                    guess -= step
                    step /= 2.0
        return guess - 1

    @api.depends('sip_line_ids')
    def compute_cagr(self):
        for rec in self:
            if rec.sip_line_ids:
                transactions = []
                for line in rec.sip_line_ids:
                    transactions.append((line.date, line.amount * -1.00))
                transactions.append((rec.name.date, rec.current_value))
                cagr = '{:.2%}'.format(self.xirr(transactions))
                rec.cagr = cagr

    @api.depends('sip_line_ids')
    def compute_amount(self):
        for rec in self:
            if rec.sip_line_ids:
                total_amount = sum(rec.sip_line_ids.mapped('amount'))
                if total_amount:
                    current_value = sum(rec.sip_line_ids.mapped('current_value'))
                    rec.total_investment = total_amount
                    rec.current_value = current_value
                    rec.profit = current_value - total_amount
                    rec.percentage = ('%.2f' % (((current_value * 100) / total_amount) - 100)) + '%'

    @api.multi
    def fetch_latest_nav(self):
        self.ensure_one()
        self.env['mutual.fund'].fetch_latest_nav()


class SIPLines(models.Model):
    _name = 'sip.lines'
    _description = 'SIP Lines'

    sip_id = fields.Many2one('sip.sip', string='SIP')
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    line_no = fields.Integer(compute='_get_line_numbers', string='No',readonly=True, default=False)
    mutual_fund = fields.Many2one('mutual.fund', related='sip_id.name', required=True)
    date = fields.Date(string="Date", required=True)
    amount = fields.Float(required=True)
    nav = fields.Float(string="NAV", required=True, digits=(16, 4))
    units = fields.Float(compute='compute_units', readonly=True, digits=(16, 3))
    current_nav_date = fields.Date(compute='compute_current_nav', string="Current NAV Date", readonly=True)
    txn_days = fields.Integer(compute='compute_txn_days', string='Txn Days', readonly=True)
    current_nav = fields.Float(compute='compute_current_nav', string='Current NAV', readonly=True, digits=(16, 4))
    current_value = fields.Float(compute='compute_current_value', string='Current Value', readonly=True, digits=(16, 2))
    profit = fields.Float(compute='compute_profit', string="Profit/Loss", readonly=True, digits=(16, 2))
    percentage = fields.Char(compute='compute_profit', string='Percentage', readonly=True)
    cagr = fields.Char(compute='compute_cagr', string='CAGR', readonly=True)

    def _get_line_numbers(self):
        line_num = 1    
        if self.ids:
            first_line_rec = self.browse(self.ids[0])

            for line_rec in first_line_rec.sip_id.sip_line_ids:
                line_rec.line_no = line_num
                line_num += 1

    @api.depends('mutual_fund')
    def compute_current_nav(self):
        for rec in self:
            if rec.mutual_fund:
                rec.current_nav = rec.mutual_fund.current_nav
                rec.current_nav_date = rec.mutual_fund.date

    @api.depends('date', 'current_nav_date')
    def compute_txn_days(self):
        for rec in self:
            if rec.current_nav_date and rec.date:
                rec.txn_days = (rec.current_nav_date - rec.date).days

    @api.depends('amount', 'nav')
    def compute_units(self):
        for rec in self:
            if rec.amount and rec.nav:
                rec.units = rec.amount / rec.nav

    @api.depends('units', 'current_nav')
    def compute_current_value(self):
        for rec in self:
            if rec.units and rec.current_nav:
                rec.current_value = rec.units * rec.current_nav

    @api.depends('amount', 'current_value')
    def compute_profit(self):
        for rec in self:
            if rec.amount and rec.current_value:
                rec.profit = rec.current_value - rec.amount
                rec.percentage = ('%.2f' % (((rec.current_value * 100) / rec.amount) - 100)) + '%'

    @api.depends('date', 'current_nav_date', 'amount', 'current_value')
    def compute_cagr(self):
        for rec in self:
            if rec.amount > 0.00 and rec.current_value > 0.00 and rec.date and rec.current_nav_date:
                days = (rec.current_nav_date - rec.date).days
                if days > 0:
                    cagr = (rec.current_value/rec.amount)**(1/(days/365))-1
                    rec.cagr = '{:.2%}'.format(cagr)