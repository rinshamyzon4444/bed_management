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

    wood_type_ids = fields.Many2many(
        'product.attribute.value',
        'product_template_wood_type_rel',
        'product_tmpl_id',
        'attribute_value_id',
        string="Wood Types",
        domain="[('attribute_id.name', '=', 'Wood Type')]",
        tracking=True,
    )

    detailed_type = fields.Selection(default='product')  # 'product' = Storable
    sale_ok = fields.Boolean(default=True)
    purchase_ok = fields.Boolean(default=True)

    length = fields.Float(string="Length (cm)")
    width = fields.Float(string="Width (cm)")
    height = fields.Float(string="Height (cm)")

    def _ensure_wood_type_attribute(self):
        attribute = self.env['product.attribute'].search([('name', 'ilike', 'Wood Type')], limit=1)
        if not attribute:
            attribute = self.env['product.attribute'].create({
                'name': 'Wood Type',
                'create_variant': 'always',
            })
        return attribute

    def _sync_wood_type_to_attribute_lines(self):
        attribute = self._ensure_wood_type_attribute()
        for template in self:
            line = self.env['product.template.attribute.line'].search([
                ('product_tmpl_id', '=', template.id),
                ('attribute_id', '=', attribute.id)
            ], limit=1)

            wood_values = template.wood_type_ids.filtered(lambda v: v.attribute_id.id == attribute.id)

            if line:
                line.write({'value_ids': [(6, 0, wood_values.ids)]})
            else:
                self.env['product.template.attribute.line'].create({
                    'product_tmpl_id': template.id,
                    'attribute_id': attribute.id,
                    'value_ids': [(6, 0, wood_values.ids)],
                })

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if vals.get('wood_type_ids'):
            rec._sync_wood_type_to_attribute_lines()
        return rec

    def write(self, vals):
        res = super().write(vals)
        if 'wood_type_ids' in vals:
            self._sync_wood_type_to_attribute_lines()
        return res