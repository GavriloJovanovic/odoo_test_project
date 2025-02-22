# custom_addons/test_applicant/models/models.py
from odoo import models, fields, api, _

class TestModel(models.Model):
    _name = 'test.model'
    _description = 'Test Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    reference_code = fields.Char(string='Reference Code', readonly=True, unique=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='State', default='draft')

    @api.model
    def create(self, vals):
        """ Override create method to generate reference_code """
        last_record = self.search([], order="id desc", limit=1)
        last_number = int(last_record.reference_code.split('-')[-1]) if last_record and last_record.reference_code else 0
        vals['reference_code'] = f'TEST-{last_number + 1:04d}'
        return super(TestModel, self).create(vals)

    def action_confirm(self):
        """ Changes the state to confirmed """
        self.write({'state': 'confirmed'})