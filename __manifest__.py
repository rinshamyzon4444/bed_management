{
    "name": "Bed product Management",

    'summary': """Bed product Management""",

    'description': """Bed product Management""",

    'author': "Sidmec",
    'category': 'Uncategorized',
    'version': '17.0.0.0',
    "depends": ['base', 'sale', 'sale_management', 'account', 'product', 'stock', 'mrp'],
    "data": [
        'security/ir.model.access.csv',
        'views/bed.xml',
        'views/bom_inherit.xml',
        'views/manufacturing.xml',
        'report/product_catalog_report.xml',
        'report/product_catalog_template.xml',
        'report/product_catalog_temp_wholesale.xml',
        'data/ir_cron.xml',
    ],
    'assets': {
        'web.report_assets_pdf': [
            'bed_management/static/src/scss/catalog_style_pdf.scss',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    "application": True,
}
