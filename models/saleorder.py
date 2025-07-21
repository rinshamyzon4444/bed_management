from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self._create_manufacturing_orders_if_needed()
        return res

    def _create_manufacturing_orders_if_needed(self):
        Mo = self.env['mrp.production']
        for order in self:
            for line in order.order_line:
                product = line.product_id
                ordered_qty = line.product_uom_qty
                on_hand_qty = product.qty_available

                if product.type == 'product' and ordered_qty > on_hand_qty:
                    required_qty = ordered_qty - on_hand_qty
                    unit_uom = self.env['uom.uom'].search([('name', '=', 'Units'), ('category_id.name', '=', 'Unit')],
                                                          limit=1)
                    bom = self.env['mrp.bom']._bom_find(products=product, company_id=self.company_id.id)

                    if bom:
                        Mo.create({
                            'product_id': product.id,
                            'product_qty': required_qty,
                            'product_uom_id': unit_uom.id,
                            'bom_id': bom.id,
                            'origin': order.name,
                            'date_start': fields.Datetime.now(),
                            'location_src_id': bom.picking_type_id.default_location_src_id.id,
                            'location_dest_id': bom.picking_type_id.default_location_dest_id.id,
                            'picking_type_id': bom.picking_type_id.id,
                        })
                    else:
                        Mo.create({
                            'product_id': product.id,
                            'product_qty': required_qty,
                            'product_uom_id': unit_uom.id,
                            'origin': order.name,
                            'date_start': fields.Datetime.now(),
                        })