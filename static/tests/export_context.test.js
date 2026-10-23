import { expect, test } from "@odoo/hoot";
import { AccountReportController } from "@account_reports/components/account_report/controller";
import "@tha_vhg_ar_c11n/components/account_report/export_context";

function loadingController() {
    const controller = Object.create(AccountReportController.prototype);
    controller.action = { context: { report_id: 42, allowed_company_ids: [4] } };
    controller.options = { vhg_ar_account_filter: true };
    controller.cachedFilterOptions = { report_id: 42, sections: [], unfolded_lines: [] };
    controller.data = undefined;
    return controller;
}

test("aged receivable has an export context while loading", () => {
    const controller = loadingController();
    expect(controller.context).toEqual(controller.action.context);
    controller.action.context = undefined;
    expect(controller.context).toEqual({});
});

test("XLSX export dispatches while report data is loading", async () => {
    const controller = loadingController();
    let dispatched;
    controller.orm = { call: async (...args) => { dispatched = args; return false; } };
    await controller.reportAction(undefined, "export_file", "export_to_xlsx", true);
    expect(dispatched[0]).toBe("account.report");
    expect(dispatched[1]).toBe("dispatch_report_action");
    expect(dispatched[2]).toEqual([
        42, controller.cachedFilterOptions, "export_file", "export_to_xlsx", true,
    ]);
    expect(dispatched[3]).toEqual({ context: controller.action.context });
});

test("loaded report contexts still use the native getter", () => {
    const controller = loadingController();
    controller.data = { context: { lang: "en_US", allowed_company_ids: [4] } };
    expect(controller.context).toEqual(controller.data.context);
    controller.options = {};
    expect(controller.context).toEqual(controller.data.context);
});
