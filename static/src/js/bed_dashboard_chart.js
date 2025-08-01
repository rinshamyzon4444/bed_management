/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted, useState } from "@odoo/owl";

export class BedProductDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

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

            const workorders = await this.orm.call("bed.product.dashboard", "get_latest_workorders", [], {}); // ⬅️ NEW
            this.latestWorkorders.records = workorders; // ⬅️ NEW
        });

        onMounted(() => {
            this.renderBarChart();
            this.renderLineChart();
            this.renderPieChart();
            this.renderProductionVolumeChart();
            this.renderRawMaterialLineChart();
            this.renderRawMaterialPieChart();
        });
    }

    renderBarChart() {
        new Chart(document.getElementById("bed_bar_chart"), {
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
        new Chart(document.getElementById("bed_line_chart"), {
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
        new Chart(document.getElementById("bed_pie_chart"), {
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
        new Chart(document.getElementById("production_volume_chart"), {
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
        new Chart(document.getElementById("raw_material_line_chart"), {
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
        new Chart(document.getElementById("raw_material_pie_chart"), {
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
