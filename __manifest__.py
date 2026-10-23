# -*- coding: utf-8 -*-
{
    "name": "VHG Aged Receivable Customization",
    "summary": "Adds Anzer columns to the original Aged Receivable report.",
    "version": "19.0.1.0.3",
    "category": "Accounting/Accounting",
    "author": "Thein Htoo Aung",
    "license": "LGPL-3",
    "depends": [
        "account_reports",
    ],
    "data": [
        "data/aged_receivable.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "tha_vhg_ar_c11n/static/src/components/account_report/export_context.js",
            "tha_vhg_ar_c11n/static/src/components/account_report/filters/filter_vhg_ar_account.xml",
        ],
        "web.assets_unit_tests": [
            "tha_vhg_ar_c11n/static/src/components/account_report/export_context.js",
            "tha_vhg_ar_c11n/static/tests/export_context.test.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
