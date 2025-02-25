# custom_addons/test_applicant/controllers/login_as.py
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError

class LoginAsController(http.Controller):

    @http.route('/web/login_as', type='http', auth='user')
    def login_as(self, user_id, **kwargs):
        """Authenticates as another user"""
        user_id = int(user_id)
        current_user = request.env.user

        current_user = request.env.user

        # Block the Superuser (ID=2) from using this feature
        if current_user.id == 2:
            raise AccessError("Superuser cannot use the Login As feature.")

        # Ensure only admin users can use this feature
        if not current_user.has_group('base.group_system'):
            raise AccessError("Only administrators can use this feature.")

        # Prevent logging in as superuser (ID=2)
        if user_id == 2:
            raise AccessError("You cannot log in as the superuser.")

        # Switch to the selected user
        user = request.env['res.users'].sudo().browse(user_id)
        request.session.uid = user.id
        return request.redirect('/web')