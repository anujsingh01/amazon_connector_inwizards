from odoo import models, fields
from datetime import datetime, timezone , timedelta


# class GlobalCronJob(models.TransientModel):
#     _name = 'global.cron.job.wizard'
#     _description = 'Global Cron Configuration Wizard'

class GlobalCronJobWizard(models.TransientModel):
    _name = 'global.cron.job.wizard'
    _description = 'Global Cron Job Wizard'


    amazon_selling = fields.Selection([
        ('FBA', 'FBA'),
        ('FBM', 'FBM'),
        ('Both', 'FBA & FBM'),
    ], string='Amazon Selling', required=True)
    
    amz_auto_import_rating_report = fields.Boolean(string='Auto Request Rating Report?')
    
    amz_auto_import_vcs_tax_report = fields.Boolean(string='Auto Request VCS Tax Report?')
    
    amz_auto_process_rating_report = fields.Boolean(string='Download and Process Rating?')
    
    amz_auto_process_vcs_tax_report = fields.Boolean(string='Download and Process VCS Tax Report?')
    
    amz_auto_upload_tax_invoices = fields.Boolean(string='Auto Upload invoices from Odoo to Amazon?')
    
    amz_auto_upload_tax_invoices_interval_number = fields.Integer(string='Upload Invoices Interval Number')
    
    amz_auto_upload_tax_invoices_interval_type = fields.Selection([
        ('hours', 'Hours'),
        ('days', 'Days'),

    ], string='Upload Invoices Time Interval Unit')
    
    amz_auto_upload_tax_invoices_next_execution = fields.Datetime(string='Upload Invoices Next Execution')
    
    amz_auto_upload_tax_invoices_user_id = fields.Many2one('res.users', string='Amazon Invoices Upload User')
    
    amz_rating_process_report_interval_number = fields.Integer(string='Process Rating Interval Number')
    
    amz_rating_process_report_interval_type = fields.Selection([
        ('hours', 'Hours'),
        ('days', 'Days'),
 
    ], string='Process Rating Interval Unit')
    
    amz_rating_process_report_next_execution = fields.Datetime(string='Process Rating Next Execution')
    
    amz_rating_process_report_user_id = fields.Many2one('res.users', string='Process Rating User')
    
    amz_rating_report_import_interval_number = fields.Integer(string='Import Rating Report Interval Number')
    
    amz_rating_report_import_interval_type = fields.Selection([
        ('hours', 'Hours'),
        ('days', 'Days'),

    ], string='Import Rating Report Interval Unit')
    
    amz_rating_report_import_next_execution = fields.Datetime(string='Import Rating Report Next Execution')
    
    amz_rating_report_import_user_id = fields.Many2one('res.users', string='Import Rating Report User')
    
    amz_seller_id = fields.Many2one('amazon.seller.ept', string='Amazon Seller')
    
    amz_settlement_report_auto_create = fields.Boolean(string='Auto Request Settlement Report?')
    
    amz_settlement_report_create_interval_number = fields.Integer(string='Settlement Report Create Interval Number')
    
    amz_settlement_report_create_interval_type = fields.Selection([
        ('hours', 'Hours'),
        ('days', 'Days'),

    ], string='Settlement Report Create Interval Unit')
    
    amz_settlement_report_create_next_execution = fields.Datetime(string='Settlement Report Create Next Execution')
    
    amz_settlement_report_create_user_id = fields.Many2one('res.users', string='Settlement Report Create User')
    
    amz_vcs_report_import_interval_number = fields.Integer(string='Import VCS Tax Report Interval Number')
    
    amz_vcs_report_import_interval_type = fields.Selection([
        ('hours', 'Hours'),
        ('days', 'Days'),

    ], string='Import VCS Tax Report Interval Unit')
    
    amz_vcs_report_import_next_execution = fields.Datetime(string='Import VCS Tax Report Next Execution')
    
    amz_vcs_report_import_user_id = fields.Many2one('res.users', string='Import VCS Tax Report User')
    
    amz_vcs_report_process_interval_number = fields.Integer(string='Process VCS Tax Report Interval Number')
    
    amz_vcs_report_process_interval_type = fields.Selection([
        ('hours', 'Hours'),
        ('days', 'Days'),

    ], string='Process VCS Tax Report Interval Unit')
    
    amz_vcs_report_process_next_execution = fields.Datetime(string='Process VCS Tax Report Next Execution')
    
    amz_vcs_report_process_user_id = fields.Many2one('res.users', string='Process VCS Tax Report User')
    
    create_date = fields.Datetime(string='Created on', readonly=True)
    
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    
    display_name = fields.Char(string='Display Name', readonly=True)
    
    # id = fields.Integer(string='ID', readonly=True)
    
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    
    
    def save_cron_configuration(self):
        # pass
        if self.amz_settlement_report_auto_create:
            self._create_or_update_cron(
                'Both Amazon Settlement Report Auto-Create',
                'global_cron_amz_settlement_report',
                self.amz_settlement_report_create_interval_number,
                self.amz_settlement_report_create_interval_type,
                self.amz_settlement_report_create_next_execution,
                self.amz_settlement_report_create_user_id,
                priority=71
            )
        else:
            self._delete_cron_job('Both Amazon Settlement Report Auto-Create of')    

        if self.amz_auto_import_rating_report:
            self._create_or_update_cron(
                'Both Amazon Rating Report Auto-Import',
                'global_cron_amz_amz_auto_import_rating_report',
                self.amz_rating_report_import_interval_number,
                self.amz_rating_report_import_interval_type,
                self.amz_rating_report_import_next_execution,
                self.amz_rating_report_import_user_id,
                priority=72
            )
        else:
            self._delete_cron_job('Both Amazon Rating Report Auto-Import of')        


        if self.amz_auto_import_vcs_tax_report:
            self._create_or_update_cron(
                'Both Amazon VCS Tax Report Auto-Import',
                'global_cron_amz_auto_import_vcs_report',
                self.amz_vcs_report_import_interval_number,
                self.amz_vcs_report_import_interval_type,
                self.amz_vcs_report_import_next_execution,
                self.amz_vcs_report_import_user_id,
                priority=73
            )
        else:
            self._delete_cron_job('Both Amazon VCS Tax Report Auto-Import of')  
            

        if self.amz_auto_upload_tax_invoices:
            self._create_or_update_cron(
                'Both Amazon Auto Upload Tax Invoices',
                'global_cron_amz_auto_upload_tax_invoices',
                self.amz_auto_upload_tax_invoices_interval_number,
                self.amz_auto_upload_tax_invoices_interval_type,
                self.amz_auto_upload_tax_invoices_next_execution,
                self.amz_auto_upload_tax_invoices_user_id,
                priority=74
            )
        else:
            self._delete_cron_job('Both Amazon Auto Upload Tax Invoices of')  


    


    def _create_or_update_cron(self, name, method_name, interval_number, interval_type, nextcall, user_id, priority):
        full_name = f"{name} {self.amz_seller_id.name}"
        cron_obj = self.env['ir.cron']
        cron = cron_obj.search([('name', '=', full_name)], limit=1)
        values = {
            'name': full_name,
            'model_id': self.env['ir.model']._get('global.cron.job.wizard').id,
            'state': 'code',
            'code': f'model.{method_name}()',  # Use the method_name dynamically
            'user_id': user_id.id,
            'interval_number': interval_number,
            'interval_type': interval_type,
            'nextcall': nextcall,
            'active': True,
            'numbercall': -1,
            'amz_seller_id': self.amz_seller_id.id,
            'priority': priority, 
        }

        if cron:
            cron.unlink()
        cron_obj.create(values)


    def _delete_cron_job(self, name):
        full_name = f"{name} {self.amz_seller_id.name}"
        cron = self.env['ir.cron'].search([('name', '=', full_name)], limit=1)
        if cron:
            cron.unlink()




    def global_cron_amz_settlement_report(self):
        import pdb;pdb.set_trace()
        now = datetime.utcnow()
        model_id = self.env['ir.model'].search([('model', '=', 'global.cron.job.wizard')], limit=1).id
        
        seller_data = self.env['ir.cron'].search([
            ('model_id', '=', model_id),
            ('code', 'like', 'model.global_cron_amz_settlement_report()'),
            ('nextcall', '<=', now)
        ], order='lastcall desc', limit=1)


        interval_type = seller_data.interval_type

        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        if interval_type == 'hours':
            report_start_time = now + timedelta(hours=1)
        elif interval_type == 'days':
            report_start_time = today + timedelta(days=1)
        else:
            report_start_time = today + timedelta(days=1)

        report_start_date = report_start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        # report_end_date = self.report_end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        report_end_date = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            
        if not seller_data :
            return("Method Not Found")
            
        # seller_id = seller_data.amz_seller_id.merchant_id
        seller_obj = seller_data.amz_seller_id
        # seller_marketplace_data = self.env['amazon.instance.ept'].search([('merchant_id', '=', seller_id)])


        operation_fba_fbm_model = self.env['amazon.process.import.export']  
            
        operation_fba_fbm_model.amz_list_settlement_report(report_start_date,report_end_date,seller_obj)
        


    def global_cron_amz_amz_auto_import_rating_report(self):
        pass
    
    def global_cron_amz_auto_import_vcs_report(self):
        pass

    def global_cron_amz_auto_upload_tax_invoices(self):
        pass
    



