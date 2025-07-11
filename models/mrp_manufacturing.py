from odoo import models,fields,api , _
from odoo.exceptions import UserError, ValidationError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    max_allowed_qty = fields.Float("Max allowed", default=30.0)

    def button_mark_done(self):
        for order in self:
            product = order.product_id
            uom_qty = order.product_qty
            available_qty = product.qty_available
            max_allowed = order.max_allowed_qty

            total_after = available_qty + uom_qty

            if max_allowed and total_after > max_allowed:
                raise ValidationError(_(
                    "You are not allowed to manufacture %.1f units of '%s'.\n"
                    "Current Available: %.1f, Total after Manufacturing: %.1f,\n"
                    "Maximum Allowed: %.1f."
                ) % (
                    uom_qty, product.display_name,
                    available_qty, total_after, max_allowed
                ))

        return super(MrpProduction, self).button_mark_done()

    def action_add_from_catalog_raw(self):
        mo = self.env['mrp.production'].browse(self.env.context.get('order_id'))
        return mo.with_context(child_field='move_raw_ids').action_add_from_catalog()
