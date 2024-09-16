from odoo import _, api, exceptions, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    
    client_key = fields.Char(string='Client Key', config_parameter='amazon_connector_inwizards.client_key')
    client_secret_key = fields.Char(string='Client Secret Key', config_parameter='amazon_connector_inwizards.client_secret_key')
    refresh_token = fields.Char(string='Refresh Token', config_parameter='amazon_connector_inwizards.refresh_token')
    is_any_european_seller = fields.Boolean()
    amz_seller_id = fields.Many2one("amazon.seller.ept", string="Amazon Seller")
    amazon_selling = fields.Selection([("FBA", "FBA"), ("FBM", "FBM"), ("Both", "FBA & FBM")], string="Fulfillment By ?", help="Select FBA for Fulfillment by Amazon, FBM for Fulfillment by Merchant FBA & FBM for those sellers who are doing both.")
    is_default_odoo_sequence_in_sales_order_fbm = fields.Boolean("Is default Odoo Sequence in Sales Orders (FBM) ?")
    amz_order_prefix = fields.Char()
    # after finish
    # amz_auto_workflow_id = fields.Many2one("sale.workflow.process.ept", string="Amazon Auto Workflow")
    amz_fulfillment_latency = fields.Integer("Fulfillment Latency")
    amz_is_another_soft_create_fba_shipment = fields.Boolean("Does another software create the FBA shipment reports?")
    amz_def_fba_partner_id = fields.Many2one("res.partner", string="Default Customer for FBA pending order")
    # after finish
    # amz_fba_auto_workflow_id = fields.Many2one("sale.workflow.process.ept", string="Auto Workflow (FBA)")
    amz_is_default_odoo_sequence_in_sales_order_fba = fields.Boolean("Is default Odoo Sequence In Sales Orders (FBA) ?")
    amz_fba_order_prefix = fields.Char(string="Amazon FBA Order Prefix")
    is_fulfilment_center_configured = fields.Boolean("Are Fulfillment Centers Required to Import FBA Orders?")
    amz_validate_stock_inventory_for_report = fields.Boolean()
    amz_is_reserved_qty_included_inventory_report = fields.Boolean("Is Reserved Quantity to be included FBA Live Inventory Report?")
    amz_is_another_soft_create_fba_inventory = fields.Boolean("Does another software create the FBA Inventory reports?")
    is_allow_to_create_removal_order = fields.Boolean("Allow Create Removal Order In FBA?")
    amz_instance_removal_order = fields.Many2one("amazon.instance.ept", string="Removal Order Marketplace")
    removal_warehouse_id = fields.Many2one("stock.warehouse", string="Removal Warehouse")
    amz_fba_liquidation_partner = fields.Many2one("res.partner", string="FBA Liquidation Partner") 
    removal_order_report_days = fields.Integer("Removal Order Report Days")
    allow_auto_create_outbound_orders = fields.Boolean("Allow Auto Create Outbound Orders")
    amz_create_outbound_on_confirmation = fields.Boolean("Create Outbound On Order Confirmation")
    fulfillment_policy = fields.Selection([("FillOrKill", "FillOrKill"), ("FillAll", "FillAll"), ("FillAllAvailable", "FillAllAvailable")])
    fulfillment_action = fields.Selection([("Ship", "Ship"), ("Hold", "Hold")])
    shipment_category = fields.Selection([("Expedited", "Expedited"), ("Standard", "Standard"), ("Priority", "Priority"), ("ScheduledDelivery", "ScheduledDelivery")])
    amz_activity_user_ids = fields.Many2many('res.users', string="Responsible User (Amazon)")
    amz_country_id = fields.Many2one('res.country', string="Country Name")
    
    
    amz_default_outbound_instance = fields.Many2one("amazon.instance.ept", string="Default Instance for Outbound Orders")
    amz_reimbursement_customer_id = fields.Many2one("res.partner", string="Reimbursement Customer")
    amz_sales_journal_id = fields.Many2one("account.journal", string="Sale Journal")
    amz_shipment_charge_product_id =  fields.Many2one("product.product", string="Amazon Shipment Fee")
    amz_gift_wrapper_product_id = fields.Many2one("product.product", string="Amazon Gift Wrapper Fee")
    amz_promotion_discount_product_id = fields.Many2one("product.product", string="Amazon Promotion Discount")
    amz_ship_discount_product_id = fields.Many2one("product.product", string="Amazon Shipment Discount")
    amz_create_new_product = fields.Boolean(string="Allow to create new product if not found in odoo")
    amz_create_outbound_order = fields.Boolean(string="Create Outbound On Order Confirmation")
    amz_default_customer_fba = fields.Many2one('res.partner', string="Default Customer for FBA pending order")
    amz_default_instance_outbound = fields.Many2one('amazon.instance.ept', string="Default Instance for Outbound Orders")
    # after finish
    # amz_auto_workflow_fba = fields.Many2one('sale.workflow.process.ept', string="Auto Workflow (FBA)")
    
    
    company_for_amazon_id = fields.Many2one("res.company", string="Amazon Company Name")
    is_amz_create_schedule_activity = fields.Boolean("Create Schedule Activity ? ")
    amz_activity_type_id = fields.Many2one('mail.activity.type', string="Activity Type")
    amz_activity_date_deadline = fields.Integer(string="Deadline lead days")
    amz_fba_warehouse_id = fields.Many2one('stock.warehouse', string="FBA Warehouse")
    amz_gift_wrapper_fee = fields.Many2one('product.product', string="Amazon Gift Wrapper Fee")
    amz_ending_balance_account = fields.Many2one('account.account', string="Ending Balance Account")
    amz_ending_balance_description = fields.Char(string="Ending Balance Description")
    amz_marketplace_id = fields.Many2one('amazon.retail.marketplace', string="Amazon Marketplace")
    amz_pricelist_id = fields.Many2one('product.pricelist', string="Pricelist Name")
    amz_removal_order_marketplace_id = fields.Many2one('amazon.retail.marketplace', string="Removal Order Marketplace")
    amz_settlement_report_journal_id = fields.Many2one('account.journal', string="Settlement Report Journal")
    amz_stock_type = fields.Selection([('fba', 'FBA'), ('fbm', 'FBM')], string="Stock Type")
    amz_invoice_report_id = fields.Many2one('ir.actions.report', string="Invoice Report")
    amz_fba_inventory_creation = fields.Boolean(string="Does another software create the FBA Inventory Adjustment in Odoo")
    amz_fba_shipment_creation = fields.Boolean(string="Does another software create the FBA shipment in Odoo")
    amz_default_sequence_fba = fields.Boolean(string="Is default Odoo Sequence In Sales Orders (FBA) ?")
    amz_reserved_qty_included = fields.Boolean(string="Is Reserved Quantity to be included FBA Live Inventory Report")
    amz_is_usa_marketplace = fields.Boolean(string="Is USA Marketplace")
    amz_language_id = fields.Many2one('res.lang', string="Language Name")
    amz_default_outbound_marketplace_id = fields.Many2one('amazon.instance.ept', string="Default Outbound Marketplace")
    amz_default_customer_id = fields.Many2one('res.partner', string="Default Customer")
    amz_payment_term_id = fields.Many2one('account.payment.term', string="Payment Term")
    amz_promotion_discount_id = fields.Many2one('product.product', string="Amazon Promotion Discount")
    amz_reimbursement_partner_id = fields.Many2one('res.partner', string="Reimbursement Partner")
    amz_reimbursement_product_id = fields.Many2one('product.product', string="Reimbursement Product")
    amz_reimbursement_journal_id = fields.Many2one('account.journal', string="Reimbursement Journal")
    amz_ending_balance_analytic_account_id = fields.Many2one('account.analytic.account', string="Ending Balance Analytic Account")
    amz_unfulfillable_product_id = fields.Many2one('product.product', string="Unfulfillable Product")
    amz_unshipped_product_id = fields.Many2one('product.product', string="Unshipped Product")
    amz_vendor_charges_tax_id = fields.Many2one('account.tax', string="Vendor Charges Tax")
    amz_sales_team_id = fields.Many2one('crm.team', string="Sales Team")
    amz_stock_location_id = fields.Many2one('stock.location', string="Stock Location")
    amz_inventory_adjustment_report_id = fields.Many2one('ir.actions.report', string="Inventory Adjustment Report")
    amz_product_label_report_id = fields.Many2one('ir.actions.report', string="Product Label Report")
    amz_stock_warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")
    amz_unshipped_inventory_report_id = fields.Many2one('ir.actions.report', string="Unshipped Inventory Report")
    amz_seller_analytic_account_id = fields.Many2one("account.analytic.account", string="Analytic Account (Seller)")
    fba_analytic_account_id = fields.Many2one("account.analytic.account", string="Analytic Account (Seller)")
    fbm_analytic_account_id = fields.Many2one("account.analytic.account", string="Analytic Account (FBM)")
    is_european_region = fields.Boolean("Is European Region ?")
    invoice_upload_policy = fields.Selection([("amazon", "Amazon Create Invoices"), ("custom", "Upload Invoice from Odoo")])
    amz_upload_refund_invoice = fields.Boolean("Export Customer Refunds to Amazon via API?")
    amz_invoice_report = fields.Many2one("ir.actions.report", string="Invoice Report")
    
    
    amz_instance_id = fields.Many2one("amazon.instance.ept", string="Amazon Marketplace")
    amz_is_usa_marketplace = fields.Boolean("Is USA Marketplace")
    amz_instance_stock_field = fields.Selection(
        string='Stock Type',
        selection=[('free_qty', '	Free Quantity'), ('	virtual_available', '	Forecast Quantity')]
    )
    amz_instance_settlement_report_journal_id = fields.Many2one("account.journal", string="Settlement Report Journal")
    amz_instance_ending_balance_account_id = fields.Many2one("account.account", string="Ending Balance Account")
    amz_instance_ending_balance_description = fields.Char(string="Ending Balance Description")
    analytic_account_id = fields.Many2one("account.analytic.account", string="Analytic Account (Marketplace)")
    amz_lang_id = fields.Many2one("res.lang", string="Language Name")
    amz_tax_id = fields.Many2one("account.tax", string="Tax Account")
    amazon_property_account_payable_id = fields.Many2one("account.account", string="Account Payable")
    amz_instance_pricelist_id = fields.Many2one("product.pricelist", string="Pricelist Name")
    amz_partner_id = fields.Many2one("res.partner", string="Default Customer")
    amz_team_id = fields.Many2one("crm.team", string="Amazon Sales Team")
    amazon_property_account_receivable_id = fields.Many2one("account.account", string="Account Receivable")
    amz_warehouse_id = fields.Many2one("stock.warehouse", string="Amazon Warehouse")
    amz_country_id = fields.Many2one("res.country", string="Country Name")
    amz_fba_warehouse_id = fields.Many2one("stock.warehouse", string="FBA Warehouse")
    company_for_amazon_id = fields.Many2one("res.company", string="Amazon Company Name")
    stock_update_warehouse_ids = fields.Many2many("stock.warehouse", string="Stock Update Warehouses")
    
    
    
    def register_seller(self):
        pass
    
    def open_operations_tutorial(self):
        pass
    
    def document_open(self):
        pass
    
    def create_more_amazon_marketplace(self):
        # view_id = self.env.ref('module_name.view_form_model_name').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Marketplace',
            'view_mode': 'form',
            'res_model': 'add.amazon.fulfillment.center',
            'context': {
                'default_seller_id': self.amz_seller_id.id,
            },
            # 'res_id': self.id,
            # 'view_id': view_id,
            'target': 'new',
            
        }
    
    def switch_amazon_fulfillment_by(self):
        pass
    
    def sync_fba_fulfilment_centers(self):
        pass
    
    def create_amazon_seller_transaction_type(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': "Amazon Chart Of Account's",
            'view_type': 'tree,form',
            'view_mode': 'tree,form',
            'res_model': 'amazon.transaction.line.ept',
            # 'res_id': self.id,
            'target': 'current',  # Use 'current' for replacing current view
        }
    
    def create_vcs_tax(self):
        pass
    
    def download_attached_module(self):
        pass
    
    
    def res_config_amazon_seller_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seller',
            'view_mode': 'form',
            'res_model': 'res.config.amazon.seller',
            'target': 'new',
        }
