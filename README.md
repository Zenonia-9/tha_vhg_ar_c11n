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
- `models/account_report.py`
  Builds ordinary aged-receivable columns directly with Odoo's native column
  builder, avoiding repeated expression dictionaries and carryover checks per
  cell. Keeps foreign-currency metadata and delegates customized expressions,
  carryovers and account grouping to the full native path. Other reports are unchanged.

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

## Performance validation (2026-10-23)

- Version `19.0.1.0.2` upgraded on local `THA`; all three focused tests passed.
  Comparisons cover blank/populated columns, currency/account visibility,
  comparison groups and fallback for customized expressions.
- Isolated column construction for 10,000 synthetic rows: native 12.3332 seconds,
  optimized 2.9960 seconds (about 4.1 times faster). This measures server-side
  column construction, not complete request, SQL, network or browser time.
- A full report with 2,000 temporary receivable items across 100 temporary
  partners returned 2,232 lines. Native and optimized output matched exactly.
  Both fixtures were transaction-only; rollback was verified.
- Initial full-report wall timings varied: native 4.3522/5.7831 seconds,
  optimized 3.5362/6.9937 seconds. These runs do not establish an overall speedup.
- A second, warmed full-report benchmark alternated three runs per builder on
  the same 2,232-line fixture. Median wall time: native 6.2474 seconds, optimized
  3.1853 seconds (49% reduction); median process CPU: 5.9351 versus 2.8532 seconds.
  Every output field matched; both paths used four queries per warmed run.
  These local synthetic timings are not a production latency guarantee.
- The small original THA sample (32 lines) is not representative of live volume.
  Production latency, query plans and browser performance remain unverified.

## License

This module is licensed under `LGPL-3`.
