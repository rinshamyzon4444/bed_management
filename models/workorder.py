from odoo import models, fields , api

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


