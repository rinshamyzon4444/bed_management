from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_bed = fields.Boolean(string="Is Bed Product", tracking=True, default=False)
    bed_type = fields.Selection([
        ('king', 'King'),
        ('queen', 'Queen'),
        ('single', 'Single'),
        ('bunk', 'Bunk'),
        ('custom', 'Custom'),
    ], string="Bed Type", tracking=True)

    wood_type = fields.Char(string="Wood Type", tracking=True)

    detailed_type = fields.Selection(default='product')  # 'product' = Storable
    sale_ok = fields.Boolean(default=True)
    purchase_ok = fields.Boolean(default=True)

    length = fields.Float(string="Length (cm)")
    width = fields.Float(string="Width (cm)")
    height = fields.Float(string="Height (cm)")