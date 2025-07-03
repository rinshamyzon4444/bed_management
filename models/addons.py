from odoo import models, fields ,api

class BedAddon(models.Model):
    _name = 'bed.addon'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bed Add-on'

    name = fields.Char(required=True)
    description = fields.Text()
    product_id = fields.Many2one('product.product', string="Related Product", readonly=True)



    @api.model
    def create(self, vals):
        addon = super(BedAddon, self).create(vals)
        product = self.env['product.product'].create({
            'name': addon.name,
            'type': 'consu',
            'default_code': f"ADDON-{addon.id}",
            'sale_ok': True,
            'purchase_ok': False,
        })
        addon.product_id = product.id
        return addon