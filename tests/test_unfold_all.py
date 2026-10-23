from unittest.mock import patch
from datetime import date

from odoo.tests import TransactionCase, tagged
from odoo.addons.account_reports.models.account_report import AccountReport as NativeAccountReport


@tagged("post_install", "-at_install")
class TestAgedReceivableUnfoldAll(TransactionCase):
    def test_column_builder_matches_native(self):
        report = self.env.ref("account_reports.aged_receivable_report")
        line = self.env.ref("account_reports.aged_receivable_line")
        for show_details in (False, True):
            options = report.get_options({"show_currency": show_details, "show_account": show_details})
            # Exercise independent values for multiple comparison column groups.
            group_key = next(iter(options["column_groups"]))
            options["column_groups"]["comparison"] = options["column_groups"][group_key]
            options["columns"] += [dict(column, column_group_key="comparison") for column in options["columns"]]
            for blank in (False, True):
                totals = {}
                for group in options["column_groups"]:
                    totals[group] = {}
                    for expression in line.expression_ids:
                        value = None if blank else {
                            "invoice_date": date(2026, 10, 23), "due_date": date(2026, 10, 24),
                            "anzer_id": "ANZER-1", "vendor_ref": "Vendor reference",
                            "invoice_no": "INV/1", "ref": "Line reference",
                            "currency": "USD", "account_name": "Receivable",
                            "_currency_amount_currency": self.env.company.currency_id.id,
                        }.get(expression.label, 123.45 if group == group_key else -67.89)
                        totals[group][expression] = {"value": value, "sublines_info": not blank}
                expected = NativeAccountReport._build_static_line_columns(report, line, options, totals)
                with patch.object(NativeAccountReport, "_build_static_line_columns", side_effect=AssertionError("Expected direct builder")):
                    self.assertEqual(report._build_static_line_columns(line, options, totals), expected)

    def test_customized_expressions_use_native_builder(self):
        report = self.env.ref("account_reports.aged_receivable_report")
        line = self.env.ref("account_reports.aged_receivable_line")
        line.expression_ids[0].formula = "_report_custom_engine_customized"
        with patch.object(NativeAccountReport, "_build_static_line_columns", return_value=["native"]) as native:
            self.assertEqual(report._build_static_line_columns(line, {}, {}), ["native"])
            native.assert_called_once()

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
