# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'IoT for PoS',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'Use IoT Devices in the PoS',
    'description': """
Allows to use in the Point of Sale the devices that are connected to an IoT Box.
Supported devices include payment terminals, receipt printers, scales and customer displays.
""",
    'data': [
        'views/pos_config_views.xml',
        'views/res_config_setting_views.xml',
        'views/pos_payment_method_views.xml',
    ],
    'depends': ['point_of_sale', 'iot'],
    'installable': True,
    'auto_install': True,
    'uninstall_hook': 'uninstall_hook',
    'license': 'OEEL-1',
    'assets': {
        'point_of_sale.assets': [
            'pos_iot/static/src/js/barcode_reader.js',
            'pos_iot/static/src/js/Chrome.js',
            'pos_iot/static/src/js/ClientScreenButton.js',
            'pos_iot/static/src/js/customer_display.js',
            'pos_iot/static/src/js/DebugWidget.js',
            'pos_iot/static/src/js/devices.js',
            'pos_iot/static/src/js/iot_longpolling.js',
            'pos_iot/static/src/js/IoTErrorPopup.js',
            'pos_iot/static/src/js/LastTransactionStatus.js',
            'pos_iot/static/src/js/models.js',
            'pos_iot/static/src/js/payment.js',
            'pos_iot/static/src/js/printers.js',
            'pos_iot/static/src/js/ProductScreen.js',
            'pos_iot/static/src/js/ScaleScreen.js',
            'pos_iot/static/src/css/pos.css',
        ],
        'web.assets_tests': [
            'pos_iot/static/tests/**/*',
        ],
        'web.assets_qweb': [
            'pos_iot/static/src/xml/**/*',
        ],
    }
}
