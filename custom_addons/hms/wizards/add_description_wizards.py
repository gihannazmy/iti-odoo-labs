from odoo import models, fields, api


class AddDescription(models.TransientModel):
   _name = 'hms.add.description'


   date = fields.Date(string='Date', required=True, default=fields.Date.today())
   description = fields.Char(string='Description', required=True)
   patient_id = fields.Many2one('hms.patient', string='Patient', required=True)


   def action_open_line_wizard(self):
       self.ensure_one()
       self.patient_id.description = self.description.id