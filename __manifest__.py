{
    'name': 'Ecuadorian Localization Multiple Barcode for products',
    'version': '18.01',
    'summary': 'Customization module for Ecuadorian localization to use multiples Barcodes in products',
    'description': """
    Este módulo permite usar barios codigos de barras y precios por cada UdM.
    """,
    'icon': '/account/static/description/l10n.png',
    'countries': ['ec'],
    'author': 'Elmer Salazar Arias',
    'category': 'Accounting/Localizations/',
    'maintainer': 'Elmer Salazar Arias',
    'website': 'http://www.galapagos.tech',
    'email': 'esalazargps@gmail.com',
    'license': 'LGPL-3',
    'depends': [
        'l10n_ec_base',
        'sale',
        'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_pricelist.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/product_barcode_views.xml',
        'views/sale_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'l10n_ec_barcode_products/static/src/js/sale_product_field.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
