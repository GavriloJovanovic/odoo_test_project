# # custom_addons/test_applicant/tests/test_applicant.py
from odoo.tests.common import TransactionCase

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

    def test_confirm_action(self):
        """Test confirming an applicant"""
        self.record.action_confirm()
        self.assertEqual(self.record.state, 'confirmed')

    def test_auto_mark_done(self):
        """Test cron job marks records as done after 30 minutes"""
        self.record.write({'state': 'confirmed', 'confirmed_at': '2025-02-23 10:00:00'})  # Simulate 30 min ago
        self.TestModel._auto_mark_done()
        self.record.invalidate_recordset()
        self.assertEqual(self.record.state, 'done')