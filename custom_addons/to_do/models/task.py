
from odoo import models, fields



class Task(models.Model):
    _name = 'td.task'
    _description = 'Task'

    name = fields.Char()
    number = fields.Integer()
    tag = fields.Char()
    state = fields.Selection([
        ('new', 'New'),
        ('doing', 'Doing'),
        ('done', 'Done'),
        ], default='new')
    file = fields.Binary()
    assigned_to = fields.Many2one('res.users')
    description = fields.Text(string='Description')

    def action_new(self):
        self.state = 'new'

    def action_doing(self):
        self.state = 'doing'

    def action_done(self):
        self.state = 'done'

