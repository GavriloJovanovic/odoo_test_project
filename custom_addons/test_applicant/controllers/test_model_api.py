import json
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import requests
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
            raise ValidationError("User not authenticated")

        if 'name' not in kwargs:
            raise ValidationError("Missing required field: name")

        new_record = request.env['test.model'].sudo().create({'name': kwargs['name']})

        return {
            'id': new_record.id,
            'reference_code': new_record.reference_code,
            'state': new_record.state
        }


    @http.route('/api/llm', type='json', auth='public', methods=['POST'], csrf=False)
    def call_llm(self, **kwargs):
        """
        Handles LLM prompt calls by fetching all users and formatting the prompt.
        Expects a JSON body with {"question": "some user question"}.
        """

        # Ensure the request contains a question
        user_question = kwargs.get('question')
        if not user_question:
            return {"error": "Missing required field: question"}

        # Fetch all users from PostgreSQL (res.users model)
        users = request.env['test.model'].sudo().search([])
        user_data = [{'id': rec.id, 'name': rec.name, 'reference_code': rec.reference_code, 'state': rec.state} for rec in users]

        # Define the system prompt
        system_prompt = (
            "You are an AI assistant with access to the Odoo user database.\n"
            "Here are the available users:\n"
        )

        # Format users into the prompt
        user_details = "\n".join([f"ID: {user['id']}, Name: {user['name']}, Reference code: {user['reference_code']}"
                                  f", State: {user['state']}, " for user in user_data])

        # Construct the final prompt
        prompt = f"{system_prompt}{user_details}\n\nFor this sys_prompt answer this: {user_question}"

        print(prompt)  # Debugging

        # Send the request to LLaMA 2 (running on localhost)
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama2", "prompt": prompt, "stream": False}
            )
            response_data = response.json()

            # Extract the response text
            llm_answer = response_data.get("response", "").strip()

        except Exception as e:
            return {"error": f"LLaMA 2 request failed: {str(e)}"}

        return {"question": user_question, "answer": llm_answer}

