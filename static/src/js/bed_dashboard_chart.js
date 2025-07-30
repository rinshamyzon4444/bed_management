/** @odoo-module **/

import { Component, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class BedDashboardChart extends Component {
    setup() {
        this.orm = useService("orm");
        onMounted(this.loadCharts.bind(this));
    }

    async loadCharts() {
        const result = await this.orm.call("bed.dashboard", "get_mo_chart_data", [], {});
        const canvas = this.el.querySelector("#chart_mo_states");
        if (canvas) {
            new Chart(canvas, {
                type: "bar",
                data: {
                    labels: result.labels,
                    datasets: [{
                        label: "Manufacturing Orders",
                        data: result.data,
                        backgroundColor: result.colors,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: "MO Status Overview"
                        },
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            console.warn("Chart canvas not found");
        }
    }
}

BedDashboardChart.template = "bed_dashboard.ChartContainer";

registry.category("actions").add("bed_dashboard_chart", BedDashboardChart);
