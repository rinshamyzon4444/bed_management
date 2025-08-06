from odoo import models, fields, api
from datetime import datetime, timedelta, date

class BedProductDashboard(models.Model):
    _name = 'bed.product.dashboard'
    _description = 'Bed Product Manufacturing Dashboard'

    @api.model
    def get_user_group_info(self):
        user = self.env.user
        return {
            'is_superadmin': user.has_group('bed_management.group_bedmanagement_superadmin'),
            'is_production_manager': user.has_group('bed_management.group_bedmanagement_productionManager'),
            'is_quality_inspector': user.has_group('bed_management.group_bedmanagement_QualityInspector'),
        }

    @api.model
    def get_tiles_data(self):
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())

        # MRP Orders
        mrp_orders = self.env['mrp.production'].search_count([])
        mrp_draft_count = self.env['mrp.production'].search_count([('state', '=', 'draft')])
        mrp_confirmed_count = self.env['mrp.production'].search_count([('state', '=', 'confirmed')])
        mrp_in_progress_count = self.env['mrp.production'].search_count([('state', '=', 'progress')])
        mrp_to_close_count = self.env['mrp.production'].search_count([('state', '=', 'to_close')])
        mrp_done_count = self.env['mrp.production'].search_count([('state', '=', 'done')])

        return {
            'mrp_order': mrp_orders,
            'mrp_draft_count' : mrp_draft_count,
            'mrp_confirmed_count' : mrp_confirmed_count,
            'mrp_in_progress_count' : mrp_in_progress_count,
            'mrp_to_close_count' : mrp_to_close_count,
            'mrp_done_count' : mrp_done_count,
        }
    # mo production

    @api.model
    def get_production_volume_by_date(self):
        self.env.cr.execute("""
                SELECT 
                    to_char(date_start, 'YYYY-MM-DD') AS production_date,
                    COUNT(*) AS production_count
                FROM mrp_production
                WHERE date_start IS NOT NULL
                GROUP BY production_date
                ORDER BY production_date ASC
            """)
        result = self.env.cr.fetchall()

        labels = []
        data = []

        for rec in result:
            labels.append(rec[0])
            data.append(rec[1])

        return {
            'labels': labels,
            'data': data
        }

    # raw material by bed type
    @api.model
    def get_raw_material_data(self):
        productions = self.env['mrp.production'].search([('state', '=', 'done')])
        raw_data = {}
        pie_total = {}

        for production in productions:
            bed_type = production.product_id.name
            for move in production.move_raw_ids.filtered(lambda m: m.state == 'done'):
                material = move.product_id.name
                qty = move.product_uom_qty

                raw_data.setdefault(material, {})
                raw_data[material][bed_type] = raw_data[material].get(bed_type, 0) + qty

                pie_total[bed_type] = pie_total.get(bed_type, 0) + qty

        # Prepare line chart format
        labels = sorted(set(bt for mat in raw_data.values() for bt in mat))
        datasets = []
        for material, values in raw_data.items():
            dataset = {
                'label': material,
                'data': [values.get(label, 0) for label in labels],
                'fill': False,
            }
            datasets.append(dataset)

        # PIE CHART
        pie = {
            'labels': list(pie_total.keys()),
            'data': list(pie_total.values()),
            'colors': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        }

        return {
            'labels': labels,
            'datasets': datasets,
            'pie': pie,
        }


#     quality check and list wo

    @api.model
    def get_latest_workorders(self):
        workorders = self.env['mrp.workorder'].search([], order='id desc', limit=10)

        passed = failed = 0
        workorder_list = []

        for wo in workorders:
            if wo.inspection_result == 'pass':
                passed += 1
            elif wo.inspection_result == 'fail':
                failed += 1

            workorder_list.append({
                'id': wo.id,
                'name': wo.name,
                'mo_name': wo.production_id.name if wo.production_id else "",
                'product_name': wo.production_id.product_id.name if wo.production_id and wo.production_id.product_id else "",
                'workcenter_id': wo.workcenter_id.name if wo.workcenter_id else "",
                'inspection_result': wo.inspection_result,
                'state': wo.state,
                'date_start': wo.date_start.strftime("%Y-%m-%d %H:%M") if wo.date_start else "",
                'date_end': wo.date_finished.strftime("%Y-%m-%d %H:%M") if wo.date_finished else "",
            })

        return {
            'workorders': workorder_list,
            'quality_summary': {
                'passed': passed,
                'failed': failed,
                'total': len(workorders),
            }
        }