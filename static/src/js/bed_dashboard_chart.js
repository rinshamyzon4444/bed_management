/** @odoo-module */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart , useState } from "@odoo/owl";

class BedProductDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
        this.viewService = useService("view");
        this.state = useState({ mrp_order: 0, mrp_draft_count : 0 , mrp_confirmed_count : 0, mrp_in_progress_count : 0, mrp_to_close_count : 0, mrp_done_count : 0});

        // Load data before rendering
        onWillStart(async () => {
            const result = await this.orm.call("bed.product.dashboard", "get_tiles_data", [], {});
            this.state.mrp_order = result.mrp_order;
            this.state.mrp_draft_count = result.mrp_draft_count;
            this.state.mrp_confirmed_count = result.mrp_confirmed_count;
            this.state.mrp_in_progress_count = result.mrp_in_progress_count;
            this.state.mrp_to_close_count = result.mrp_to_close_count;
            this.state.mrp_done_count = result.mrp_done_count;

        });
    }

    openMrpView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'MRP Orders',
            res_model: 'mrp.production',
            view_mode: 'tree,graph,pivot',
            views: [
                [false, 'tree'],
                [false, 'graph'],
                [false, 'pivot'],
            ],
            target: 'current',
        });
    }
    openMrpDraftView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'MRP Orders (Draft)',
            res_model: 'mrp.production',
            view_mode: 'tree,graph',
            views: [
                [false, 'tree'],
                [false, 'graph']
            ],
            domain: [['state', '=', 'draft']],  // Only shows draft records
            target: 'current',
        });
    }
    openMrpConfirmedView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'MRP Orders (Draft)',
            res_model: 'mrp.production',
            view_mode: 'tree,graph',
            views: [
                [false, 'tree'],
                [false, 'graph']
            ],
            domain: [['state', '=', 'confirmed']],  // Only shows confirmed records
            target: 'current',
        });
    }
    openMrpInProgressView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'MRP Orders (Draft)',
            res_model: 'mrp.production',
            view_mode: 'tree,graph',
            views: [
                [false, 'tree'],
                [false, 'graph']
            ],
            domain: [['state', '=', 'progress']],  // Only shows progress records
            target: 'current',
        });
    }
    openMrpToCloseView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'MRP Orders (Draft)',
            res_model: 'mrp.production',
            view_mode: 'tree,graph',
            views: [
                [false, 'tree'],
                [false, 'graph']
            ],
            domain: [['state', '=', 'to_close']],  // Only shows to-close records
            target: 'current',
        });
    }
    openMrpDoneView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'MRP Orders (Draft)',
            res_model: 'mrp.production',
            view_mode: 'tree,graph',
            views: [
                [false, 'tree'],
                [false, 'graph']
            ],
            domain: [['state', '=', 'done']],  // Only shows to-close records
            target: 'current',
        });
    }

}

BedProductDashboard.template = "bed_management.bed_product_dashboard_template";

registry.category("actions").add("bed_product_dashboard_tag", BedProductDashboard);