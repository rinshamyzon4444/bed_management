from odoo import models, fields , api , _
from odoo.exceptions import UserError

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'


    assigned_employee_ids = fields.Many2many(
        'hr.employee',
        'mrp_workorder_assigned_employee_rel',
        'workorder_id',
        'employee_id',
        string='Assigned '
    )

    allowed_employee_ids = fields.Many2many(
        'hr.employee',
        string='Allowed Employees (Related)',
        related='workcenter_id.allowed_employee_ids',
        readonly=True
    )

    assigned_user_ids = fields.Many2many(
        'res.users',
        compute='_compute_assigned_user_ids',
        string='Assigned Users',
        store=False
    )

    @api.depends('assigned_employee_ids.user_id')
    def _compute_assigned_user_ids(self):
        for workorder in self:
            workorder.assigned_user_ids = workorder.assigned_employee_ids.mapped('user_id')

# Quality check in workorder


    inspection_result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('measure', 'Measured')
    ], string="Inspection Result")
    inspection_notes = fields.Text("Inspection Notes")
    inspection_image = fields.Binary("Inspection Image")



    def write(self, vals):
        res = super().write(vals)

        if vals.get('state') == 'done':
            for workorder in self:
                # Get all workorders from the same MO
                related_workorders = workorder.production_id.workorder_ids
                failed_workorders = related_workorders.filtered(lambda w: w.inspection_result == 'fail')
                if failed_workorders:
                    failed_names = "\n".join(f"- {w.name}" for w in failed_workorders)
                    raise UserError(_(
                        "Cannot complete Manufacturing Order.\n"
                        "The following Work Orders failed inspection:(Quality Check)\n%s"
                    ) % failed_names)

        return res


