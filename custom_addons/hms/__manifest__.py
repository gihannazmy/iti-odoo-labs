{
    "name": "Hospitals Management System",
    "summary": "Hospitals Management System",
    "description": """ """,
    "author": "Gihan Atef",
    "category": "",
    "version": "17.0.0.1.0",
    "depends": ['base','crm','mail'],
    "application": True,
    "data": [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/department_view.xml',
        'views/res_partner.xml',
        'report/patient_print.xml',
        'wizards/add_description.xml',

    ]
}