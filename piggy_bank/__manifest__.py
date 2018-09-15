# -*- coding: utf-8 -*-
{
    'name': 'Piggy Bank',
    'version': '1.0',
    'category': 'Money',
    'sequence': 1,
    'summary': 'Piggy Bank',
    'description': """
Piggy Bank
==========================
    """,
    'author': 'Deep Rajput',
    'depends': [
        'finance'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/piggy_bank_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
}
