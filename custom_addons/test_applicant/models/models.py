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
        """ Override create method to generate reference_code """
        vals['reference_code'] = self.env['ir.sequence'].next_by_code('test.model.reference_code')
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
        """ Resets the reference_code sequence daily and updates all records """
        sequence = self.env['ir.sequence'].search([('code', '=', 'test.model.reference_code')])
        if sequence:
            sequence.sudo().write({'number_next': 1})  # Reset sequence to start from 1

        for index, record in enumerate(self.search([]), start=1):
            new_code = f"TEST-{str(index).zfill(4)}"
            record.sudo().write({'reference_code': new_code})