from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'res.partner']

    vat = fields.Char(string="Tax ID")
    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")

    @api.constrains('email', 'related_patient_id')
    def _check_email_in_patient(self):
        for rec in self:
            if rec.email:
                patient_with_email = self.env['hms.patient'].search([('email', '=', rec.email)], limit=1)
                if patient_with_email:
                    raise ValidationError(f"The email '{rec.email}' is already linked to a patient (ID: {patient_with_email.id}). Please use a different email.")


    @api.constrains('vat', 'customer')
    def _check_tax_id(self):
        for rec in self:
            if rec.customer and not rec.vat:
                raise ValidationError("The Tax ID field is mandatory for CRM customers.")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError(f"You cannot delete the customer '{rec.name}' since they are linked to a patient.")
        return super(ResPartner, self).unlink()