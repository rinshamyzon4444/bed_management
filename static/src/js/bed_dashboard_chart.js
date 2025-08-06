/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted, useState } from "@odoo/owl";

export class BedProductDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.viewService = useService("view");

        this.state = useState({
            mrp_order: 0,
            mrp_draft_count: 0,
            mrp_confirmed_count: 0,
            mrp_in_progress_count: 0,
            mrp_to_close_count: 0,
            mrp_done_count: 0,
            productionVolumeLabels: [],
            productionVolumeData: [],
            rawMaterialLabels: [],
            rawMaterialDatasets: [],
            pieLabels: [],
            pieData: [],
            pieColors: [],
            groupInfo: {
                is_superadmin: false,
                is_production_manager: false,
                is_quality_inspector: false,
            },
        });

        this.latestWorkorders = useState({ records: [] }); // ⬅️ NEW

        onWillStart(async () => {
            const result = await this.orm.call("bed.product.dashboard", "get_tiles_data", [], {});
            Object.assign(this.state, result);

            const volumeResult = await this.orm.call("bed.product.dashboard", "get_production_volume_by_date", [], {});
            this.state.productionVolumeLabels = volumeResult.labels;
            this.state.productionVolumeData = volumeResult.data;

            const rawMaterialResult = await this.orm.call("bed.product.dashboard", "get_raw_material_data", [], {});
            this.state.rawMaterialLabels = rawMaterialResult.labels || [];
            this.state.rawMaterialDatasets = rawMaterialResult.datasets || [];
            this.state.pieLabels = rawMaterialResult.pie?.labels || [];
            this.state.pieData = rawMaterialResult.pie?.data || [];
            this.state.pieColors = rawMaterialResult.pie?.colors || [];

           const workorders = await this.orm.call("bed.product.dashboard", "get_latest_workorders", [], {});
            this.latestWorkorders.records = workorders.workorders;
            this.state.woPassFailLabels = ["Passed", "Failed"];
            this.state.woPassFailData = [
                workorders.quality_summary.passed,
                workorders.quality_summary.failed,
            ];

            const groupInfo = await this.orm.call("bed.product.dashboard", "get_user_group_info", [], {});
            this.state.groupInfo = groupInfo;

        });

        onMounted(() => {
            this.renderBarChart();
            this.renderLineChart();
            this.renderPieChart();
            this.renderProductionVolumeChart();
            this.renderRawMaterialLineChart();
            this.renderRawMaterialPieChart();
            this.renderWorkorderPassFailChart();
        });
    }

    renderBarChart() {
        const el = document.getElementById("bed_bar_chart");
        if (!el) return; // Prevent crash if DOM element doesn't exist

        new Chart(el, {
            type: "bar",
            data: {
                labels: ["Draft", "Confirmed", "In Progress", "To Close", "Done"],
                datasets: [{
                    label: "MRP Orders by State",
                    data: [
                        this.state.mrp_draft_count,
                        this.state.mrp_confirmed_count,
                        this.state.mrp_in_progress_count,
                        this.state.mrp_to_close_count,
                        this.state.mrp_done_count,
                    ],
                    backgroundColor: "#4CAF50",
                }],
            },
        });
    }

    renderLineChart() {
        const el = document.getElementById("bed_line_chart");
        if (!el) return; // Prevent crash if DOM element doesn't exist
        new Chart(el, {
            type: "line",
            data: {
                labels: ["Draft", "Confirmed", "In Progress", "To Close", "Done"],
                datasets: [{
                    label: "MRP Order Trend",
                    data: [
                        this.state.mrp_draft_count,
                        this.state.mrp_confirmed_count,
                        this.state.mrp_in_progress_count,
                        this.state.mrp_to_close_count,
                        this.state.mrp_done_count,
                    ],
                    borderColor: "#2196F3",
                    tension: 0.3,
                    fill: false,
                }],
            },
        });
    }

    renderPieChart() {
        const el = document.getElementById("bed_pie_chart");
        if (!el) return; // Prevent crash if DOM element doesn't exist
        new Chart(el, {
            type: "pie",
            data: {
                labels: ["Draft", "Confirmed", "In Progress", "To Close", "Done"],
                datasets: [{
                    label: "MRP Distribution",
                    data: [
                        this.state.mrp_draft_count,
                        this.state.mrp_confirmed_count,
                        this.state.mrp_in_progress_count,
                        this.state.mrp_to_close_count,
                        this.state.mrp_done_count,
                    ],
                    backgroundColor: [
                        "#9E9E9E",
                        "#03A9F4",
                        "#FFC107",
                        "#FF5722",
                        "#4CAF50",
                    ],
                }],
            },
        });
    }

    renderProductionVolumeChart() {
        const el = document.getElementById("production_volume_chart");
        if (!el) return;
        new Chart(el, {
            type: "bar",
            data: {
                labels: this.state.productionVolumeLabels,
                datasets: [{
                    label: "Production Orders by Date",
                    data: this.state.productionVolumeData,
                    backgroundColor: "#673AB7",
                }],
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        ticks: { autoSkip: true, maxTicksLimit: 12 },
                    },
                    y: { beginAtZero: true },
                },
            },
        });
    }

    renderRawMaterialLineChart() {
        const el = document.getElementById("raw_material_line_chart");
        if (!el) return;
        new Chart(el, {
            type: "bar",
            data: {
                labels: this.state.rawMaterialLabels,
                datasets: this.state.rawMaterialDatasets,
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: "Raw Material Usage by Bed Type",
                    },
                },
            },
        });
    }

    renderRawMaterialPieChart() {
        const el = document.getElementById("raw_material_pie_chart");
        if (!el) return;
        new Chart(el, {
            type: "pie",
            data: {
                labels: this.state.pieLabels,
                datasets: [{
                    data: this.state.pieData,
                    backgroundColor: this.state.pieColors,
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: "Total Raw Material Usage by Bed Type",
                    },
                },
            },
        });
    }

    renderWorkorderPassFailChart() {
    const ctx = document.getElementById("workorder_pass_fail_chart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: this.state.woPassFailLabels,
            datasets: [{
                label: "Workorder Inspection Results",
                data: this.state.woPassFailData,
                backgroundColor: ["#4CAF50", "#F44336"],
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                title: {
                    display: true,
                    text: "Quality Check",
                    font: { size: 16 },
                },
            },
            scales: {
                y: { beginAtZero: true },
            },
        },
    });
    }


    // ---- Navigation Actions ----
    openMrpView() {
        this.action.doAction("mrp.mrp_production_action");
    }

    openMrpDraftView() {
        this.action.doAction({
            name: "Draft MRP Orders",
            type: "ir.actions.act_window",
            res_model: "mrp.production",
            view_mode: "tree,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["state", "=", "draft"]],
        });
    }

    openMrpConfirmedView() {
        this.action.doAction({
            name: "Confirmed MRP Orders",
            type: "ir.actions.act_window",
            res_model: "mrp.production",
            view_mode: "tree,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["state", "=", "confirmed"]],
        });
    }

    openMrpInProgressView() {
        this.action.doAction({
            name: "In Progress MRP Orders",
            type: "ir.actions.act_window",
            res_model: "mrp.production",
            view_mode: "tree,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["state", "=", "progress"]],
        });
    }



    openMrpToCloseView() {
        this.action.doAction({
            name: "MRP Orders To Close",
            type: "ir.actions.act_window",
            res_model: "mrp.production",
            view_mode: "tree,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["state", "=", "to_close"]],
        });
    }

    openMrpDoneView() {
        this.action.doAction({
            name: "Done MRP Orders",
            type: "ir.actions.act_window",
            res_model: "mrp.production",
            view_mode: "tree,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["state", "=", "done"]],
        });
    }
}

