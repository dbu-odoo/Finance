# -*- coding: utf-8 -*-
{
    'name': 'Daily Expense Management',
    'version': '1.0',
    'category': 'Expense',
    'sequence': 1,
    'summary': 'Daily Expense Management',
    'description': """
Daily Expense Management
==========================
    """,
    'author': 'Deep Rajput',
    'depends': [
        'finance'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/daily_expense_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
}
