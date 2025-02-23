import json
from odoo import http
from odoo.http import request
# custom_addons/test_applicant/controllers/test_model_api.py

class TestModelAPI(http.Controller):

    @http.route('/api/test_model', type='json', auth='public', methods=['GET'])
    def get_test_models(self, **kwargs):
        """Returns a list of all records."""
        """Returns a list of all records."""
        print("Ja SAM OVDE")
        records = request.env['test.model'].sudo().search([])
        data = [{'id': rec.id, 'name': rec.name, 'reference_code': rec.reference_code, 'state': rec.state} for rec in records]

        # ✅ Fix: Return a JSON response properly
        return data  # No need to use json.dumps()

    @http.route('/api/test_model', type='json', auth='user', methods=['POST'], csrf=False)
    def create_test_model(self, **kwargs):
        """Creates a new test.model record (Requires Authentication)."""
        data = request.jsonrequest  # Get JSON data from request
        required_fields = ['name', 'description']

        # Validate required fields
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}

        try:
            new_record = request.env['test.model'].sudo().create({
                'name': data['name'],
                'description': data.get('description', ''),
                'state': 'draft'
            })
            return {'success': True, 'id': new_record.id, 'reference_code': new_record.reference_code}
        except Exception as e:
            return {'error': str(e)}

