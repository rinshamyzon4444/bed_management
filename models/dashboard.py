from odoo import models, fields, api


class BedDashboard(models.Model):
    _name = 'bed.dashboard'
    _description = 'Bed Manufacturing Dashboard'

    total_mrp_orders = fields.Integer(compute='_compute_mrp_counts')
    mrp_draft_count = fields.Integer(compute='_compute_mrp_counts')
    mrp_confirmed_count = fields.Integer(compute='_compute_mrp_counts')
    mrp_in_progress_count = fields.Integer(compute='_compute_mrp_counts')
    mrp_to_close_count = fields.Integer(compute='_compute_mrp_counts')
    mrp_done_count = fields.Integer(compute='_compute_mrp_counts')

    raw_material_move_ids = fields.Many2many('stock.move', relation='bed_dashboard_stock_move_rel',
                                             column1='dashboard_id',
                                             column2='move_id',
                                             string='Raw Material Moves',
                                             compute='_compute_raw_material_usage')


    def action_refresh_dashboard(self):
        self._compute_mrp_counts()
        self._compute_raw_material_usage()

    @api.depends()
    def _compute_mrp_counts(self):
        for rec in self:
            rec.total_mrp_orders = self.env['mrp.production'].search_count([])
            rec.mrp_draft_count = self.env['mrp.production'].search_count([('state', '=', 'draft')])
            rec.mrp_confirmed_count = self.env['mrp.production'].search_count([('state', '=', 'confirmed')])
            rec.mrp_in_progress_count = self.env['mrp.production'].search_count([('state', '=', 'progress')])
            rec.mrp_to_close_count = self.env['mrp.production'].search_count([('state', '=', 'to_close')])
            rec.mrp_done_count = self.env['mrp.production'].search_count([('state', '=', 'done')])

    def _compute_raw_material_usage(self):
        for rec in self:
            rec.raw_material_move_ids = self.env['stock.move'].search([
                ('raw_material_production_id', '!=', False),
            ], order='date desc').ids

    # Actions to open MRP by stage
    def action_open_mrp_all(self):
        return self._get_mrp_action([])

    def action_open_mrp_draft(self):
        return self._get_mrp_action([('state', '=', 'draft')])

    def action_open_mrp_confirmed(self):
        return self._get_mrp_action([('state', '=', 'confirmed')])

    def action_open_mrp_in_progress(self):
        return self._get_mrp_action([('state', '=', 'progress')])

    def action_open_mrp_to_close(self):
        return self._get_mrp_action([('state', '=', 'to_close')])

    def action_open_mrp_done(self):
        return self._get_mrp_action([('state', '=', 'done')])

    def _get_mrp_action(self, domain):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'domain': domain,
            'view_mode': 'tree,form,graph,pivot',
            'target': 'current',
        }

    def action_open_raw_materials(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move',
            'domain': [('raw_material_production_id', '!=', False)],
            'view_mode': 'tree,form,pivot,graph',
            'target': 'current',
        }


   # graph
    @api.model
    def get_mo_chart_data(self):
        states = ['draft', 'confirmed', 'in_progress', 'to_close', 'done']
        data = []
        labels = []
        colors = []
        color_map = {
            'draft': '#95a5a6',
            'confirmed': '#f1c40f',
            'in_progress': '#3498db',
            'to_close': '#e67e22',
            'done': '#27ae60'
        }

        for state in states:
            count = self.env['mrp.production'].search_count([('state', '=', state)])
            labels.append(state.title())
            data.append(count)
            colors.append(color_map.get(state, "#000"))

        return {
            'labels': labels,
            'data': data,
            'colors': colors,
        }


