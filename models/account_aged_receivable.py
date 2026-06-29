# -*- coding: utf-8 -*-

from odoo import models


class AccountAgedReceivableReportHandler(models.AbstractModel):
    _inherit = "account.aged.receivable.report.handler"

    @staticmethod
    def _set_line_total(values):
        period_keys = [key for key in values if key.startswith("period")]
        values["total"] = sum(values[key] for key in period_keys)

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
                self._set_line_total(values)
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
