# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.exceptions import UserError

import json
import base64
import types
from urllib.parse import urlparse, parse_qs


class ReportExportWizard(models.TransientModel):
    """ Wizard allowing to export an accounting report in several different formats
    at once, saving them as attachments.
    """
    _name = 'account_reports.export.wizard'
    _description = "Export wizard for accounting's reports"

    export_format_ids = fields.Many2many(string="Export to", comodel_name='account_reports.export.wizard.format', relation="dms_acc_rep_export_wizard_format_rel")
    report_model = fields.Char(string="Report Model", required=True)
    report_id = fields.Integer(string="Parent Report Id", required=True)
    doc_name = fields.Char(string="Documents Name", help="Name to give to the generated documents.")

    @api.model
    def create(self, vals):
        rslt = super(ReportExportWizard, self).create(vals)

        report = rslt._get_report_obj()
        rslt.doc_name = hasattr(report, 'name') and report.name or report._description # account.financial.html.report objects have a name field, not account.report ones

        # We create one export format object per available export type of the report,
        # with the right generation function associated to it.
        # This is done so to allow selecting them as Many2many tags in the wizard.
        for button_dict in report._get_reports_buttons_in_sequence(self._context.get('account_report_generation_options', {})):
            if button_dict.get('file_export_type'):
                self.env['account_reports.export.wizard.format'].create({
                    'name': button_dict['file_export_type'],
                    'fun_to_call': button_dict['action'],
                    'export_wizard_id': rslt.id,
                })

        return rslt

    def export_report(self):
        self.ensure_one()
        created_attachments = self.env['ir.attachment']
        for vals in self._get_attachments_to_save():
            created_attachments |= self.env['ir.attachment'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Generated Documents'),
            'view_mode': 'kanban,form',
            'res_model': 'ir.attachment',
            'domain': [('id', 'in', created_attachments.ids)],
        }

    def _get_attachments_to_save(self):
        self.ensure_one()
        to_create_attachments = []
        for format in self.export_format_ids:
            report_options = self.env.context['account_report_generation_options']
            report_action = format.apply_export(report_options)
            report = self._get_report_obj()
            if report_action['type'] == 'ir_actions_account_report_download':
                output_format = report_action['data']['output_format']
                mimetype = report.get_export_mime_type(output_format)

                if mimetype is not False: # We let the option to set a None value for it
                    report_options = json.loads(report_action['data']['options'])
                    report_options = self._get_log_options_dict(report_options)
                    generation_function = getattr(report, 'get_' + output_format)
                    file_name = f"{self.doc_name or report.get_report_filename(report_options)}.{output_format}"
                    # We use the options from the action, as the action may have added or modified
                    # stuff into them (see l10n_es_reports, with BOE wizard)
                    generated_content = generation_function(report_options)
                    # We need to unpack the content in case of a generator
                    if isinstance(generated_content, types.GeneratorType):
                        generated_content = b''.join(c.encode() for c in generated_content)
                    file_content = base64.encodebytes(generated_content) if isinstance(generated_content, bytes) else generated_content
            elif report_action['type'] == 'ir.actions.act_url':
                query_params = parse_qs(urlparse(report_action['url']).query)
                model = query_params['model'][0]
                model_id = int(query_params['id'][0])
                wizard = self.env[model].browse(model_id)
                file_name = wizard[query_params['filename_field'][0]]
                file_content = wizard[query_params['field'][0]]
                mimetype = self.env['account.report'].get_export_mime_type(file_name.split('.')[-1])
            else:
                raise UserError(_("One of the formats chosen can not be exported in the DMS"))
            report_options.pop('self', False)
            to_create_attachments.append(self.get_attachment_vals(file_name, file_content, mimetype, report_options))
        return to_create_attachments

    def get_attachment_vals(self, file_name, file_content, mimetype, log_options_dict):
        self.ensure_one()
        return {
            'name': file_name,
            'company_id': self.env.company.id,
            'datas': file_content,
            'mimetype': mimetype,
            'description': json.dumps(log_options_dict)
        }

    def _get_report_obj(self):
        model = self.env[self.report_model]
        if self.report_id:
            return model.browse(self.report_id)
        return model

    def _get_log_options_dict(self, report_options):
        """ To be overridden in order to replace wizard ids by json data for the
        correponding object.
        """
        return report_options


class ReportExortWizardOption(models.TransientModel):
    _name = 'account_reports.export.wizard.format'
    _description = "Export format for accounting's reports"

    name = fields.Char(string="Name", required=True)
    fun_to_call = fields.Char(string="Function to Call", required=True)
    export_wizard_id = fields.Many2one(string="Parent Wizard", comodel_name='account_reports.export.wizard', required=True, ondelete='cascade')

    def apply_export(self, report_options):
        report = self.env[self.export_wizard_id.report_model].browse(self.export_wizard_id.report_id)
        models.check_method_name(self.fun_to_call)
        return getattr(report, self.fun_to_call)(report_options)
