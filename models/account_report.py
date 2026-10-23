from odoo import api, models


class AccountReport(models.Model):
    _inherit = "account.report"

    @api.model
    def _build_static_line_columns(self, line, options, all_column_groups_expression_totals, groupby_model=None):
        if self.custom_handler_model_name != "account.aged.receivable.report.handler":
            return super()._build_static_line_columns(
                line, options, all_column_groups_expression_totals, groupby_model=groupby_model,
            )

        expressions = {expression.label: expression for expression in line.expression_ids}
        # Only use the direct path for ordinary aged-receivable expressions.
        # Customized carryovers and editable budgets use Odoo's full builder.
        if any(
            (label.startswith("_") and not label.startswith("_currency_")) or expression.engine != "custom"
            or expression.formula != "_report_custom_engine_aged_receivable"
            for label, expression in expressions.items()
        ) or groupby_model == "account.account":
            return super()._build_static_line_columns(
                line, options, all_column_groups_expression_totals, groupby_model=groupby_model,
            )

        columns = []
        for column in options["columns"]:
            expression = expressions.get(column["expression_label"])
            totals = all_column_groups_expression_totals[column["column_group_key"]]
            result = totals.get(expression, {})
            currency_expression = expressions.get(f"_currency_{column['expression_label']}")
            currency_id = totals.get(currency_expression, {}).get("value") if result.get("value") is not None else None
            # Keep native formatting, audit links, rounding and column metadata.
            columns.append(self._build_column_dict(
                result.get("value"), column, options=options,
                column_expression=expression,
                has_sublines=result.get("sublines_info", False),
                report_line_id=line.id,
                digits=options.get("float_rounding") or 1,
                currency=self.env["res.currency"].browse(currency_id) if currency_id else False,
            ))
        return columns
