from odoo import models, fields

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    cost_per_employee_hour = fields.Float(string="Cost per Hour")
    expense_account_id = fields.Many2one('account.account', string="Expense Account")
    allowed_employee_ids = fields.Many2many('hr.employee', string="Allowed Employees")
