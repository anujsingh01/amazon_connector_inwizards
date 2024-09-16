from odoo import models, fields, api

class AmazonSellerEPT(models.Model):
    _name = "amazon.seller.ept"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    active = fields.Boolean(string="Active", default=True)
    allow_auto_create_outbound_orders = fields.Boolean(string="Allow Auto Create Outbound Orders")
    allow_to_process_shipped_order = fields.Boolean(string="Allow to process shipped order (FBM) in odoo ?")
    amazon_program = fields.Selection([('pan_eu', 'PAN EU'), ('efn', 'EFN'), ('mci', 'mci'), ('cep', 'cep'), ('efn+mci', 'EFN+MCI'), ], string="Amazon Program")
    amazon_selling = fields.Selection([('FBA', 'FBA'), ('FBM', 'FBM'), ('Both', 'FBA & FBM')], string="Fulfillment By ?")
    amz_activity_date_deadline = fields.Integer(string="Deadline lead days")
    amz_activity_type_id = fields.Many2one('mail.activity.type', string="Activity Type")
    amz_activity_user_ids = fields.Many2many('res.users', string="Responsible User (Amazon)")
    amz_auto_import_inbound_shipment_status = fields.Boolean(string="Auto Import Inbound Shipment Status ?")
    amz_auto_import_shipped_orders = fields.Boolean(string="Auto Import Shipped Orders?")
    amz_auto_import_vcs_tax_report = fields.Boolean(string="Auto import VCS Tax report ?")
    amz_auto_process_vcs_tax_report = fields.Boolean(string="Download and Process VCS Tax Report ?")
    amz_auto_upload_tax_invoices = fields.Boolean(string="Auto Upload Tax Invoices to Amazon ?")
    amz_fba_liquidation_partner = fields.Many2one('res.partner', string="FBA Liquidation Partner")
    amz_fba_us_program = fields.Selection([('narf', 'NARF')], string="Amz Fba Us Program")
    amz_invoice_report = fields.Many2one('ir.actions.report', string="Invoice Report")
    amz_is_reserved_qty_included_inventory_report = fields.Boolean(string="Is Reserved Quantity to be included FBA Live Inventory Report?")
    amz_order_auto_update = fields.Boolean(string="Auto Update Order Shipment ?")
    amz_outbound_instance_id = fields.Many2one('amazon.instance.ept', string="Default Outbound Marketplace")
    amz_seller_analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account (Seller)")
    amz_stock_auto_export = fields.Boolean(string="Stock Auto Export?")
    
    amz_upload_refund_invoice = fields.Boolean(string="Export Customer Refunds to Amazon via API?")
    amz_warehouse_ids = fields.One2many('stock.warehouse', 'seller_id', string="Warehouses")
    auth_token = fields.Char(string="Auth Token")
    auto_check_cancel_order = fields.Boolean(string="Auto Check Cancel Order ?")
    auto_create_fba_stock_adj_report = fields.Boolean(string="Auto Create FBA Stock Adjustment Report ?")
    auto_create_removal_order_report = fields.Boolean(string="Auto Create Removal Order Report ?")
    auto_import_fba_pending_order = fields.Boolean(string="Auto Import FBA Pending Order?")
    auto_import_product_stock = fields.Boolean(string="Auto Import Amazon FBA Live Stock Report")
    auto_import_rating_report = fields.Boolean(string="Auto Import Rating Report?")
    auto_import_return_report = fields.Boolean(string="Auto Import Return Report?")
    auto_import_shipment_report = fields.Boolean(string="Auto Import Shipment Report?")
    auto_process_rating_report = fields.Boolean(string="Auto Process Rating Report?")
    auto_send_invoice = fields.Boolean(string="Auto Send Invoice Via Email ?")
    auto_send_refund = fields.Boolean(string="Auto Send Refund Via Email ?")
    # after finish
    # b2b_amazon_tax_ids = fields.One2many('amazon.tax.configuration.ept', 'seller_id', string="B2B VCS Tax")
    cancel_fbm_order_last_sync_on = fields.Datetime(string="Last Cancel FBM Order Request Time")
    company_id = fields.Many2one('res.company', string="Company")
    country_id = fields.Many2one('res.country', string="Region")
    create_date = fields.Datetime(string="Created on", readonly=True)
    create_new_product = fields.Boolean(string="Allow to create new product if not found in odoo ?")
    create_outbound_on_confirmation = fields.Boolean(string="Create Outbound On Order Confirmation")
    create_uid = fields.Many2one('res.users', string="Created by", readonly=True)
    cron_count = fields.Integer(string="Scheduler Count", readonly=True)
    customer_return_report_days = fields.Integer(string="Customer Return Report Days")
    def_fba_partner_id = fields.Many2one('res.partner', string="Default Customer for FBA pending order")
    default_outbound_instance = fields.Many2one('amazon.instance.ept', string="Default Instance for Outbound Orders")
    fba_analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account (FBA)")
    fba_auto_workflow_id = fields.Many2one('sale.workflow.process.ept', string="Auto Workflow (FBA)")
    fba_order_last_sync_on = fields.Datetime(string="Last FBA Order Sync Time")
    
    
    fba_order_prefix = fields.Char(string="FBA Order Prefix")
    fba_pending_order_last_sync_on = fields.Datetime(string="FBA Pending Order Last Sync Time")
    fba_recommended_removal_report_last_sync_on = fields.Datetime(string="Last FBA Recommended Report Request Time")
    fba_vcs_report_days = fields.Integer(string="Default VCS Request Report Days")
    fbm_analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account (FBM)")
    fbm_auto_workflow_id = fields.Many2one('sale.workflow.process.ept', string="Auto Workflow (FBM)")
    fulfillment_action = fields.Selection([('Ship', 'Ship'), ('Hold', 'Hold')], string="Fulfillment Action")
    fulfillment_latency = fields.Integer(string="Fulfillment Latency")
    fulfillment_policy = fields.Selection([('FillOrKill', 'FillOrKill'), ('FillAll', 'FillAll'), ('FillAllAvailable', 'FillAllAvailable')], string="Fulfillment Policy")
    gift_wrapper_product_id = fields.Many2one('product.product', string="Gift Wrapper Fee")
    
    instance_ids = fields.One2many('amazon.instance.ept', "seller_id", string="Marketplaces")
    inv_adjustment_report_days = fields.Integer(string="Inventory Adjustment Report Days")
    inventory_report_last_sync_on = fields.Datetime(string="Last Inventory Report Request Time")
    invoice_upload_policy = fields.Selection([('amazon', 'Amazon Create invoices'), ('custom', 'Upload Invoice from Odoo')], string="Invoice Upload Policy")
    is_amz_create_schedule_activity = fields.Boolean(string="Create Schedule Activity ?")
    is_another_soft_create_fba_inventory = fields.Boolean(string="Does another software create the FBA Inventory reports?")
    is_another_soft_create_fba_shipment = fields.Boolean(string="Does another software create the FBA shipment reports?")
    is_default_odoo_sequence_in_sales_order = fields.Boolean(string="Is default Odoo Sequence in Sales Orders ?")
    # order = fields.Char(string="Orders ?")
    
    
    is_default_odoo_sequence_in_sales_order_fba = fields.Boolean(string="Is default Odoo Sequence In Sales Orders (FBA) ?")
    is_european_region = fields.Boolean(string="Is European Region ?")
    is_fulfilment_center_configured = fields.Boolean(string="Are Fulfillment Centers Required to Import FBA Orders?")
    is_north_america_region = fields.Boolean(string="Is North America Region ?")
    is_sp_api_amz_seller = fields.Boolean(string="Is SPAPI Seller?", default=True)
    is_vcs_activated = fields.Boolean(string="Is VCS Activated ?")
    last_inbound_shipment_status_sync = fields.Datetime(string="Last Inbound Shipment Status Sync")
    live_inv_adjustment_report_days = fields.Integer(string="Live Inventory Adjustment Report Days")
    # after finish
    marketplace_ids = fields.One2many('amazon.marketplace.ept', 'seller_id', string="Amazon Marketplaces")
    merchant_id = fields.Char(string="Merchant ID")
    name = fields.Char(string="Name")
    order_auto_import = fields.Boolean(string="Auto Order Import?")
    order_last_sync_on = fields.Datetime(string="Last FBM Order Sync Time")
    order_prefix = fields.Char(string="Order Prefix")
    other_pan_europe_country_ids = fields.Many2many('res.country', string="Other Pan Europe Countries")
    payment_term_id = fields.Many2one('account.payment.term', string="Payment Term")
    promotion_discount_product_id = fields.Many2one('product.product', string="Promotion Discount")
    rating_ids = fields.One2many('rating.rating', 'res_id', string="Ratings")
    rating_report_days = fields.Integer(string="Rating Report Days")
    rating_report_last_sync_on = fields.Datetime(string="Last Rating Report Request Time")
    reimbursement_customer_id = fields.Many2one('res.partner', string="Reimbursement Customer")
    reimbursement_product_id = fields.Many2one('product.product', string="Product")
    removal_order_report_days = fields.Integer(string="Removal Order Report Days")
    removal_order_report_last_sync_on = fields.Datetime(string="Last Removal Order Report Request Time")
    return_report_last_sync_on = fields.Datetime(string="Last Return Report Request Time")
    sale_journal_id = fields.Many2one('account.journal', string="Sales Journal")
    settlement_report_auto_create = fields.Boolean(string="Auto Create Settlement Report ?")
    settlement_report_last_sync_on = fields.Datetime(string="Settlement Report Last Sync Time")
    ship_discount_product_id = fields.Many2one('product.product', string="Shipment Discount")
    shipment_category = fields.Selection([('Expedited', 'Expedited'), ('Standard', 'Standard'), ('Priority', 'Priority'), ('ScheduledDelivery', 'ScheduledDelivery')], string="Shipment Category")
    shipment_charge_product_id = fields.Many2one('product.product', string="Shipment Fee")
    shipping_report_days = fields.Integer(string="Shipping Report Report Days")
    shipping_report_last_sync_on = fields.Datetime(string="Last Shipping Report Request Time")
    stock_adjustment_report_last_sync_on = fields.Datetime(string="Last Stock Adjustment Report Request Time")
    store_inv_wh_efn = fields.Many2one('res.country', string="Store Inv. Country")
    # after finish
    # transaction_line_ids = fields.One2many('amazon.transaction.line.ept', 'seller_id', string="Transactions")
    update_shipment_last_sync_on = fields.Datetime(string="Last Shipment update status Sync Time")
    validate_stock_inventory_for_report = fields.Boolean(string="Auto Validate Amazon FBA Live Stock Report")
    vcs_report_last_sync_on = fields.Datetime(string="Last VCS Report Request Time")
    vidr_report_last_sync_on = fields.Datetime(string="Last VIDR Report Request Time")
    website_message_ids = fields.One2many('mail.message', 'res_id', string="Website Messages")
    write_date = fields.Datetime(string="Last Updated on", readonly=True)
    write_uid = fields.Many2one('res.users', string="Last Updated by", readonly=True)
    
    
    
    def load_marketplace(self):
        pass
    
    def active_iap_database(self):
        pass
    
    def re_authorisation_to_sp_api(self):
        pass
    
    def amazon_instance_list(self):
        return {
            'name': 'Amazon Marketplaces',
            'type': 'ir.actions.act_window',
            'res_model': 'amazon.instance.ept',
            'view_mode': 'tree',
        }
    
    def toggle_active(self):
        pass
    
    def list_of_seller_cron(self):
        pass
    
    # def global_cron_configuration_action(self):
    #     return {
    #         'name': 'Global Cron Configuration',
    #         'type': 'ir.actions.act_window',
    #        'context': {
    #             'default_amz_seller_id': self.id,
    #             'default_amazon_selling' : "Both"
    #         },
    #         'res_model': 'global.cron.job',
    #         'view_mode': 'form',
    #         'target': 'new',
    #     }
    
    
    def fba_cron_configuration_action(self):
        context = {
            'default_amz_seller_id': self.id,
            'default_amazon_selling': "FBA",
        }

        
        cron_order_import = self.env['ir.cron'].search([('name', '=', f'FBA Auto Import Pending Orders of {self.name}')], limit=1)
        cron_shipment_report = self.env['ir.cron'].search([('name', '=', f'FBA Auto Import Shipment Report of {self.name}')], limit=1)
        cron_removal_order_report = self.env['ir.cron'].search([('name', '=', f'FBA Auto Create Removal Order Report of {self.name}')], limit=1)
        cron_return_report = self.env['ir.cron'].search([('name', '=', f'FBA Auto Import Return Report of {self.name}')], limit=1)
        cron_inventory_report = self.env['ir.cron'].search([('name', '=', f'FBA Auto Import Inventory Report of {self.name}')], limit=1)
        cron_stock_adj_report = self.env['ir.cron'].search([('name', '=', f'FBA Auto Import Stock Adj Report of {self.name}')], limit=1)
        cron_inbound_shipment_status = self.env['ir.cron'].search([('name', '=', f'FBA Auto Import Inbound Shipment Status {self.name}')], limit=1)


        # Set values in the context based on the presence of each cron job
        if cron_order_import:
            context.update({
                'default_amz_pending_order_import_user_id': cron_order_import.create_uid.id,
                'default_amz_pending_order_import_interval_number': cron_order_import.interval_number,
                'default_amz_pending_order_import_interval_type': cron_order_import.interval_type,
                'default_amz_pending_order_import_next_execution': cron_order_import.nextcall,
                'default_amz_auto_import_fba_pending_order': True,
                
            })
            
        if cron_shipment_report:
            context.update({
                'default_amz_ship_report_import_user_id': cron_shipment_report.create_uid.id,
                'default_amz_ship_report_import_interval_number': cron_shipment_report.interval_number,
                'default_amz_ship_report_import_interval_type': cron_shipment_report.interval_type,
                'default_amz_ship_report_import_next_execution': cron_shipment_report.nextcall,
                'default_amz_auto_import_shipment_report': True,
            })
            
        if cron_removal_order_report:
            context.update({
                'default_fba_removal_order_user': cron_removal_order_report.create_uid.id,
                'default_fba_removal_order_interval_number': cron_removal_order_report.interval_number,
                'default_fba_removal_order_interval_type': cron_removal_order_report.interval_type,
                'default_fba_removal_order_next_execution': cron_removal_order_report.nextcall,
                'default_auto_create_removal_order_report': True,
            })

        if cron_return_report:
            context.update({
                'default_amz_return_report_import_user_id': cron_return_report.create_uid.id,
                'default_amz_return_report_import_interval_number': cron_return_report.interval_number,
                'default_amz_return_report_import_interval_type': cron_return_report.interval_type,
                'default_amz_return_report_import_next_execution': cron_return_report.nextcall,
                'default_amz_auto_import_return_report': True,
            })


        if cron_inventory_report:
            context.update({
                'default_amz_inventory_import_user_id': cron_inventory_report.create_uid.id,
                'default_amz_inventory_import_interval_number': cron_inventory_report.interval_number,
                'default_amz_inventory_import_interval_type': cron_inventory_report.interval_type,
                'default_amz_inventory_import_next_execution': cron_inventory_report.nextcall,
                'default_amz_stock_auto_import_by_report': True,
            })

        if cron_stock_adj_report:
            context.update({
                'default_fba_stock_adj_report_user_id': cron_stock_adj_report.create_uid.id,
                'default_fba_stock_adj_report_interval_number': cron_stock_adj_report.interval_number,
                'default_fba_stock_adj_report_interval_type': cron_stock_adj_report.interval_type,
                'default_fba_stock_adj_report_next_execution': cron_stock_adj_report.nextcall,
                'default_auto_create_fba_stock_adj_report': True,
            })

        if cron_inbound_shipment_status:
            context.update({
                'default_amz_shipment_status_import_user_id': cron_inbound_shipment_status.create_uid.id,
                'default_amz_shipment_status_import_interval_number': cron_inbound_shipment_status.interval_number,
                'default_amz_shipment_status_import_interval_type': cron_inbound_shipment_status.interval_type,
                'default_amz_shipment_status_import_next_execution': cron_inbound_shipment_status.nextcall,
                'default_amz_auto_import_inbound_shipment_status': True,
            })



        return {
            'name': 'FBA Cron Configuration',
            'type': 'ir.actions.act_window',
            'res_model': 'fba.cron.configuration.wizard',
            'context': context,
            'view_mode': 'form',
            'target': 'new',
        }
    
    
    def fbm_cron_configuration_action(self):

        # Initialize context
        context = {
            'default_amz_seller_id': self.id,
            'default_amazon_selling': "FBM",
        }
        
        # Search for cron jobs
        cron_unshipped = self.env['ir.cron'].search([('name', '=', f'FBM Auto Import Orders of {self.name}')], limit=1)
        cron_shipped = self.env['ir.cron'].search([('name', '=', f'FBM Auto Import Shipped Orders of {self.name}')], limit=1)
        cron_export_stock = self.env['ir.cron'].search([('name', '=', f'FBM Auto Export Stock of {self.name}')], limit=1)
        cron_update_order = self.env['ir.cron'].search([('name', '=', f'FBM Update Order Status of {self.name}')], limit=1)
        cron_canceled_order = self.env['ir.cron'].search([('name', '=', f'FBM Check Canceled Orders of {self.name}')], limit=1)
        
        # Set values in the context based on the presence of each cron job
        if cron_unshipped:
            context.update({
                'default_amz_order_import_user_id': cron_unshipped.create_uid.id,
                'default_amz_order_import_interval_number': cron_unshipped.interval_number,
                'default_amz_order_import_interval_type': cron_unshipped.interval_type,  # Use the actual interval type
                'default_amz_order_import_next_execution': cron_unshipped.nextcall,
                'default_amz_order_auto_import': True,
            })
        
        if cron_shipped:
            context.update({
                'default_auto_import_fbm_shipped_user_id': cron_shipped.create_uid.id,
                'default_auto_import_fbm_shipped_interval_number': cron_shipped.interval_number,
                'default_auto_import_fbm_shipped_interval_type': cron_shipped.interval_type,
                'default_auto_import_fbm_shipped_next_execution': cron_shipped.nextcall,
                'default_amz_auto_import_shipped_orders': True,
            })
        
        if cron_export_stock:
            context.update({
                'default_amz_inventory_export_user_id': cron_export_stock.create_uid.id,
                'default_amz_inventory_export_interval_number': cron_export_stock.interval_number,
                'default_amz_inventory_export_interval_type': cron_export_stock.interval_type,
                'default_amz_inventory_export_next_execution': cron_export_stock.nextcall,
                'default_amz_stock_auto_export': True,
            })
        
        if cron_update_order:
            context.update({
                'default_amz_order_update_user_id': cron_update_order.create_uid.id,
                'default_amz_order_update_interval_number': cron_update_order.interval_number,
                'default_amz_order_update_interval_type': cron_update_order.interval_type,
                'default_amz_order_update_next_execution': cron_update_order.nextcall,
                'default_amz_order_auto_update': True,
            })
        
        if cron_canceled_order:
            context.update({
                'default_amz_cancel_order_report_user_id': cron_canceled_order.create_uid.id,
                'default_amz_cancel_order_interval_number': cron_canceled_order.interval_number,
                'default_amz_cancel_order_interval_type': cron_canceled_order.interval_type,
                'default_amz_cancel_order_next_execution': cron_canceled_order.nextcall,
                'default_amz_auto_check_cancel_order': True,
            })
                 
                    
        return {
            'name': 'FBM Cron Configuration',
            'type': 'ir.actions.act_window',
            'res_model': 'fbm.cron.configuration.wizard',
            # 'context': {
            #     'default_amz_seller_id': self.id,
            #     'default_amazon_selling' : "FBM"
            # },
            'context': context,
            'view_mode': 'form',
            'target': 'new',
        }
        
        
    def global_cron_configuration_action(self):
        context = {
            'default_amz_seller_id': self.id,
            'default_amazon_selling': "Both",
        }        
        
        
        # Search for cron jobs
        cron_amazon_settlement_report = self.env['ir.cron'].search([('name', '=', f'Amazon Settlement Report Auto-Create of {self.name}')], limit=1)
        cron_amazon_rating_report = self.env['ir.cron'].search([('name', '=', f'Amazon Rating Report Auto-Import of {self.name}')], limit=1)
        cron_vcs_tax_report = self.env['ir.cron'].search([('name', '=', f'Amazon VCS Tax Report Auto-Import of {self.name}')], limit=1)
        cron_upload_tax_invoice = self.env['ir.cron'].search([('name', '=', f'Amazon Auto Upload Tax Invoices of {self.name}')], limit=1)

        # Set values in the context based on the presence of each cron job
        if cron_amazon_settlement_report:
            context.update({
                'default_amz_settlement_report_create_user_id': cron_amazon_settlement_report.create_uid.id,
                'default_amz_settlement_report_create_interval_number': cron_amazon_settlement_report.interval_number,
                'default_amz_settlement_report_create_interval_type': cron_amazon_settlement_report.interval_type,  # Use the actual interval type
                'default_amz_settlement_report_create_next_execution': cron_amazon_settlement_report.nextcall,
                'default_amz_settlement_report_auto_create': True,
            })
        
        if cron_amazon_rating_report:
            context.update({
                'default_amz_rating_report_import_user_id': cron_amazon_rating_report.create_uid.id,
                'default_amz_rating_report_import_interval_number': cron_amazon_rating_report.interval_number,
                'default_amz_rating_report_import_interval_type': cron_amazon_rating_report.interval_type,
                'default_amz_rating_report_import_next_execution': cron_amazon_rating_report.nextcall,
                'default_amz_auto_import_rating_report': True,
            })
        
        if cron_vcs_tax_report:
            context.update({
                'default_amz_vcs_report_import_user_id': cron_vcs_tax_report.create_uid.id,
                'default_amz_vcs_report_import_interval_number': cron_vcs_tax_report.interval_number,
                'default_amz_vcs_report_import_interval_type': cron_vcs_tax_report.interval_type,
                'default_amz_vcs_report_import_next_execution': cron_vcs_tax_report.nextcall,
                'default_amz_auto_import_vcs_tax_report': True,
            })
        
        if cron_upload_tax_invoice:
            context.update({
                'default_amz_auto_upload_tax_invoices_user_id': cron_upload_tax_invoice.create_uid.id,
                'default_amz_auto_upload_tax_invoices_interval_number': cron_upload_tax_invoice.interval_number,
                'default_amz_auto_upload_tax_invoices_interval_type': cron_upload_tax_invoice.interval_type,
                'default_amz_auto_upload_tax_invoices_next_execution': cron_upload_tax_invoice.nextcall,
                'default_amz_auto_upload_tax_invoices': True,
            })
        

                 
                    
        return {
            'name': 'Global Cron Configuration',
            'type': 'ir.actions.act_window',
            'res_model': 'global.cron.job.wizard',
            # 'context': {
            #     'default_amz_seller_id': self.id,
            #     'default_amazon_selling' : "FBM"
            # },
            'context': context,
            'view_mode': 'form',
            'target': 'new',
        }