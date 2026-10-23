import { AccountReportController } from "@account_reports/components/account_report/controller";
import { patch } from "@web/core/utils/patch";

patch(AccountReportController.prototype, {
    get context() {
        // Odoo clears data during slow loads, although export buttons remain active.
        // Use the same context as the report-loading RPC until its result is ready.
        if (!this.data && this.options?.vhg_ar_account_filter) {
            return this.action.context || {};
        }
        return super.context;
    },
});
