# -*- coding: utf-8 -*-
{
    'name': 'Finance Management',
    'version': '1.0',
    'category': 'Account',
    'sequence': 1,
    'summary': 'Fixed Deposites, Loan Management, Installment Management',
    'description': """
Finance Management
==========================
    """,
    'author': 'Deep Rajput',
    'depends': [
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/fixed_deposite_views.xml',
        'views/bank_account_views.xml',
        'views/loan_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
}
