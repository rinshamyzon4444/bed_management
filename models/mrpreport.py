from odoo import models, fields

class MrpReport(models.Model):
    _inherit = 'stock.move'

    bed_product_id = fields.Many2one(
        'product.product',
        string='Bed Type',
        related='raw_material_production_id.product_id',
        store=True
    )