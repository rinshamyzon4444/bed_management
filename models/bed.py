from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    list_price = fields.Float(string="Retail Price")
    wholesale_price = fields.Float(string="Wholesale Price", help="The Wholesale amount of product")

    is_bed = fields.Boolean(string="Is Bed Product", tracking=True, default=False)

    BED_TYPES = [
        ('king', 'King'),
        ('queen', 'Queen'),
        ('single', 'Single'),
        ('bunk', 'Bunk'),
        ('custom', 'Custom'),
    ]

    bed_type = fields.Selection(
        BED_TYPES,
        string="Bed Type",
        tracking=True
    )

    wood_type_ids = fields.Many2many(
        'product.attribute.value',
        'product_template_wood_type_rel',
        'product_tmpl_id',
        'attribute_value_id',
        string="Wood Types",
        domain="[('attribute_id.name', 'ilike', 'Wood Type')]",
        tracking=True,
    )

    detailed_type = fields.Selection(default='product')  # 'product' = Storable
    sale_ok = fields.Boolean(default=True)
    purchase_ok = fields.Boolean(default=True)

    length = fields.Float(string='Length (in")')
    width = fields.Float(string='Width (in")')
    height = fields.Float(string='Height (in")')

    low_stock_threshold = fields.Integer(string="Minimum Quantity", default=3,
                                         help="The minimum quantity allowed in stock. If actual stock drops below this value, a low stock warning will be triggered.")
    restock_quantity = fields.Integer(string="Suggested Restock Quantity", default=10,
                                      help="Suggested quantity to replenish when stock is low.")

    # Searches for an attribute in product.attribute. If found, it returns that attribute else it creates a new attribute with the name "Wood Type"
    def _ensure_wood_type_attribute(self):
        attribute = self.env['product.attribute'].search([('name', 'ilike', 'wood_type')], limit=1)
        if not attribute:
            attribute = self.env['product.attribute'].create({
                'name': 'Wood Type',
                'create_variant': 'always',
            })
        return attribute

    # method ensures that the selected wood types (wood_type_ids) on a product template are reflected
    # in its variant-generating attribute lines for the "Wood Type" attribute.
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

    # The create method overrides the default create behavior to sync the wood_type_ids with attribute lines after a new product template is created.
    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if vals.get('wood_type_ids'):
            rec._sync_wood_type_to_attribute_lines()
        return rec

    # This write method updates the record and, if wood_type_ids has changed, synchronizes those wood types with the product's attribute lines
    # @api.onchange('wood_type_ids')
    def write(self, vals):
        res = super().write(vals)
        if 'wood_type_ids' in vals:
            self._sync_wood_type_to_attribute_lines()
        return res

    # This method checks if a product's total available quantity is below its low stock threshold
    # and posts a low stock alert message in the chatter if it is.
    def check_and_notify_low_stock(self):
        for product in self:
            qty_available = sum(product.product_variant_ids.mapped('qty_available'))

            if qty_available < product.low_stock_threshold:
                message = (
                    f"⚠️ Low Stock Alert!\n"
                    f"Product: {product.name}\n"
                    f"Current Qty: {qty_available}\n"
                    f"Recommended Restock: {product.restock_quantity}"
                )
                product.message_post(body=message, subtype_xmlid="mail.mt_note")
                # if self.env.context.get('raise_warning', False):
                #     raise UserError(message)