BedProductDashboard.template = "bed_management.bed_product_dashboard_template";
registry.category("actions").add("bed_product_dashboard_tag", BedProductDashboard);

///** @odoo-module **/
//
//import { registry } from "@web/core/registry";
//import { useService } from "@web/core/utils/hooks";
//import { Component, onWillStart, onMounted, useState } from "@odoo/owl";
//
//export class BedProductDashboard extends Component {
//  setup() {
//    this.orm = useService("orm");
//    this.action = useService("action");
//    this.viewService = useService("view");
//    this.user = useService("user"); // ✅ Correct way
//
//    // ✅ Safe group check (returns array of strings like 'base.group_user')
//    this.isQualityInspector = this.user.groups?.includes("bed_management.group_bedmanagement_QualityInspector");
//
//    this.state = useState({
//        mrp_order: 0,
//        mrp_draft_count: 0,
//        mrp_confirmed_count: 0,
//        mrp_in_progress_count: 0,
//        mrp_to_close_count: 0,
//        mrp_done_count: 0,
//        productionVolumeLabels: [],
//        productionVolumeData: [],
//        rawMaterialLabels: [],
//        rawMaterialDatasets: [],
//        pieLabels: [],
//        pieData: [],
//        pieColors: [],
//        woPassFailLabels: [],
//        woPassFailData: [],
//    });
//
//    this.latestWorkorders = useState({ records: [] });
//
//    onWillStart(async () => {
//        if (!this.isQualityInspector) {
//            const result = await this.orm.call("bed.product.dashboard", "get_tiles_data", [], {});
//            Object.assign(this.state, result);
//
//            const volumeResult = await this.orm.call("bed.product.dashboard", "get_production_volume_by_date", [], {});
//            this.state.productionVolumeLabels = volumeResult.labels;
//            this.state.productionVolumeData = volumeResult.data;
//
//            const rawMaterialResult = await this.orm.call("bed.product.dashboard", "get_raw_material_data", [], {});
//            this.state.rawMaterialLabels = rawMaterialResult.labels || [];
//            this.state.rawMaterialDatasets = rawMaterialResult.datasets || [];
//            this.state.pieLabels = rawMaterialResult.pie?.labels || [];
//            this.state.pieData = rawMaterialResult.pie?.data || [];
//            this.state.pieColors = rawMaterialResult.pie?.colors || [];
//        }
//
//        const workorders = await this.orm.call("bed.product.dashboard", "get_latest_workorders", [], {});
//        this.latestWorkorders.records = workorders.workorders;
//        this.state.woPassFailLabels = ["Passed", "Failed"];
//        this.state.woPassFailData = [
//            workorders.quality_summary.passed,
//            workorders.quality_summary.failed,
//        ];
//    });
//
//    onMounted(() => {
//        if (!this.isQualityInspector) {
//            this.renderBarChart();
//            this.renderLineChart();
//            this.renderPieChart();
//            this.renderProductionVolumeChart();
//            this.renderRawMaterialLineChart();
//            this.renderRawMaterialPieChart();
//        }
//        this.renderWorkorderPassFailChart();
//    });
//}
//
//    renderBarChart() {
//        new Chart(document.getElementById("bed_bar_chart"), {
//            type: "bar",
//            data: {
//                labels: ["Draft", "Confirmed", "In Progress", "To Close", "Done"],
//                datasets: [{
//                    label: "MRP Orders by State",
//                    data: [
//                        this.state.mrp_draft_count,
//                        this.state.mrp_confirmed_count,
//                        this.state.mrp_in_progress_count,
//                        this.state.mrp_to_close_count,
//                        this.state.mrp_done_count,
//                    ],
//                    backgroundColor: "#4CAF50",
//                }],
//            },
//        });
//    }
//
//    renderLineChart() {
//        new Chart(document.getElementById("bed_line_chart"), {
//            type: "line",
//            data: {
//                labels: ["Draft", "Confirmed", "In Progress", "To Close", "Done"],
//                datasets: [{
//                    label: "MRP Order Trend",
//                    data: [
//                        this.state.mrp_draft_count,
//                        this.state.mrp_confirmed_count,
//                        this.state.mrp_in_progress_count,
//                        this.state.mrp_to_close_count,
//                        this.state.mrp_done_count,
//                    ],
//                    borderColor: "#2196F3",
//                    tension: 0.3,
//                    fill: false,
//                }],
//            },
//        });
//    }
//
//    renderPieChart() {
//        new Chart(document.getElementById("bed_pie_chart"), {
//            type: "pie",
//            data: {
//                labels: ["Draft", "Confirmed", "In Progress", "To Close", "Done"],
//                datasets: [{
//                    label: "MRP Distribution",
//                    data: [
//                        this.state.mrp_draft_count,
//                        this.state.mrp_confirmed_count,
//                        this.state.mrp_in_progress_count,
//                        this.state.mrp_to_close_count,
//                        this.state.mrp_done_count,
//                    ],
//                    backgroundColor: [
//                        "#9E9E9E",
//                        "#03A9F4",
//                        "#FFC107",
//                        "#FF5722",
//                        "#4CAF50",
//                    ],
//                }],
//            },
//        });
//    }
//
//    renderProductionVolumeChart() {
//        new Chart(document.getElementById("production_volume_chart"), {
//            type: "bar",
//            data: {
//                labels: this.state.productionVolumeLabels,
//                datasets: [{
//                    label: "Production Orders by Date",
//                    data: this.state.productionVolumeData,
//                    backgroundColor: "#673AB7",
//                }],
//            },
//            options: {
//                responsive: true,
//                scales: {
//                    x: {
//                        ticks: { autoSkip: true, maxTicksLimit: 12 },
//                    },
//                    y: { beginAtZero: true },
//                },
//            },
//        });
//    }
//
//    renderRawMaterialLineChart() {
//        new Chart(document.getElementById("raw_material_line_chart"), {
//            type: "bar",
//            data: {
//                labels: this.state.rawMaterialLabels,
//                datasets: this.state.rawMaterialDatasets,
//            },
//            options: {
//                responsive: true,
//                plugins: {
//                    title: {
//                        display: true,
//                        text: "Raw Material Usage by Bed Type",
//                    },
//                },
//            },
//        });
//    }
//
//    renderRawMaterialPieChart() {
//        new Chart(document.getElementById("raw_material_pie_chart"), {
//            type: "pie",
//            data: {
//                labels: this.state.pieLabels,
//                datasets: [{
//                    data: this.state.pieData,
//                    backgroundColor: this.state.pieColors,
//                }],
//            },
//            options: {
//                responsive: true,
//                plugins: {
//                    title: {
//                        display: true,
//                        text: "Total Raw Material Usage by Bed Type",
//                    },
//                },
//            },
//        });
//    }
//
//    renderWorkorderPassFailChart() {
//        const ctx = document.getElementById("workorder_pass_fail_chart");
//        if (!ctx) return;
//
//        new Chart(ctx, {
//            type: "bar",
//            data: {
//                labels: this.state.woPassFailLabels,
//                datasets: [{
//                    label: "Workorder Inspection Results",
//                    data: this.state.woPassFailData,
//                    backgroundColor: ["#4CAF50", "#F44336"],
//                }],
//            },
//            options: {
//                responsive: true,
//                plugins: {
//                    legend: { display: true },
//                    title: {
//                        display: true,
//                        text: "Quality Check",
//                        font: { size: 16 },
//                    },
//                },
//                scales: {
//                    y: { beginAtZero: true },
//                },
//            },
//        });
//    }
//
//    // ---- Navigation Actions ----
//    openMrpView() {
//        this.action.doAction("mrp.mrp_production_action");
//    }
//
//    openMrpDraftView() {
//        this.action.doAction({
//            name: "Draft MRP Orders",
//            type: "ir.actions.act_window",
//            res_model: "mrp.production",
//            view_mode: "tree,form",
//            views: [[false, "list"], [false, "form"]],
//            domain: [["state", "=", "draft"]],
//        });
//    }
//
//    openMrpConfirmedView() {
//        this.action.doAction({
//            name: "Confirmed MRP Orders",
//            type: "ir.actions.act_window",
//            res_model: "mrp.production",
//            view_mode: "tree,form",
//            views: [[false, "list"], [false, "form"]],
//            domain: [["state", "=", "confirmed"]],
//        });
//    }
//
//    openMrpInProgressView() {
//        this.action.doAction({
//            name: "In Progress MRP Orders",
//            type: "ir.actions.act_window",
//            res_model: "mrp.production",
//            view_mode: "tree,form",
//            views: [[false, "list"], [false, "form"]],
//            domain: [["state", "=", "progress"]],
//        });
//    }
//
//    openMrpToCloseView() {
//        this.action.doAction({
//            name: "MRP Orders To Close",
//            type: "ir.actions.act_window",
//            res_model: "mrp.production",
//            view_mode: "tree,form",
//            views: [[false, "list"], [false, "form"]],
//            domain: [["state", "=", "to_close"]],
//        });
//    }
//
//    openMrpDoneView() {
//        this.action.doAction({
//            name: "Done MRP Orders",
//            type: "ir.actions.act_window",
//            res_model: "mrp.production",
//            view_mode: "tree,form",
//            views: [[false, "list"], [false, "form"]],
//            domain: [["state", "=", "done"]],
//        });
//    }
//}
//
//BedProductDashboard.template = "bed_management.bed_product_dashboard_template";
//registry.category("actions").add("bed_product_dashboard_tag", BedProductDashboard);
