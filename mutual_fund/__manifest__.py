# -*- coding: utf-8 -*-
{
    'name': 'Mutual Funds Management',
    'version': '1.0',
    'category': 'Finance',
    'sequence': 1,
    'summary': 'Manage mutual funds ands SIP',
    'description': """
Mutual Fund Management
==========================
Get live nav rate of funds.
    """,
    'author': 'Deep Rajput',
    'depends': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mutual_fund_data.xml',
        'views/mutual_fund_views.xml',
        'views/sip_views.xml',
        'views/lumpsum_views.xml',
        'views/res_config_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
}
