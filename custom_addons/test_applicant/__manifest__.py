{
    'name': 'Test Applicant',
    'version': '1.0',
    'summary': 'Test module for managing applicants',
    'category': 'Custom',
    'author': 'Gavrilo Jovanovic',
    'license': 'LGPL-3',
    'depends': ['base'],
    'test_enable': True,
    'data': [
        'security/security.xml',
        'views/test_model_menu.xml',
        'views/test_model_views.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/cron.xml',
    ],
    'installable': True,
    'application': True,
}
