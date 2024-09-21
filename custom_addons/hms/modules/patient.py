from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import re

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _inherit = ['res.partner', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-')
    ])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
        ], default='undetermined')
    department_id = fields.Many2one('hms.department')
    doctor_ids = fields.Many2many('hms.doctor')
    patient_line_ids = fields.One2many('hms.patient.line', 'patient_id', string="Log History")
    age = fields.Integer(compute='_compute_age')
    department_capacity = fields.Integer(compute="_compute_department_capacity")
    hide_history = fields.Boolean(compute='_compute_hide_history')
    email = fields.Char(unique=True)

    _sql_constraints = [
        ('email_uniq', 'unique(email)', 'The email must be unique!')
    ]

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                match = re.match(r"[^@]+@[^@]+\.[^@]+", rec.email)
                if not match:
                    raise ValidationError("Please enter a valid email address.")
    def action_undetermined(self):
        self.state = 'undetermined'

    def action_good(self):
        self.state = 'good'

    def action_fair(self):
        self.state = 'fair'

    def action_serious(self):
        self.state = 'serious'

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                patient.age = relativedelta(fields.Date.today(), patient.birth_date).years
            else:
                patient.age = 0

    @api.depends('department_id')
    def _compute_department_capacity(self):
        for rec in self:
            if rec.department_id:
                rec.department_capacity = rec.department_id.capacity
            else:
                rec.department_capacity = 0

    @api.onchange('age')
    def _onchange_age(self):
        if self.age:
            if self.age < 50:
                self.history = False

        if self.age < 30 and not self.pcr:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Automatically Checked",
                    'message': "The PCR field has been automatically checked because the patient's age is below 30.",
                }
            }

    @api.model
    def write(self, vals):
        for rec in self:
            if 'state' in vals and rec.state != vals['state']:
                self.env['hms.patient.line'].create({
                    'patient_id': rec.id,
                    'description': f"State changed to {vals['state']}",
                    'user_id': self.env.user.id,
                    'date': fields.Datetime.now(),
                })
        return super(Patient, self).write(vals)

    @api.constrains('department_id')
    def _check_department_open(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("You cannot select a closed department. Please choose an open department.")


    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR ratio must be filled .")


class PatientLine(models.Model):
    _name = 'hms.patient.line'
    _description = 'Patient Log History'

    date = fields.Date()
    description = fields.Char()
    user_id = fields.Many2one('res.users', string='Logged By', default=lambda self: self.env.user)
    patient_id = fields.Many2one('hms.patient')

