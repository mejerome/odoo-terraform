# -*- coding: utf-8 -*-

import os
import datetime
import time
import shutil
import json
import tempfile
import dropbox

from odoo import models, fields, api, tools, _
import odoo


import logging
_logger = logging.getLogger(__name__)

try:
    import dropbox
except ImportError:
    raise ImportError(
        'This module needs dropbox !'
        'Please install dropbox on your system. (sudo pip install dropbox)')


class DbBackup(models.Model):
    _name = 'db.backup'
    _description = 'Backup configuration record'

    def _get_db_name(self):
        dbName = self._cr.dbname
        return dbName

    # Columns for local server configuration
    access_token = fields.Char('Access Token')
    upload_dropbox = fields.Boolean('Upload to DropBox')
    host = fields.Char('Host', required=True, default='localhost')
    port = fields.Char('Port', required=True, default=8069)
    name = fields.Char('Database', required=True, help='Database you want to schedule backups for',
                       default=_get_db_name)
    folder = fields.Char('Backup Directory', help='Absolute path for storing the backups', required='True',
                         default='/odoo/backups')
    dropbox_folder = fields.Char('Backup Directory', help='Absolute path for storing the backups', default='/odoo_backups')
    email_notification = fields.Boolean('Email Notification')
    email = fields.Char('Email')
    backup_type = fields.Selection([('zip', 'Zip'), ('dump', 'Dump')], 'Backup Type', required=True, default='zip')
    autoremove = fields.Boolean('Remove Backups',
                                help='If you check this option you can choose to automaticly remove the backup '
                                     'after xx days')
    days_to_keep = fields.Integer('Remove after n days',
                                  help="Choose after how many days the backup should be deleted. For example:\n"
                                       "If you fill in 5 the backups will be removed after 5 days.",
                                  required=True,  default=5)

    def _access_dbx(self, access_token):
        dbx = None
        try:
            dbx = dropbox.Dropbox(access_token)
        except Exception as e:
            print(e)
        return dbx

    def schedule_backup(self):
        conf_ids = self.search([])
        if conf_ids:
            for rec in conf_ids:
                backup_status = {
                    'local_backup': True,
                    'local_backup_error': '',
                    'dbx_backup': True,
                    'dbx_backup_error': '',
                }
                try:
                    if not os.path.isdir(rec.folder):
                        os.makedirs(rec.folder)
                except:
                    raise
                # Create name for dumpfile.
                bkp_file = '%s_%s.%s' % (time.strftime('%Y_%m_%d_%H_%M_%S'), rec.name, rec.backup_type)
                file_path = os.path.join(rec.folder, bkp_file)
                fp = open(file_path, 'wb')
                try:
                    # try to backup database and write it away
                    fp = open(file_path, 'wb')
                    backup_status['local_backup'], backup_status['local_backup_error'] = self._take_dump(rec.name, fp, 'db.backup', rec.backup_type)
                    if rec.upload_dropbox and backup_status['local_backup']:
                        backup_status['dbx_backup'], backup_status['dbx_backup_error'] = self.upload_file(rec.access_token, file_path, f'{rec.dropbox_folder}/{bkp_file}')
                    fp.close()
                except Exception as error:
                    backup_status['local_backup'] = False
                    backup_status['local_backup_error'] = error
                    _logger.debug(
                        "Couldn't backup database %s. Bad database administrator password for server running at "
                        "http://%s:%s" % (rec.name, rec.host, rec.port))
                    _logger.debug("Exact error from the exception: " + str(error))
                    continue
                """
                            Remove all old files (on local server) in case this is configured..
                            """
                if rec.autoremove:
                    directory = rec.folder
                    # Loop over all files in the directory.
                    for f in os.listdir(directory):
                        fullpath = os.path.join(directory, f)
                        # Only delete the ones which are from the current database
                        # (Makes it possible to save different databases in the same folder)
                        if rec.name in fullpath:
                            timestamp = os.stat(fullpath).st_ctime
                            createtime = datetime.datetime.fromtimestamp(timestamp)
                            now = datetime.datetime.now()
                            delta = now - createtime
                            if delta.days >= rec.days_to_keep:
                                # Only delete files (which are .dump and .zip), no directories.
                                if os.path.isfile(fullpath) and (".dump" in f or '.zip' in f):
                                    _logger.info("Delete local out-of-date file: " + fullpath)
                                    os.remove(fullpath)
                    self._remove_from_dropbox(rec.access_token, rec.days_to_keep, rec.dropbox_folder)
                if rec.email_notification:
                    if not backup_status['dbx_backup'] and backup_status['local_backup']:
                        backup_error = f"Error : {backup_status['dbx_backup_error']}"
                        self._send_mail_notification(failed='DropBox', error=backup_error, email=rec.email)
                    elif not backup_status['local_backup']:
                        backup_error = f"<p>Error local backup : {backup_status['local_backup_error']}</p><p>Error for DropBox backup : {backup_status['local_backup_error']}</p>"
                        self._send_mail_notification(failed='Both Local and DropBox', error=backup_error, email=rec.email)
                    else:
                        pass

    def _send_mail_notification(self, failed, error, email):
        body = f"<div style='font-size: 12px;font-weight: bold;color:red;'>Hello,<p>{failed} Backup failed.</p>{error}</div>"
        self.env['mail.mail'].create({
            'body_html': body,
            'subject': f'{failed} Backup Failed',
            'email_to': email,
        }).send()

    def _remove_from_dropbox(self, access_token, days_to_keep, dropbox_folder):
        try:
            dbx = self._access_dbx(access_token)
            files = dbx.files_list_folder(dropbox_folder).entries
            for file in files:
                try:
                    modify_date = file.client_modified
                except Exception:
                    modify_date = False
                    pass
                if modify_date and days_to_keep > 0:
                    today = datetime.datetime.today()
                    delta = today - file.client_modified
                    if delta.days >= days_to_keep:
                        dbx.files_delete(file.path_display)
                        print("Deleted from DropBox", file.path_display)
        except Exception as e:
            print(e)
            pass

    def _take_dump(self, db_name, stream, model, backup_format='zip'):
        """Dump database `db` into file-like object `stream` if stream is None
        return a file object with the dump """

        _logger.info('DUMP DB: %s format %s', db_name, backup_format)
        try:
            cmd = ['pg_dump', '--no-owner']
            cmd.append(db_name)

            if backup_format == 'zip':
                with odoo.tools.osutil.tempdir() as dump_dir:
                    filestore = odoo.tools.config.filestore(db_name)
                    if os.path.exists(filestore):
                        shutil.copytree(filestore, os.path.join(dump_dir, 'filestore'))
                    with open(os.path.join(dump_dir, 'manifest.json'), 'w') as fh:
                        db = odoo.sql_db.db_connect(db_name)
                        with db.cursor() as cr:
                            json.dump(self._dump_db_manifest(cr), fh, indent=4)
                    cmd.insert(-1, '--file=' + os.path.join(dump_dir, 'dump.sql'))
                    odoo.tools.exec_pg_command(*cmd)
                    if stream:
                        odoo.tools.osutil.zip_dir(dump_dir, stream, include_dir=False, fnct_sort=lambda file_name: file_name != 'dump.sql')
                    else:
                        t=tempfile.TemporaryFile()
                        odoo.tools.osutil.zip_dir(dump_dir, t, include_dir=False, fnct_sort=lambda file_name: file_name != 'dump.sql')
                        t.seek(0)
            else:
                cmd.insert(-1, '--format=c')
                stdin, stdout = odoo.tools.exec_pg_command_pipe(*cmd)
                if stream:
                    shutil.copyfileobj(stdout, stream)
            return True, ''
        except Exception as e:
            os.remove(stream.name)
            print(e)
            return False, e

    def _dump_db_manifest(self, cr):
        pg_version = "%d.%d" % divmod(cr._obj.connection.server_version / 100, 100)
        cr.execute("SELECT name, latest_version FROM ir_module_module WHERE state = 'installed'")
        modules = dict(cr.fetchall())
        manifest = {
            'odoo_dump': '1',
            'db_name': cr.dbname,
            'version': odoo.release.version,
            'version_info': odoo.release.version_info,
            'major_version': odoo.release.major_version,
            'pg_version': pg_version,
            'modules': modules,
        }
        return manifest

    def upload_file(self, access_token, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        try:
            dbx = self._access_dbx(access_token)
            with open(file_from, 'rb') as f:
                dbx.files_upload(f.read(), file_to)
            status = True
            error = ''
        except Exception as e:
            status = False
            error = e
        return status, error