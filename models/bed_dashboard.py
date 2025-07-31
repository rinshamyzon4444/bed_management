from odoo import models, fields, api
from datetime import datetime, timedelta, date
from collections import defaultdict

class BedProductDashboard(models.Model):
    _name = 'bed.product.dashboard'
    _description = 'Bed Product Manufacturing Dashboard'

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
