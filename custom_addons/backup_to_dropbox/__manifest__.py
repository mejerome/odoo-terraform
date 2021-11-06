# -*- coding: utf-8 -*-
{
    'name': "Database auto-backup to DropBox",

    'summary': 'Automated backups to DropBox',

    'description': """
        The Database Auto-Backup module enables the user to make configurations for the automatic backup of the database along with DropBox
    """,

    'author': "Fasil",
    'website': "https://github.com/fasilwdr",
    'category': 'Administration',
    'version': '13.0',
    'installable': True,
    'application': True,
    'license': 'LGPL-3',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/backup_view.xml',
        'data/backup_data.xml',
    ],
    'images': ['static/description/banner.png'],
}
