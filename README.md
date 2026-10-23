# VHG Aged Receivable Customization

![Odoo 19](https://img.shields.io/badge/Odoo-19.0-875A7B?style=flat-square)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=flat-square)
![Category](https://img.shields.io/badge/Category-Accounting-4ECDC4?style=flat-square)

Extend the native Aged Receivable report with Anzer, invoice, and reference columns for Odoo 19.

This addon customizes the original `account_reports` Aged Receivable report in place. It adds **Anzer ID**, **Anzer Reference**, and **Invoice No.** columns to unfolded journal-item rows while preserving the standard report action, menu, aging periods, filters, PDF export, and XLSX export.

## Highlights

- Adds **Anzer ID**, **Anzer Reference**, **Invoice No.**, and **Reference** columns to the native Aged Receivable report.
- Reuses the original `account.aged.receivable.report.handler`.
- Reads values from `account.move.anzer_id`, `account.move.vendor_ref`, and `account.move.name`.
- Leaves partner summary and total lines blank for move-level Anzer fields.
- Supplies blank custom fields to the native Unfold All batch summaries, preventing
  missing-key errors while retaining invoice-level details and aging totals.
- Avoids cloning the full report definition.

## Technical Notes

- `data/aged_receivable.xml`
  Declares the new `account.report.column` and `account.report.expression` records on the existing Aged Receivable report.
- `models/account_aged_receivable.py`
  Extends the native receivable aging engine result for move-line group rows, including the invoice number.

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
3. Install **VHG Aged Receivable Customization**.

## Unfold All regression validation (2026-10-23)

- Version `19.0.1.0.1` upgraded on local `THA`; focused Odoo test passed.
- With the original native partner defaults restored temporarily in a read-only
  shell check, the report reproduced `KeyError('anzer_id')`.
- With the fix active, THUKHA's report as of 2026-10-23 returned 32 lines,
  including 22 journal items; all 10 collapsed summary/total rows matched.
- Python/XML syntax and manifest checks passed; local Odoo restarted successfully.
- Deployment and successful browser verification on `10.100.10.61` remain pending.

## License

This module is licensed under `LGPL-3`.
