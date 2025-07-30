{
    "name": "Bed product Management",

    'summary': """Bed product Management""",

    'description': """Bed product Management""",

    'author': "Sidmec",
    'category': 'Uncategorized',
    'version': '17.0.0.0',
    "depends": ['base', 'sale', 'sale_management', 'account', 'product', 'stock', 'mrp', 'hr', 'board'],
    "data": [
        'security/ir.model.access.csv',
        'views/bed_dashboard.xml',
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

    ],
    'assets': {
        'web.report_assets_pdf': [
            'bed_management/static/src/scss/catalog_style_pdf.scss',
        ],
        'web.assets_backend': [
            'https://cdn.jsdelivr.net/npm/chart.js',
            'bed_management/static/src/js/bed_dashboard_chart.js',
            'bed_management/static/src/xml/bed_dashboard_chart.xml',
        ],

    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    "application": True,
}
