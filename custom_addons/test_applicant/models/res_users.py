# custom_addons/test_applicant/models/res_users.py
from odoo import models, fields
from odoo.exceptions import AccessError, ValidationError
from odoo import api

class ResUsers(models.Model):
    _inherit = 'res.users'

    show_login_as = fields.Boolean(string="Show Login As",compute='_compute_show_login_as')

    def action_login_as(self):
        if self.id == 2:
            raise ValidationError("Cannot log in as superuser.")
        return {
            'type': 'ir.actions.client',
            'tag': 'login',
            'params': {'uid': self.id},
        }

    @api.depends('groups_id')
    def _compute_show_login_as(self):
        """ Hide the button for the Superuser (ID=2) """
        for user in self:
            user.show_login_as = user.id != 2

