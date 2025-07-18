{
    "name": "Bed product Management",

    'summary': """Bed product Management""",

    'description': """Bed product Management""",

    'author': "Sidmec",
    'category': 'Uncategorized',
    'version': '17.0.0.0',
    "depends": ['base', 'sale', 'sale_management', 'account', 'product', 'stock', 'mrp','hr'],
    "data": [
        'security/ir.model.access.csv',
        'views/bed.xml',
        'views/bom_inherit.xml',
        'views/manufacturing.xml',
        'views/workcenter.xml',
        'views/workorder.xml',
        'views/reporting.xml',
        'views/report_mrporder.xml',
        'report/product_catalog_report.xml',
        'report/product_catalog_template.xml',
        'report/product_catalog_temp_wholesale.xml',
        'report/workorder_pdf.xml',
        'data/ir_cron.xml',
        'views/dashboard.xml',
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
