from unittest.mock import patch

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAgedReceivableUnfoldAll(TransactionCase):
    def test_batch_custom_columns_and_totals(self):
        report = self.env.ref("account_reports.aged_receivable_report")
        report_line = self.env.ref("account_reports.aged_receivable_line")
        handler = self.env[report.custom_handler_model_name]
        custom_values = dict(anzer_id="ANZER-1", vendor_ref="Vendor reference",
                             invoice_no="INV/1", ref="Line reference")
        aml_values = handler._prepare_partner_values()
        aml_values.update(custom_values, partner_id=42, total=125.0)
        aml_values.update({f"period{i}": 125.0 if i == 0 else 0.0 for i in range(6)})
        options = {"report_id": report.id}
        lines_to_expand = {"_report_expand_unfoldable_line_with_groupby": [
            {"id": report._get_generic_line_id("account.report.line", report_line.id)},
        ]}
        with patch.object(type(report), "_split_options_per_column_group", return_value={"test": options}), \
             patch.object(type(handler), "_aged_partner_report_custom_engine_common", return_value=[(99, aml_values)]):
            batch = handler._common_custom_unfold_all_batch_data_generator(
                "asset_receivable", report, options, lines_to_expand,
            )

        partners = batch[f"[{report_line.id}]=>partner_id"]["test"]
        invoices = batch[f"[{report_line.id}]partner_id:42=>id"]["test"]
        expressions = {expression.subformula: expression for expression in partners}
        for label, value in custom_values.items():
            self.assertEqual(partners[expressions[label]]["value"], [(42, "")])
            self.assertEqual(invoices[expressions[label]]["value"], [(99, value)])
        self.assertEqual(partners[expressions["total"]]["value"], [(42, 125.0)])
        self.assertEqual(partners[expressions["period0"]]["value"], [(42, 125.0)])
