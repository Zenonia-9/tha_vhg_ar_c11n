// Run with: node --experimental-vm-modules tests/run_frontend_export_tests.mjs
// Executes the actual Odoo controller, patch utility and frontend regression tests.
// Service stubs replace browser/Owl dependencies; this is not a browser integration test.
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import vm from "node:vm";

const root = new URL("../../../", import.meta.url);
const sources = {
    "@account_reports/components/account_report/controller": new URL("addons/account_reports/static/src/components/account_report/controller.js", root),
    "@web/core/utils/patch": new URL("addons/web/static/src/core/utils/patch.js", root),
    "@tha_vhg_ar_c11n/components/account_report/export_context": new URL("../static/src/components/account_report/export_context.js", import.meta.url),
    tests: new URL("../static/tests/export_context.test.js", import.meta.url),
};

async function run(withFix) {
    const tests = [];
    const stubs = {
        "@odoo/hoot": {
            expect: (actual) => ({
                toBe: (expected) => assert.strictEqual(actual, expected),
                toEqual: (expected) => assert.deepStrictEqual(actual, expected),
            }),
            test: (name, callback) => tests.push({ name, callback }),
        },
        "@web/core/browser/browser": { browser: {} },
        "@web/core/user": { user: {} },
        "@web/core/utils/hooks": { useService: () => ({}) },
        "@odoo/owl": { useState: (state) => state },
    };
    if (!withFix) {
        stubs["@tha_vhg_ar_c11n/components/account_report/export_context"] = {};
    }
    const modules = new Map();
    async function load(name) {
        if (!modules.has(name)) {
            const values = stubs[name];
            const module = values
                ? new vm.SyntheticModule(Object.keys(values), function () {
                    for (const [key, value] of Object.entries(values)) this.setExport(key, value);
                })
                : new vm.SourceTextModule(await fs.readFile(sources[name], "utf8"), { identifier: name });
            modules.set(name, module);
        }
        return modules.get(name);
    }
    const suite = await load("tests");
    await suite.link(load);
    await suite.evaluate();
    let failures = 0;
    for (const test of tests) {
        try {
            await test.callback();
            console.log(`${withFix ? "FIXED" : "BASELINE"} PASS: ${test.name}`);
        } catch (error) {
            failures++;
            console.log(`${withFix ? "FIXED" : "BASELINE"} FAIL: ${test.name}: ${error.message}`);
        }
    }
    return failures;
}

assert.equal(await run(false), 2, "The original controller must reproduce both loading/export errors");
assert.equal(await run(true), 0, "The patched controller must pass every regression test");
