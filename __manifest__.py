{
    "name": "Bed product Management",

    'summary': """Bed product Management""",

    'description': """Bed product Management""",

    'author': "Sidmec",
    'category': 'Uncategorized',
    'version': '17.0.0.0',
    "depends": ['base', 'sale', 'account', 'product', 'stock','mrp'],
    "data": [
        'security/ir.model.access.csv',
        'views/bed.xml',
        'views/addons.xml',
        'views/bom_inherit.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    "application": True,
}
