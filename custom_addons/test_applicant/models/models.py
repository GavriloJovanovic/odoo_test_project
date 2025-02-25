# custom_addons/test_applicant/models/models.py
from datetime import datetime, timedelta

from odoo import models, fields, api


class TestModel(models.Model):
    _name = 'test.model'
    _description = 'Test Model'
    _sql_constraints = [
        ('unique_reference_code', 'UNIQUE(reference_code)', 'Reference Code must be unique!')
    ]

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    reference_code = fields.Char(string='Reference Code', readonly=True, unique=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='State', default='draft')
    confirmed_at = fields.Datetime(string="Confirmed At")

    @api.model
    def create(self, vals):
        """ Generate a unique reference_code based on the highest existing one. """
        last_record = self.search([], order='reference_code desc', limit=1)

        if last_record and last_record.reference_code:
            last_number = int(last_record.reference_code.split('-')[-1])  # Extract last number
        else:
            last_number = 0

        new_reference_code = f"TEST-{str(last_number + 1).zfill(4)}"
        vals['reference_code'] = new_reference_code

        return super(TestModel, self).create(vals)

    def action_confirm(self):
        """ Changes the state to confirmed """
        self.write({'state': 'confirmed','confirmed_at': fields.Datetime.now()})

    @api.model
    def _auto_mark_done(self):
        """Cron job to mark records as 'done' if they've been in 'confirmed' for more than 30 minutes."""
        threshold_time = datetime.now() - timedelta(minutes=30)
        records = self.search([('state', '=', 'confirmed'), ('confirmed_at', '<=', threshold_time)])
        records.write({'state': 'done'})

    @api.model
    def _reset_reference_code(self):
        """ Reset reference_code sequence daily while maintaining uniqueness. """
        sequence = self.env['ir.sequence'].search([('code', '=', 'test.model.reference_code')], limit=1)
        if sequence:
            sequence.sudo().write({'number_next': 1})  # Reset sequence

        # Get all records sorted by ID and reassign unique reference codes
        records = self.search([], order="id asc")

        for index, record in enumerate(records, start=1):
            new_code = f"TEST-{str(index).zfill(4)}"

            # Ensure uniqueness
            if self.search([('reference_code', '=', new_code)], limit=1):
                continue  # Skip if the reference code already exists

            record.sudo().write({'reference_code': new_code})

