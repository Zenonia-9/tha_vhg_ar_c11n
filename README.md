# THA VHG Aged Receivable Customization

![Odoo 19](https://img.shields.io/badge/Odoo-19.0-875A7B?style=flat-square)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=flat-square)
![Category](https://img.shields.io/badge/Category-Accounting-4ECDC4?style=flat-square)

Extend the native Aged Receivable report with Anzer document reference columns for Odoo 19.

This addon customizes the original `account_reports` Aged Receivable report in place. It adds **Anzer ID** and **Anzer Reference** columns to unfolded journal-item rows while preserving the standard report action, menu, aging periods, filters, PDF export, and XLSX export.

## Highlights

- Adds **Anzer ID** and **Anzer Reference** columns to the native Aged Receivable report.
- Reuses the original `account.aged.receivable.report.handler`.
- Reads values from `account.move.anzer_id` and `account.move.vendor_ref`.
- Leaves partner summary and total lines blank for move-level Anzer fields.
- Avoids cloning the full report definition.

## Technical Notes

- `data/aged_receivable.xml`
  Declares the new `account.report.column` and `account.report.expression` records on the existing Aged Receivable report.
- `models/account_aged_receivable.py`
  Extends the native receivable aging engine result for move-line group rows.

## Module Layout

```text
tha_vhg_ar_c11n/
|-- data/
|-- models/
`-- __manifest__.py
```

## Dependencies

- `account_reports`
- `anzer_odoo_integration`

## Installation

1. Place the module in your custom addons path.
2. Update the Apps list in Odoo.
3. Install **THA VHG Aged Receivable Customization**.

## License

This module is licensed under `LGPL-3`.
