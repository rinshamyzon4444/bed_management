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

    def _set_wood_type_attribute(self, wood_type_value):
        attribute = self.env['product.attribute'].search([('name', '=', 'Wood Type')], limit=1)
        if not attribute:
            attribute = self.env['product.attribute'].create({
                'name': 'Wood Type',
                'string' : 'Wood Type',
                'create_variant': 'always',
            })

        attr_value = self.env['product.attribute.value'].search([
            ('name', '=', wood_type_value),
            ('attribute_id', '=', attribute.id)
        ], limit=1)
        if not attr_value:
            attr_value = self.env['product.attribute.value'].create({
                'name': wood_type_value,
                'attribute_id': attribute.id
            })

        for template in self:
            line = self.env['product.template.attribute.line'].search([
                ('product_tmpl_id', '=', template.id),
                ('attribute_id', '=', attribute.id)
            ], limit=1)

            if line:
                line.write({'value_ids': [(6, 0, [attr_value.id])]})
            else:
                self.env['product.template.attribute.line'].create({
                    'product_tmpl_id': template.id,
                    'attribute_id': attribute.id,
                    'value_ids': [(6, 0, [attr_value.id])],
                })

    @api.model
    def write(self, vals):
        res = super().write(vals)
        if 'wood_type' in vals:
            for rec in self:
                rec._set_wood_type_attribute(vals['wood_type'])
        return res