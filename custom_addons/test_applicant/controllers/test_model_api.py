import json
from odoo import http
from odoo.http import request
# custom_addons/test_applicant/controllers/test_model_api.py


class TestModelAPI(http.Controller):

    @http.route('/api/test_model', type='json', auth='public', methods=['GET'])
    def get_test_models(self, **kwargs):
        """Returns a list of all records."""
        """Returns a list of all records."""
        records = request.env['test.model'].sudo().search([])
        data = [{'id': rec.id, 'name': rec.name, 'reference_code': rec.reference_code, 'state': rec.state} for rec in records]

        return data

    @http.route('/api/test_model', type='json', auth='user', methods=['POST'], csrf=False)
    def create_test_model(self, **kwargs):
        """Creates a new record (requires authentication)."""

        # Debug authentication
        print("Session UID:", request.session.uid)
        print("User ID:", request.env.user.id)
        print("User Name:", request.env.user.name)
        print("Is Superuser:", request.env.user._is_superuser())

        if not request.session.uid:
            return {"error": "User not authenticated"}

        if 'name' not in kwargs:
            return {'error': 'Missing required field: name'}

        new_record = request.env['test.model'].sudo().create({'name': kwargs['name']})

        return {
            'id': new_record.id,
            'reference_code': new_record.reference_code,
            'state': new_record.state
        }


