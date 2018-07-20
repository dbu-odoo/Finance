# -*- coding: utf-8 -*-
{
    'name': 'Mutual Funds Management',
    'version': '1.0',
    'category': 'Finance',
    'sequence': 1,
    'license': 'LGPL-3',
    'summary': 'Manage mutual funds ands SIP',
    'description': """
Mutual Fund Management
==========================
Get live nav rate of funds.
    """,
    'author': 'Deep Technologies',
    'depends': ['base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'data/mutual_fund_data.xml',
        'views/mutual_fund_views.xml',
        'views/sip_views.xml',
        'views/lumpsum_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'price': 30.00,
    'currency': 'EUR',
    'application': True,
}
