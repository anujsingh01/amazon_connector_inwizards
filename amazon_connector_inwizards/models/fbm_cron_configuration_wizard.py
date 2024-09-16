from odoo import models, fields
# from odoo.addons.amazon_connector_inwizards.models.operation_fba_dbm import OperationFbaFbm
# from .operation_fba_dbm import OperationsFBAFBM
from datetime import datetime, timezone

class FBMCronConfigurationWizard(models.TransientModel):
    _name = 'fbm.cron.configuration.wizard'
    _description = 'FBM Cron Configuration Wizard'

    amz_seller_id = fields.Many2one('amazon.seller.ept', string='Amazon Seller')
    amz_order_auto_import = fields.Boolean(string='Auto Import Orders')
    amz_order_import_interval_number = fields.Integer(string='Import Interval Number')
    amz_order_import_interval_type = fields.Selection([
        # ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        # ('weeks','Weeks'),
    ], string='Import Interval Type')
    
    amz_order_import_next_execution = fields.Datetime(string='Next Execution')
    amz_order_import_user_id = fields.Many2one('res.users', string='User')

    amz_stock_auto_export = fields.Boolean(string='Auto Export Stock')
    amz_inventory_export_interval_number = fields.Integer(string='Export Interval Number')
    amz_inventory_export_interval_type = fields.Selection([
        # ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        # ('weeks','Weeks'),
    ], string='Export Interval Type')
    
    amz_inventory_export_next_execution = fields.Datetime(string='Next Execution')
    amz_inventory_export_user_id = fields.Many2one('res.users', string='User')

    amz_order_auto_update = fields.Boolean(string='Auto Update Orders')
    amz_order_update_interval_number = fields.Integer(string='Update Interval Number')
    amz_order_update_interval_type = fields.Selection([
        # ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        # ('weeks','Weeks'),
    ], string='Update Interval Type')
    
    amz_order_update_next_execution = fields.Datetime(string='Next Execution')
    amz_order_update_user_id = fields.Many2one('res.users', string='User')

    amz_auto_check_cancel_order = fields.Boolean(string='Auto Check Cancel Orders')
    amz_cancel_order_interval_number = fields.Integer(string='Cancel Interval Number')
    amz_cancel_order_interval_type = fields.Selection([
        # ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        # ('weeks','Weeks'),
    ], string='Cancel Interval Type')
    
    amz_cancel_order_next_execution = fields.Datetime(string='Next Execution')
    amz_cancel_order_report_user_id = fields.Many2one('res.users', string='User')

    amz_auto_import_shipped_orders = fields.Boolean(string='Auto Import Shipped Orders')
    auto_import_fbm_shipped_interval_number = fields.Integer(string='Import Shipped Interval Number')
    auto_import_fbm_shipped_interval_type = fields.Selection([
        # ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        # ('weeks','Weeks'),
    ], string='Import Shipped Interval Type')
    
    auto_import_fbm_shipped_next_execution = fields.Datetime(string='Next Execution')
    auto_import_fbm_shipped_user_id = fields.Many2one('res.users', string='User')





    # Define similar fields for all other operations...

    def save_cron_configuration(self):

        # Handle FBM Auto Import Orders
        if self.amz_order_auto_import:
            self._create_or_update_cron_job(
                'FBM Auto Import Orders of', 
                'fbm_cron_auto_import_orders', 
                self.amz_order_import_interval_number, 
                self.amz_order_import_interval_type, 
                self.amz_order_import_next_execution, 
                self.amz_order_import_user_id,
                priority=51
            )
        else:
            self._delete_cron_job('FBM Auto Import Orders of')

        # Handle FBM Auto Export Stock
        if self.amz_stock_auto_export:
            self._create_or_update_cron_job(
                'FBM Auto Export Stock of', 
                'fbm_cron_auto_export_stock', 
                self.amz_inventory_export_interval_number, 
                self.amz_inventory_export_interval_type, 
                self.amz_inventory_export_next_execution, 
                self.amz_inventory_export_user_id,
                priority=52
            )
        else:
            self._delete_cron_job('FBM Auto Export Stock of')

        # Handle FBM Update Order Status
        if self.amz_order_auto_update:
            self._create_or_update_cron_job(
                'FBM Update Order Status of', 
                'fbm_cron_update_order_status', 
                self.amz_order_update_interval_number, 
                self.amz_order_update_interval_type, 
                self.amz_order_update_next_execution, 
                self.amz_order_update_user_id,
                priority=53
            )
        else:
            self._delete_cron_job('FBM Update Order Status of')    

        # Handle FBM Check Canceled Orders
        if self.amz_auto_check_cancel_order:
            self._create_or_update_cron_job(
                'FBM Check Canceled Orders of', 
                'fbm_cron_check_canceled_orders', 
                self.amz_cancel_order_interval_number, 
                self.amz_cancel_order_interval_type, 
                self.amz_cancel_order_next_execution, 
                self.amz_cancel_order_report_user_id,
                priority=54
            )
        else:
            self._delete_cron_job('FBM Check Canceled Orders of')    

        # Handle FBM Auto Import Shipped Orders
        if self.amz_auto_import_shipped_orders:
            self._create_or_update_cron_job(
                'FBM Auto Import Shipped Orders of', 
                'fbm_cron_auto_import_shipped_orders', 
                self.auto_import_fbm_shipped_interval_number, 
                self.auto_import_fbm_shipped_interval_type, 
                self.auto_import_fbm_shipped_next_execution, 
                self.auto_import_fbm_shipped_user_id,
                priority=55
            )
        else:
            self._delete_cron_job('FBM Auto Import Shipped Orders of')    



    def _delete_cron_job(self, name):
        full_name = f"{name} {self.amz_seller_id.name}"
        cron = self.env['ir.cron'].search([('name', '=', full_name)], limit=1)
        if cron:
            cron.unlink()




    def _create_or_update_cron_job(self, name, method_name, interval_number, interval_type, nextcall, user_id,priority):
        full_name = f"{name} {self.amz_seller_id.name}"
        cron_obj = self.env['ir.cron']
        cron = cron_obj.search([('name', '=', full_name)], limit=1)
        values = {
            'name': full_name,
            'model_id': self.env['ir.model']._get('fbm.cron.configuration.wizard').id,
            'state': 'code',
            'code': f'model.{method_name}()',  # Use the method_name dynamically
            'user_id': user_id.id,
            'interval_number': interval_number,
            'interval_type': interval_type,
            'nextcall': nextcall,
            'active': True,
            'numbercall':-1,
            'amz_seller_id': self.amz_seller_id.id,
            'priority':priority, 
         
        }

        print("cron ----",cron)
        print("values ----",values)

        if cron:
            cron.unlink()
        cron_obj.create(values)




    def fbm_cron_auto_import_orders(self):
        
        now = datetime.utcnow()
        model_id = self.env['ir.model'].search([('model', '=', 'fbm.cron.configuration.wizard')], limit=1).id
        
        seller_data = self.env['ir.cron'].search([
            ('model_id', '=', model_id),
            ('code', 'like', 'model.fbm_cron_auto_import_orders()'),
            ('nextcall', '<=', now)
        ], order='lastcall desc', limit=1)


        
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        if not seller_data :
            return("Method Not Found")
        
        seller_id = seller_data.amz_seller_id.merchant_id
        seller = seller_data.amz_seller_id
        seller_marketplace_data = self.env['amazon.instance.ept'].search([('merchant_id', '=', seller_id)])


        operation_fba_fbm_model = self.env['amazon.process.import.export']  
            
            
        operation_fba_fbm_model.amz_import_fbm_missing_unshipped_orders(today, seller,seller_marketplace_data)





    def fbm_cron_auto_export_stock(self):
        now = datetime.utcnow()        
        model_id = self.env['ir.model'].search([('model', '=', 'fbm.cron.configuration.wizard')], limit=1).id
        seller_data = self.env['ir.cron'].search([
            ('model_id', '=', model_id),
            ('code', 'like', 'model.fbm_cron_auto_export_stock()'),
            ('nextcall', '<=', now)
        ], order='lastcall desc', limit=1)
        
        seller_id = seller_data.amz_seller_id.merchant_id
       
        seller = seller_data.amz_seller_id
        
        seller_marketplace_data = self.env['amazon.instance.ept'].search([('merchant_id', '=', seller_id)])
        operation_fba_fbm_model = self.env['amazon.process.import.export']  
        operation_fba_fbm_model.amz_fbm_export_stock_from_odoo_to_amazon(seller,seller_id,seller_marketplace_data)
        
        

    def fbm_cron_update_order_status(self):
        pass

    def fbm_cron_check_canceled_orders(self):
        pass

    def fbm_cron_auto_import_shipped_orders(self):
        now = datetime.utcnow()
        model_id = self.env['ir.model'].search([('model', '=', 'fbm.cron.configuration.wizard')], limit=1).id
        
        seller_data = self.env['ir.cron'].search([
            ('model_id', '=', model_id),
            ('code', 'like', 'model.fbm_cron_auto_import_shipped_orders()'),
            ('nextcall', '<=', now)
        ], order='lastcall desc', limit=1)


        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        if not seller_data :
            return("Method Not Found")
        
        seller_id = seller_data.amz_seller_id.merchant_id
        seller = seller_data.amz_seller_id
        seller_marketplace_data = self.env['amazon.instance.ept'].search([('merchant_id', '=', seller_id)])
        operation_fba_fbm_model = self.env['amazon.process.import.export']  
        
        
        operation_fba_fbm_model.amz_import_fbm_shipped_orders(today, seller,seller_marketplace_data)


class IrCron(models.Model):
    _inherit = 'ir.cron'

    amz_seller_id = fields.Many2one('amazon.seller.ept', string='Amazon Seller')