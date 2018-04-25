# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Lumpsum(models.Model):
    _name = 'lumpsum.lumpsum'
    _rec_name = 'mutual_fund'
    _order = 'date desc'

    mutual_fund = fields.Many2one('mutual.fund', required=True)
    trading_account = fields.Char(string='Trading Account', required=True)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    date = fields.Date(string="Date", required=True)
    amount = fields.Float(required=True, digits=(16, 2))
    nav = fields.Float(string="NAV", required=True, digits=(16, 4))
    units = fields.Float(compute='compute_units', readonly=True, digits=(16, 3))
    current_nav_date = fields.Date(compute='compute_current_nav', string="Current NAV Date", readonly=True)
    current_nav = fields.Float(compute='compute_current_nav', string='Current NAV', readonly=True, digits=(16, 4))
    current_value = fields.Float(compute='compute_current_value', string='Current Value', readonly=True, digits=(16, 2))
    profit = fields.Float(compute='compute_profit', readonly=True, string='Profit/Loss', digits=(16, 2))
    percentage = fields.Char(compute='compute_profit', string='Percentage', readonly=True)
    active = fields.Boolean(default=True)

    @api.multi
    def fetch_latest_nav(self):
        self.ensure_one()
        self.env['mutual.fund'].fetch_latest_nav()

    @api.depends('mutual_fund')
    def compute_current_nav(self):
        for rec in self:
            if rec.mutual_fund:
                rec.current_nav = rec.mutual_fund.current_nav
                rec.current_nav_date = rec.mutual_fund.date

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
