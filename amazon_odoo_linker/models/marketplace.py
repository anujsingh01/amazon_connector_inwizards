from odoo import models, fields, api

class AmazonInstanceEpt(models.Model):
    _name = 'amazon.instance.ept'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    
    
    
    name = fields.Char()
    seller_id = fields.Many2one("amazon.seller.ept", string="Seller")
    # market_place_id = fields.Char()
    # is_allow_to_create_removal_order = fields.Boolean()
    
    
    active = fields.Boolean(string="Active", default=True)
    # activity_date_deadline = fields.Date(string="Next Activity Deadline")
    # activity_exception_decoration = fields.Selection([('info', 'Info'), ('warning', 'Warning'), ('danger', 'Danger')], string="Activity Exception Decoration")
    # activity_exception_icon = fields.Char(string="Icon")
    # activity_ids = fields.One2many('mail.activity', 'res_id', string="Activities")
    # activity_state = fields.Selection([('today', 'Today'), ('planned', 'Planned')], string="Activity State")
    # activity_summary = fields.Char(string="Next Activity Summary")
    # activity_type_icon = fields.Char(string="Activity Type Icon")
    # activity_type_id = fields.Many2one('mail.activity.type', string="Next Activity Type")
    # activity_user_id = fields.Many2one('res.users', string="Responsible User")
    amazon_order_data = fields.Text(string="Amazon Order Data")
    amazon_property_account_payable_id = fields.Many2one('account.account', string="Account Payable")
    amazon_property_account_receivable_id = fields.Many2one('account.account', string="Account Receivable")
    amz_tax_id = fields.Many2one('account.tax', string="Tax Account")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account (Marketplace)")
    color = fields.Integer(string="Color Index")
    company_id = fields.Many2one('res.company', string="Company")
    country_id = fields.Many2one('res.country', string="Country")
    create_date = fields.Datetime(string="Created on", readonly=True)
    create_uid = fields.Many2one('res.users', string="Created by", readonly=True)
    # display_name = fields.Char(string="Display Name", readonly=True)
    ending_balance_account_id = fields.Many2one('account.account', string="Ending Balance Account")
    ending_balance_description = fields.Char(string="Ending Balance Description")
    fba_invoice_count = fields.Integer(string="FBA Sales Invoices Count", readonly=True)
    fba_order_count = fields.Integer(string="FBA Sales Orders Count", readonly=True)
    fba_warehouse_id = fields.Many2one('stock.warehouse', string="FBA Warehouse")
    fbm_invoice_count = fields.Integer(string="FBM Sales Invoices Count", readonly=True)
    fbm_order_count = fields.Integer(string="FBM Sales Orders Count", readonly=True)
    fiscal_position_id = fields.Many2one('account.fiscal.position', string="Fiscal Position")
    flag_url = fields.Char(string="Country Flag Url", readonly=True)

    
    inventory_last_sync_on = fields.Datetime(string="Last FBM Inventory Sync Time")
    is_allow_to_create_removal_order = fields.Boolean(string="Allow Create Removal Order In FBA?")
    is_configured_rm_ord_routes = fields.Boolean(string="Configured Removal Order Routes")
    is_use_percent_tax = fields.Boolean(string="Use Tax Percent?")
    lang_id = fields.Many2one('res.lang', string="Language")
    market_place_id = fields.Char(string="Marketplace ID", readonly=True)
    marketplace_id = fields.Many2one('amazon.marketplace.ept', string="Marketplace")
    merchant_id = fields.Char(string="Merchant ID", readonly=True)
    # message_attachment_count = fields.Integer(string="Attachment Count", readonly=True)
    # message_follower_ids = fields.One2many('mail.followers', 'res_id', string="Followers")
    # message_has_error = fields.Boolean(string="Message Delivery error", readonly=True)
    # message_has_error_counter = fields.Integer(string="Number of errors", readonly=True)
    # message_has_sms_error = fields.Boolean(string="SMS Delivery error", readonly=True)
    # message_ids = fields.One2many('mail.message', 'res_id', string="Messages")
    # message_is_follower = fields.Boolean(string="Is Follower", readonly=True)
    # message_needaction = fields.Boolean(string="Action Needed", readonly=True)
    # message_needaction_counter = fields.Integer(string="Number of Actions", readonly=True)
    # message_partner_ids = fields.Many2many('res.partner', string="Followers (Partners)")
    # my_activity_date_deadline = fields.Date(string="My Activity Deadline")
    # name = fields.Char(string="Name")
    partner_id = fields.Many2one('res.partner', string="Default Customer")
    pricelist_id = fields.Many2one('product.pricelist', string="Pricelist")
    rating_ids = fields.One2many('rating.rating', 'res_id', string="Ratings")
    # after finish
    # removal_order_config_ids = fields.One2many('removal.order.config.ept', 'instance_id', string="Removal Order Configuration")
    removal_warehouse_id = fields.Many2one('stock.warehouse', string="Removal Warehouse")
    # seller_id = fields.Many2one('amazon.seller.ept', string="Seller")
    sequence = fields.Integer(string="Sequence")
    settlement_report_journal_id = fields.Many2one('account.journal', string="Settlement Report Journal")
    stock_field = fields.Selection([('free_qty', 'Free Quantity'), ('virtual_available', 'Forecast Quantity')], string="Stock Type")
    stock_update_warehouse_ids = fields.Many2many('stock.warehouse', string="FBM Warehouse(S)")
    team_id = fields.Many2one('crm.team', string="Sales Team")
    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")
    website_message_ids = fields.One2many('mail.message', 'res_id', string="Website Messages")
    write_date = fields.Datetime(string="Last Updated on", readonly=True)
    write_uid = fields.Many2one('res.users', string="Last Updated by", readonly=True)
    amazon_retail_marketplace_id = fields.Many2one("amazon.retail.marketplace", string="Amazon Marketplace")
    api_ref = fields.Char(string="API Identifier" )
    seller_central_url = fields.Char()
    region = fields.Selection([('us-east-1', 'North America'),('eu-west-1', 'Europe'),('us-west-2', 'Far Fast')])
    
    
    def test_amazon_connection(self):
        pass
    
    def configure_amazon_removal_order_routes(self):
        pass
    
    def toggle_active(self):
        pass
    
    def DashboardBoxValues(self):
        records = self.env['amazon.instance.ept'].search_read([], ['id', 'name'])
        # Assuming you want to count records for each instance
        for record in records:
            instance_id = record['id']
            product_count = self.env['amazon.product.ept'].search_count([('instance_id', '=', instance_id)])
            record['product_count'] = product_count  # Adding the count to each record
            
            FBM_order_count = self.env['sale.order'].search_count([('amz_instance_id', '=', instance_id),('amz_fulfillment_by','=',"FBM")])
            record['FBM_order_count'] = FBM_order_count  # Adding the count to each record
            
            FBA_order_count = self.env['sale.order'].search_count([('amz_instance_id', '=', instance_id),('amz_fulfillment_by','=',"FBA")])
            record['FBA_order_count'] = FBA_order_count  # Adding the count to each record

        return records
    
    
