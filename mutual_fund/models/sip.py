# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SIP(models.Model):
    _name = 'sip.sip'
    _description = 'SIP'

    name = fields.Many2one('mutual.fund', required=True)
    trading_account = fields.Char(string='Trading Account', required=True)
    user_id = fields.Many2one(
        'res.users', string="User", default=lambda self: self.env.user)
    amount = fields.Float(required=True)
    total_investment = fields.Float(
        compute='compute_amount', string='Total Investment')
    current_value = fields.Float(
        compute='compute_amount', string='Current Value')
    profit = fields.Float(compute='compute_amount', string='Profit/Loss')
    date_of_installment = fields.Integer(
        string='Installment Date', required=True)
    percentage = fields.Char(compute='compute_amount',
                             string='Percentage', readonly=True)
    note = fields.Text()
    active = fields.Boolean(default=True)
    sip_line_ids = fields.One2many('sip.lines', 'sip_id', string="SIP Lines")
    total_installments = fields.Integer(compute='compute_total_installments', string='Total Installments')

    @api.depends('sip_line_ids')
    def compute_amount(self):
        for rec in self:
            rec.total_investment = 0.00
            rec.current_value = 0.00
            rec.profit = 0.00
            rec.percentage = 0.00
            if rec.sip_line_ids:
                total_amount = sum(rec.sip_line_ids.mapped('amount'))
                if total_amount:
                    current_value = sum(rec.sip_line_ids.mapped('current_value'))
                    rec.total_investment = total_amount
                    rec.current_value = current_value
                    rec.profit = current_value - total_amount
                    rec.percentage = (
                        '%.2f' % (((current_value * 100) / total_amount) - 100)) + '%'

    def fetch_latest_nav(self):
        self.ensure_one()
        self.env['mutual.fund'].fetch_latest_nav()

    @api.depends('sip_line_ids')
    def compute_total_installments(self):
        for rec in self:
            rec.total_installments = len(rec.sip_line_ids)


class SIPLines(models.Model):
    _name = 'sip.lines'
    _description = 'SIP Lines'
    _order = 'date desc'

    sip_id = fields.Many2one('sip.sip', string='SIP')
    user_id = fields.Many2one(
        'res.users', string="User", default=lambda self: self.env.user)
    # line_no = fields.Integer(compute='_get_line_numbers',
    #                          string='No', readonly=True, default=False)
    mutual_fund = fields.Many2one(
        'mutual.fund', related='sip_id.name', required=True)
    date = fields.Date(string="Date", required=True)
    amount = fields.Float(required=True)
    nav = fields.Float(string="NAV", required=True, digits=(16, 4))
    units = fields.Float(compute='compute_units',
                         readonly=True, digits=(16, 3))
    current_nav_date = fields.Date(
        compute='compute_current_nav', string="Current NAV Date", readonly=True)
    current_nav = fields.Float(
        compute='compute_current_nav', string='Current NAV', readonly=True, digits=(16, 4))
    current_value = fields.Float(
        compute='compute_current_value', string='Current Value', readonly=True, digits=(16, 2))
    profit = fields.Float(compute='compute_profit',
                          string="Profit/Loss", readonly=True, digits=(16, 2))
    percentage = fields.Char(compute='compute_profit',
                             string='Percentage', readonly=True)

    @api.depends('mutual_fund')
    def compute_current_nav(self):
        for rec in self:
            if rec.mutual_fund:
                rec.current_nav = rec.mutual_fund.current_nav
                rec.current_nav_date = rec.mutual_fund.date
            else:
                rec.current_nav = 0.00
                rec.current_nav_date = False

    @api.depends('amount', 'nav')
    def compute_units(self):
        for rec in self:
            if rec.amount and rec.nav:
                rec.units = rec.amount / rec.nav
            else:
                rec.units = 0.00

    @api.depends('units', 'current_nav')
    def compute_current_value(self):
        for rec in self:
            if rec.units and rec.current_nav:
                rec.current_value = rec.units * rec.current_nav
            else:
                rec.current_value = 0.00

    @api.depends('amount', 'current_value')
    def compute_profit(self):
        for rec in self:
            if rec.amount and rec.current_value:
                rec.profit = rec.current_value - rec.amount
                rec.percentage = (
                    '%.2f' % (((rec.current_value * 100) / rec.amount) - 100)) + '%'
            else:
                rec.profit = 0.00
                rec.percentage = 0.00
