from odoo import models, fields, api


class BedProduct(models.Model):
    _name = 'bed.product'
    _description = 'Bed Product'

    name = fields.Char(required=True)
    bed_type = fields.Selection([
        ('king', 'King'),
        ('queen', 'Queen'),
        ('single', 'Single'),
        ('bunk', 'Bunk'),
        ('custom', 'Custom'),
    ], required=True)

    length = fields.Float(string="Length (cm)")
    width = fields.Float(string="Width (cm)")
    height = fields.Float(string="Height (cm)")

    wood_type = fields.Char()
    addon_ids = fields.Many2many('bed.addon', string='Add-ons')

    price = fields.Float(string="Price")
    product_id = fields.Many2one(
        'product.product',
        string="Inventory Product",
        readonly=True,
    )

    @api.model
    def create(self, vals):
        bed = super(BedProduct, self).create(vals)
        # auto-create a stockable product for this bed
        product = self.env['product.product'].create({
            'name': bed.name,
            'type': 'product',  # stockable product
            'default_code': f"BED-{bed.id}",
            'sale_ok': True,
            'purchase_ok': True,
            'list_price': bed.price or 0.0,
        })
        bed.product_id = product.id
        return bed

