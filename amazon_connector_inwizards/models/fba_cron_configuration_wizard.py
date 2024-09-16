from odoo import models, fields, api
from datetime import datetime, timezone

class FbaCronConfigurationWizard(models.TransientModel):
    _name = 'fba.cron.configuration.wizard'
    _description = 'FBA Cron Configuration Wizard'

    # Fields
    # amz_seller_id = fields.Many2one('amazon.seller', string="Amazon Seller")
    amazon_selling = fields.Selection([('FBM', 'FBM'), ('FBA', 'FBA')], string="Amazon Selling Type")
    
    # # FBA Pending Orders
    amz_auto_import_fba_pending_order = fields.Boolean("Auto Import FBA Pending Orders")
    # amz_pending_order_import_interval_number = fields.Integer("Interval Number")
    amz_pending_order_import_interval_type = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days')
    ], "Interval Type")
    # amz_pending_order_next_execution = fields.Datetime("Next Execution")
    # amz_pending_order_import_user_id = fields.Many2one('res.users', string="Import User")

    # # FBA Shipment Report
    # amz_auto_import_shipment_report = fields.Boolean("Auto Import FBA Shipment Report")
    # amz_ship_report_import_interval_number = fields.Integer("Interval Number")
    amz_ship_report_import_interval_type = fields.Selection([
        
        ('hours', 'Hours'),
        ('days', 'Days')
    ], "Interval Type")
    # amz_ship_report_import_next_execution = fields.Datetime("Next Execution")
    # amz_ship_report_import_user_id = fields.Many2one('res.users', string="Import User")

    # # Removal Order Report
    # auto_create_removal_order_report = fields.Boolean("Auto Create Removal Order Report")
    # fba_removal_order_interval_number = fields.Integer("Interval Number")
    fba_removal_order_interval_type = fields.Selection([
        
        ('hours', 'Hours'),
        ('days', 'Days')
    ], "Interval Type")
    # fba_removal_order_next_execution = fields.Datetime("Next Execution")
    # fba_removal_order_user = fields.Many2one('res.users', string="User")

    # # Return Report
    # amz_auto_import_return_report = fields.Boolean("Auto Import Return Report")
    # amz_return_report_import_interval_number = fields.Integer("Interval Number")
    amz_return_report_import_interval_type = fields.Selection([
        
        ('hours', 'Hours'),
        ('days', 'Days')
    ], "Interval Type")
    # amz_return_report_import_next_execution = fields.Datetime("Next Execution")
    # amz_return_report_import_user_id = fields.Many2one('res.users', string="Import User")

    # # Inventory
    # amz_stock_auto_import_by_report = fields.Boolean("Auto Import Stock by Report")
    # fba_stock_report_import_interval_number = fields.Integer("Interval Number")
    # fba_stock_report_import_interval_type = fields.Selection([
    #     
    #     ('hours', 'Hours'),
    #     ('days', 'Days')
    # ], "Interval Type")
    # fba_stock_report_import_next_execution = fields.Datetime("Next Execution")
    # fba_stock_report_import_user_id = fields.Many2one('res.users', string="Import User")

    # amz_auto_import_inbound_shipment = fields.Boolean(string="Auto Import FBA Inbound Shipments")
    # amz_auto_import_inbound_shipment = fields.Boolean(string="Auto Import FBA Inbound Shipments")
    # amz_inbound_shipment_import_interval_number = fields.Integer(string="Inbound Shipment Import Interval Number")
    # amz_inbound_shipment_import_interval_type = fields.Selection([('hours', 'Hours'), ('days', 'Days')], string="Inbound Shipment Import Interval Type")
    # amz_inbound_shipment_import_next_execution = fields.Datetime(string="Next Inbound Shipment Import Execution")
    # amz_inbound_shipment_import_user_id = fields.Many2one('res.users', string="Inbound Shipment Import User")

    # amz_fba_pending_order_import_interval_number = fields.Integer(string="Import Interval Number")
    # amz_fba_pending_order_import_interval_type = fields.Selection([
    #     
    #     ('hours', 'Hours'),
    #     ('days', 'Days'),
    #     ('weeks', 'Weeks'),
    #     ('months', 'Months'),
    # ], string="Import Interval Type")
    # amz_fba_pending_order_import_next_execution = fields.Datetime(string="Next Execution Time")
    # amz_fba_pending_order_import_user_id = fields.Many2one('res.users', string="User")
    # amz_auto_export_fba_stock = fields.Boolean(string="Auto Export FBA Stock")

    # amz_fba_stock_export_interval_number = fields.Integer(string="Stock Export Interval Number")
    # amz_fba_stock_export_interval_type = fields.Selection([
    #     
    #     ('hours', 'Hours'),
    #     ('days', 'Days')],
    #     string="Stock Export Interval Type"
    # )
    # amz_fba_stock_export_next_execution = fields.Datetime(string="Next Execution Time")
    # amz_fba_stock_export_user_id = fields.Many2one('res.users', string="Responsible User")

    # amz_auto_update_fba_order_status = fields.Boolean(string="Auto Update FBA Order Status")

    # amz_fba_order_update_interval_number = fields.Integer(string="Order Update Interval Number")
    # amz_fba_order_update_interval_type = fields.Selection(
    #     [ ('hours', 'Hours'), ('days', 'Days')],
    #     string="Order Update Interval Type"
    # )
    # amz_fba_order_update_next_execution = fields.Datetime(string="Next Execution Time")
    # amz_fba_order_update_user_id = fields.Many2one('res.users', string="User Responsible")

    # amz_auto_import_fba_shipped_orders = fields.Boolean(string="Auto Import FBA Shipped Orders")

    # # Define any other necessary fields
    # amz_fba_shipped_orders_import_interval_number = fields.Integer(string="Shipped Orders Import Interval Number")
    # amz_fba_shipped_orders_import_interval_type = fields.Selection(
    #     [ ('hours', 'Hours'), ('days', 'Days')],
    #     string="Shipped Orders Import Interval Type"
    # )
    # amz_fba_shipped_orders_import_next_execution = fields.Datetime(string="Next Execution Time")
    # amz_fba_shipped_orders_import_user_id = fields.Many2one('res.users', string="User Responsible")

    #     # Add the missing fields
    # auto_import_fba_shipped_interval_number = fields.Integer(string="FBA Shipped Orders Import Interval Number")
    # auto_import_fba_shipped_interval_type = fields.Selection(
    #     [ ('hours', 'Hours'), ('days', 'Days')],
    #     string="FBA Shipped Orders Import Interval Type"
    # )
    # auto_import_fba_shipped_next_execution = fields.Datetime(string="Next Execution Time")
    # auto_import_fba_shipped_user_id = fields.Many2one('res.users', string="User Responsible")
    # amz_auto_update_inventory = fields.Boolean(string="Auto Update Inventory")


    amz_inventory_update_interval_number = fields.Integer(string="Inventory Update Interval Number")
    amz_inventory_update_user_id = fields.Many2one('res.users', string="Inventory Update User")

    amz_inventory_update_next_execution = fields.Datetime(string="Next Inventory Update")


    amz_inventory_update_interval_type = fields.Selection([
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks')
    ], string="Inventory Update Interval Type")
    
    # amazon_selling = fields.Selection(
    #     selection=[('hours', 'Hours'),
    #     ('days', 'Days'),],
    #     string='Amazon Selling',
    #     readonly=True
    # )
    # amz_auto_import_fba_pending_order = fields.Boolean(string='Auto Request FBA Pending Order ?')
    amz_auto_import_inbound_shipment_status = fields.Boolean(string='Auto Import FBA Inbound Shipment Item Status?')
    amz_auto_import_return_report = fields.Boolean(string='Auto Request FBA Customer Return Report ?')
    amz_auto_import_shipment_report = fields.Boolean(string='Auto Request FBA Shipment Report?')
    amz_inventory_import_interval_number = fields.Integer(string='Import FBA Live Stock Report Interval Number')
    amz_inventory_import_interval_type = fields.Selection(
        selection=[('hours', 'Hours'),
    ('days', 'Days'),],
        string='Import FBA Live Stock Report Interval Unit'
    )
    amz_inventory_import_next_execution = fields.Datetime(string='Import FBA Live Stock Report Next Execution')
    amz_inventory_import_user_id = fields.Many2one('res.users', string='Import FBA Live Stock Report User')
    amz_pending_order_import_interval_number = fields.Integer(string='Import FBA Pending Order Interval Number')
    # amz_pending_order_import_interval_type = fields.Selection(
    #     selection=[('hours', 'Hours'),
    #     ('days', 'Days'),],
    #     string='Import FBA Pending Order Interval Unit'
    # )
    amz_pending_order_import_user_id = fields.Many2one('res.users', string='Import FBA Pending Order User')
    amz_pending_order_next_execution = fields.Datetime(string='Import FBA Pending Order Next Execution')
    amz_return_report_import_interval_number = fields.Integer(string='Import FBA Customer Return Report Interval Number')
    # amz_return_report_import_interval_type = fields.Selection(
    #     selection=[('hours', 'Hours'),
    #     ('days', 'Days'),],
    #     string='Import FBA Customer Return Report Interval Unit'
    # )
    amz_return_report_import_next_execution = fields.Datetime(string='Import FBA Customer Return Report Next Execution')
    amz_return_report_import_user_id = fields.Many2one('res.users', string='Import FBA Customer Return Report User')
    amz_seller_id = fields.Many2one('amazon.seller.ept', string='Amazon Seller')
    amz_ship_report_import_interval_number = fields.Integer(string='Import FBA Shipment Report Interval Number')
    # amz_ship_report_import_interval_type = fields.Selection(
    #     selection=[('hours', 'Hours'),
    #     ('days', 'Days'),],
    #     string='Import FBA Shipment Report Interval Unit'
    # )
    amz_ship_report_import_next_execution = fields.Datetime(string='Import FBA Shipment Report Next Execution')
    amz_ship_report_import_user_id = fields.Many2one('res.users', string='Import FBA Shipment Report User')
    amz_shipment_status_import_interval_number = fields.Integer(string='Auto Import FBA Inbound Shipment Interval Number')
    amz_shipment_status_import_interval_type = fields.Selection(
        selection=[('hours', 'Hours'),
         ('days', 'Days'),],
        string='Auto Import FBA Inbound Shipment Status Unit'
    )
    amz_shipment_status_import_next_execution = fields.Datetime(string='Auto Import FBA Inbound Shipment Next Execution')
    amz_shipment_status_import_user_id = fields.Many2one('res.users', string='Auto Import FBA Inbound Shipment User')
    amz_stock_auto_import_by_report = fields.Boolean(string='Auto Request FBA Live Stock Report?')
    auto_create_fba_stock_adj_report = fields.Boolean(string='Auto Request FBA Stock Adjustment Report ?')
    auto_create_removal_order_report = fields.Boolean(string='Auto Request Removal Order Report ?')
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    display_name = fields.Char(string='Display Name', readonly=True)
    fba_removal_order_interval_number = fields.Integer(string='Auto Create Removal Order Report Interval Number')
    # fba_removal_order_interval_type = fields.Selection(
    #     selection=[('hours', 'Hours'),
    #     ('days', 'Days'),],
    #     string='Auto Create Removal Order Report Interval Unit'
    # )
    fba_removal_order_next_execution = fields.Datetime(string='Auto Create Removal Order Report Next Execution')
    fba_removal_order_user = fields.Many2one('res.users', string='Auto Create Removal Order Report User')
    fba_stock_adj_report_interval_number = fields.Integer(string='Auto Create Stock Adjustment Report Interval Number')
    fba_stock_adj_report_interval_type = fields.Selection(
        selection=[('hours', 'Hours'),
         ('days', 'Days'),],
        string='Auto Create Stock Adjustment Report Interval Unit'
    )
    fba_stock_adj_report_next_execution = fields.Datetime(string='Auto Create Stock Adjustment Report Next Execution')
    fba_stock_adj_report_user_id = fields.Many2one('res.users', string='Import FBA Live Stock Adjustment User')
    amz_auto_update_fba_inventory = fields.Boolean("Auto Update FBA Inventory")


    def action_save(self):
        # Save logic or processing can be implemented here
        pass
    
    def action_apply(self):
        pass
    
    def save_cron_configuration(self):
        pass

    # @api.model
    # def save_cron_configuration(self):
    #     # Add your logic for saving configuration
    #     return True





    def save_cron_configuration(self):

        # Handle FBA Auto Import Pending Orders
        if self.amz_auto_import_fba_pending_order:
            self._create_or_update_cron_job(
                'FBA Auto Import Pending Orders of', 
                'fba_cron_auto_import_pending_orders', 
                self.amz_pending_order_import_interval_number, 
                self.amz_pending_order_import_interval_type, 
                self.amz_pending_order_next_execution, 
                self.amz_pending_order_import_user_id,
                priority=61
            )
        else:
            self._delete_cron_job('FBA Auto Import Pending Orders of')
            
            
        # Handle FBA Auto Import Shipment Report
        if self.amz_auto_import_shipment_report:
            self._create_or_update_cron_job(
                'FBA Auto Import Shipment Report of', 
                'fba_cron_auto_import_shipment_report', 
                self.amz_ship_report_import_interval_number, 
                self.amz_ship_report_import_interval_type, 
                self.amz_ship_report_import_next_execution, 
                self.amz_ship_report_import_user_id,
                priority=62
            )
        else:
            self._delete_cron_job('FBA Auto Import Shipment Report of')
    

        # Handle FBA Auto Create Removal Order Report
        if self.auto_create_removal_order_report:
            self._create_or_update_cron_job(
                'FBA Auto Create Removal Order Report of', 
                'fba_cron_auto_create_removal_order_report', 
                self.fba_removal_order_interval_number, 
                self.fba_removal_order_interval_type, 
                self.fba_removal_order_next_execution, 
                self.fba_removal_order_user,
                priority=63
            )
        else:
            self._delete_cron_job('FBA Auto Import Return Report of')
    
            

        # Handle FBA Auto Import Return Report
        if self.amz_auto_import_return_report:
            self._create_or_update_cron_job(
                'FBA Auto Import Return Report of', 
                'fba_cron_auto_import_return_report', 
                self.amz_return_report_import_interval_number, 
                self.amz_return_report_import_interval_type, 
                self.amz_return_report_import_next_execution, 
                self.amz_return_report_import_user_id,
                priority=64
            )
        else:
            self._delete_cron_job('FBA Auto Import Return Report of')

    
       
        if self.amz_stock_auto_import_by_report:
            self._create_or_update_cron_job(
                'FBA Auto Import Inventory Report of', 
                'fba_cron_auto_import_by_report', 
                self.amz_inventory_import_interval_number, 
                self.amz_inventory_import_interval_type, 
                self.amz_inventory_import_next_execution, 
                self.amz_inventory_import_user_id,
                priority=65
            )
        else:
            self._delete_cron_job('FBA Auto Import Inventory Report of')

       
        if self.auto_create_fba_stock_adj_report:
            self._create_or_update_cron_job(
                'FBA Auto Import Stock Adj Report of', 
                'fba_cron_auto_create_fba_stock_adj_report', 
                self.fba_stock_adj_report_interval_number, 
                self.fba_stock_adj_report_interval_type, 
                self.fba_stock_adj_report_next_execution, 
                self.fba_stock_adj_report_user_id,
                priority=66
            )
        else:
            self._delete_cron_job('FBA Auto Import Stock Adj Report of')


      
        if self.amz_auto_import_inbound_shipment_status:
            self._create_or_update_cron_job(
                'FBA Auto Import Inbound Shipment Status', 
                'fba_cron_auto_import_inbound_shipment_status', 
                self.amz_shipment_status_import_interval_number, 
                self.amz_shipment_status_import_interval_type, 
                self.amz_shipment_status_import_next_execution, 
                self.amz_shipment_status_import_user_id,
                priority=67
            )          
        else:
            self._delete_cron_job('FBA Auto Import Inbound Shipment Status')



    def _create_or_update_cron_job(self, name, method_name, interval_number, interval_type, nextcall, user_id, priority):
            full_name = f"{name} {self.amz_seller_id.name}"
            cron_obj = self.env['ir.cron']
            cron = cron_obj.search([('name', '=', full_name)], limit=1)
            values = {
                'name': full_name,
                'model_id': self.env['ir.model']._get('fba.cron.configuration.wizard').id,
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




    def fba_cron_auto_import_pending_orders(self):
        
        now = datetime.utcnow()
        model_id = self.env['ir.model'].search([('model', '=', 'fba.cron.configuration.wizard')], limit=1).id
        
        seller_data = self.env['ir.cron'].search([
            ('model_id', '=', model_id),
            ('code', 'like', 'model.fba_cron_auto_import_pending_orders()'),
            ('nextcall', '<=', now)
        ], order='lastcall desc', limit=1)


        
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        if not seller_data :
            return("Method Not Found")
        
        seller_id = seller_data.amz_seller_id.merchant_id
        seller = seller_data.amz_seller_id
        seller_marketplace_data = self.env['amazon.instance.ept'].search([('merchant_id', '=', seller_id)])


        operation_fba_fbm_model = self.env['amazon.process.import.export']  
            
        operation_fba_fbm_model.amz_import_fba_unshipped_orders(today, seller,seller_marketplace_data)
        


    def fba_cron_auto_import_shipment_report(self):
        pass
    
    def fba_cron_auto_create_removal_order_report(self):
        pass

    def fba_cron_auto_import_return_report(self):
        pass
    
    def fba_cron_auto_import_by_report(self):
        pass

    def fba_cron_auto_create_fba_stock_adj_report(self):
        pass   
    
    def fba_cron_auto_import_inbound_shipment_status(self):
        pass        







