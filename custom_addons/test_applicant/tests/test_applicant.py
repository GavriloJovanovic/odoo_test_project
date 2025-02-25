# custom_addons/test_applicant/tests/test_applicant.py
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError
from odoo import fields


class TestApplicant(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.TestModel = cls.env['test.model']
        cls.record = cls.TestModel.create({
            'name': 'Test Record',
            'description': 'A test record for validation'
        })

    def test_create_reference_code(self):
        """Test that reference code is generated correctly"""
        self.assertTrue(self.record.reference_code.startswith('TEST-'))

    def test_unique_reference_code(self):
        """Ensure that newly created records have unique reference codes"""
        new_record = self.TestModel.create({'name': 'Test Record 2'})
        self.assertNotEqual(self.record.reference_code, new_record.reference_code)

    def test_reference_code_format(self):
        """Ensure reference code follows the correct format"""
        self.assertRegex(self.record.reference_code, r'^TEST-\d{4}$')

    def test_confirm_action(self):
        """Test confirming an applicant"""
        self.record.action_confirm()
        self.assertEqual(self.record.state, 'confirmed')

    def test_auto_mark_done(self):
        """Test cron job marks records as done after 30 minutes"""
        self.record.write({'state': 'confirmed', 'confirmed_at': '2025-02-23 10:00:00'})
        self.TestModel._auto_mark_done()
        self.record.invalidate_recordset()
        self.assertEqual(self.record.state, 'done')

    def test_auto_mark_done_no_change(self):
        """Ensure records confirmed recently do not change"""
        self.record.write({'state': 'confirmed', 'confirmed_at': fields.Datetime.now()})
        self.TestModel._auto_mark_done()
        self.record.invalidate_recordset()
        self.assertEqual(self.record.state, 'confirmed')

    def test_reset_reference_code(self):
        """Test if reference codes are reset properly without duplication"""
        self.TestModel._reset_reference_code()

        # Fetch all reference codes
        codes = self.TestModel.search([]).mapped('reference_code')

        # Ensure uniqueness
        self.assertEqual(len(codes), len(set(codes)))

    def test_create_test_model_api(self):
        """Test API creating a new test.model"""
        response = self.env['test.model'].sudo().create({'name': 'API Record'})
        self.assertTrue(response.id)
        self.assertTrue(response.reference_code.startswith('TEST-'))
