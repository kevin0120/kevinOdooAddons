# -*- coding: utf-8 -*-
{
    'name': "bug管理",

    'summary': """
        用于软件开发过程当中bug的管理""",

    'description': """
        用于软件开发过程当中bug的管理
    """,

    'author': "Scott",
    'website': "http://www.scott-odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'CAP/hello',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_setup', 'web_notify', 'app_odoo_customize'],

    # always loaded
    'data': [
        'security/onesphere_cap_rules.xml',
        'security/ir.model.access.csv',
        'template/templates.xml',
        'views/bugs.xml',
        'views/follower.xml',
        'views/bugmanage.xml',
        'template/bugs_template.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
