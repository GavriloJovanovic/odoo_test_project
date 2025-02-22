# -*- coding: utf-8 -*-
# from odoo import http


# class ../customAddons/testApplicant(http.Controller):
#     @http.route('/../custom_addons/test_applicant/../custom_addons/test_applicant', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/../custom_addons/test_applicant/../custom_addons/test_applicant/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('../custom_addons/test_applicant.listing', {
#             'root': '/../custom_addons/test_applicant/../custom_addons/test_applicant',
#             'objects': http.request.env['../custom_addons/test_applicant.../custom_addons/test_applicant'].search([]),
#         })

#     @http.route('/../custom_addons/test_applicant/../custom_addons/test_applicant/objects/<model("../custom_addons/test_applicant.../custom_addons/test_applicant"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('../custom_addons/test_applicant.object', {
#             'object': obj
#         })
