# -*- coding: utf-8 -*-
{
    'name': "odoo_odoo_test",

    'summary': """
        Custom module for odoo-test""",

    'description': """
        Custom module for odoo-test
    """,

    'author': "Coopdevs",
    'website': "https://coopdevs.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
