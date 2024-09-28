// /** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { onMounted, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class OwlSalesDashboard extends Component {
    setup() {
        this.instances = useState([]);
        this.orm = useService("orm");
        this.action = useService("action");
        this.currentCharts = {};

        onMounted(() => {
            this.fetchInstances();
        });
    }

    async fetchInstances() {
        const instances = await this.orm.call("amazon.instance.ept", "DashboardBoxValues", [[]]);
        this.instances.push(...instances);
        this.instances.forEach(instance => {
            const staticSalesData = [10, 20, 15, 30, 25, 35, 10]; // Example static sales data
            this.waitForCanvas(instance.id, staticSalesData, 'current_week');
        });
    }

    waitForCanvas(instanceId, salesData, period) {
        const canvasId = 'chart-' + instanceId;
        const interval = setInterval(() => {
            const ctx = document.getElementById(canvasId);
            if (ctx) {
                clearInterval(interval);
                this.renderChart(canvasId, salesData, period);
                this.addDropdownListeners(instanceId);
            }
        }, 100); // Check every 100 milliseconds
    }

    renderChart(canvasId, salesData, period) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        const labels = this.getLabelsForPeriod(period);
        if (this.currentCharts[canvasId]) {
            this.currentCharts[canvasId].destroy();
        }
        this.currentCharts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sales',
                    data: salesData,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    getLabelsForPeriod(period) {
        switch (period) {
            case 'current_week':
                return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
            case 'current_month':
                return Array.from({ length: 31 }, (_, i) => i + 1);
            case 'current_year':
                return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            case 'all':
                return ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 'Year 6', 'Year 7'];
            default:
                return [];
        }
    }

    async fetchSalesData(instanceId, period) {
        // This is where you fetch the data based on the period selected.
        // For now, we'll use static data as an example.
        const salesData = {
            'current_week': [10, 20, 15, 30, 25, 35, 10],
            'current_month': Array.from({ length: 31 }, (_, i) => i + 1),
            'current_year': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'all': [10, 20, 30, 40, 50, 60, 70]
        };
        return salesData[period];
    }

    async addDropdownListeners(instanceId) {
        const periodSelect = document.querySelector(`#period-select-${instanceId}`);
        const fullfillmentSelect = document.querySelector(`#fulfillment-select-${instanceId}`);
        // ##############

        fullfillmentSelect.addEventListener('change', async (event) => {
            const period = event.target.value;
            console.log("fullfillmentSelect....",period,"instanceId..",instanceId)
        });
        //###############
        periodSelect.addEventListener('change', async (event) => {
            const period = event.target.value;
            console.log("periodSelect....",period,"instanceId...",instanceId)
            const salesData = await this.fetchSalesData(instanceId, period);
            this.renderChart('chart-' + instanceId, salesData, period);
        });
    }

    async open_amazon_product(instanceId) {
        this.action.doAction({
            name: "Amazon Products",
            type: "ir.actions.act_window",
            res_model: "amazon.product.ept",
            views: [[false, "list"]],
            domain: [['instance_id', '=', instanceId]],
            target: "current",
        });
    }

    async open_sales_order(instanceId, fulfillmentBy) {
        this.action.doAction({
            name: "Sales Orders",
            type: "ir.actions.act_window",
            res_model: "sale.order",
            views: [[false, "list"]],
            domain: [['amz_instance_id', '=', instanceId], ['amz_fulfillment_by', '=', fulfillmentBy]],
            target: "current",
        });
    }
}

OwlSalesDashboard.template = "amazon_odoo_linker.sales_dashboard";
registry.category("actions").add("amazon_odoo_linker.sales_dashboard", OwlSalesDashboard);
