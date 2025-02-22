{
    'name': 'Test Applicant',
    'version': '1.0',
    'summary': 'Test module for managing applicants',
    'category': 'Custom',
    'author': 'Gavrilo Jovanovic',
    'license': 'LGPL-3',  # ✅ Add license to avoid warnings
    'depends': ['base'],
    'data': [
        'security/security.xml',  # ✅ Load security AFTER views/menus
        'views/test_model_menu.xml',   # ✅ Load menu first
        'views/test_model_views.xml',  # ✅ Load views after menus
        'security/ir.model.access.csv', # ✅ Load access rules last
    ],
    'installable': True,
    'application': True,
}
