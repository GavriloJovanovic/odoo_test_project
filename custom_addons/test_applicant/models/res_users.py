# custom_addons/test_applicant/models/res_users.py
from odoo import models, fields
from odoo.exceptions import AccessError, ValidationError
from odoo import api

class ResUsers(models.Model):
    _inherit = 'res.users'

    def action_login_as(self):
        """Allows admin to log in as another user except the superuser"""
        self.ensure_one()

        # Prevent logging in as superuser (ID=2)
        if self.id == 2:
            raise AccessError("You cannot log in as the superuser (admin).")

        # Get login URL
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/login_as?user_id={self.id}',
            'target': 'self',
        }


