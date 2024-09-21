from odoo import models, fields


class Department(models.Model):
    _name = 'hms.department'
    _description = 'Department'

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    doctor_ids = fields.Many2many('hms.doctor')
    patient_ids = fields.One2many('hms.patient', 'department_id')
