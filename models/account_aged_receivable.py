# -*- coding: utf-8 -*-

from odoo import models


class AccountAgedReceivableReportHandler(models.AbstractModel):
    _inherit = "account.aged.receivable.report.handler"

    def _custom_options_initializer(self, report, options, previous_options):
        super()._custom_options_initializer(report, options, previous_options=previous_options)

        previous_options = previous_options or {}
        previous_account_ids = previous_options.get("account_ids") or []
        selected_account_ids = [int(account_id) for account_id in previous_account_ids]
        selected_accounts = selected_account_ids and self.env["account.account"].with_context(active_test=False).search([
            ("id", "in", selected_account_ids),
            ("account_type", "=", "asset_receivable"),
            *self.env["account.account"]._check_company_domain(report.get_report_company_ids(options)),
        ]) or self.env["account.account"]

        options["vhg_ar_account_filter"] = True
        options["account_ids"] = selected_accounts.ids
        options["selected_account_ids"] = selected_accounts.mapped("display_name")

        if selected_accounts:
            options["forced_domain"] = options.get("forced_domain", []) + [("account_id", "in", selected_accounts.ids)]

    def _aged_partner_report_custom_engine_common(self, options, internal_type, current_groupby, next_groupby, offset=0, limit=None):
        result = super()._aged_partner_report_custom_engine_common(
            options,
            internal_type,
            current_groupby,
            next_groupby,
            offset=offset,
            limit=limit,
        )
        if internal_type != "asset_receivable":
            return result

        if current_groupby == "id" and isinstance(result, list):
            aml_ids = [aml_id for aml_id, _values in result]
            moves_by_line = {
                line.id: line.move_id
                for line in self.env["account.move.line"].browse(aml_ids)
            }
            for aml_id, values in result:
                line = self.env["account.move.line"].browse(aml_id)
                move = moves_by_line.get(aml_id)
                values["anzer_id"] = (move.anzer_id or "") if move else ""
                values["vendor_ref"] = (move.vendor_ref or "") if move else ""
                values["invoice_no"] = (move.name or "") if move else ""
                values["ref"] = line.ref or ""
            return result

        if isinstance(result, dict):
            result.setdefault("anzer_id", "")
            result.setdefault("vendor_ref", "")
            result.setdefault("invoice_no", "")
            result.setdefault("ref", "")
        elif isinstance(result, list):
            for _grouping_key, values in result:
                values.setdefault("anzer_id", "")
                values.setdefault("vendor_ref", "")
                values.setdefault("invoice_no", "")
                values.setdefault("ref", "")

        return result
