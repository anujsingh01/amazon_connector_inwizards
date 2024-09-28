from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    partner_shipping_id = fields.Many2one( comodel_name='res.partner', string='Delivery Address')
    amz_shipment_report_id = fields.Many2one("shipping.report.request.history")
    amz_fulfillment_action = fields.Selection([("Ship", "Ship"), ("Hold", "Hold")], string="Fulfillment Action")
    amz_delivery_end_time = fields.Datetime(string='Delivery End Time')
    amz_delivery_start_time = fields.Datetime(string='Delivery Start Time')
    amz_displayable_date_time = fields.Date(string='Displayable Order Date Time')
    amz_fulfillment_by = fields.Selection([("FBA", "Amazon Fulfillment Network"), ("FBM", "Merchant Fullfillment Network")], string='Fulfillment By')
    amz_fulfillment_instance_id = fields.Many2one("amazon.instance.ept", string='Fulfillment Marketplace')
    amz_fulfillment_policy = fields.Selection([("FillOrKill", "FillOrKill"), ("FillAll", "FillAll"), ("FillAllAvailable", "FillAllAvailable")], string='Fulfillment Policy')
    amz_fulfullment_order_status = fields.Selection([("RECEIVED", "RECEIVED"), ("INVALID", "INVALID"), ("PLANNING", "PLANNING"), ("PROCESSING", "PROCESSING"), ("CANCELLED", "CANCELLED"), ("COMPLETE", "COMPLETE"), ("COMPLETE_PARTIALLED", "COMPLETE_PARTIALLED"), ("UNFULFILLABLE", "UNFULFILLABLE")], string='Fulfillment Order Status')
    amz_instance_country_code = fields.Char(string='Marketplace Country')
    amz_instance_id = fields.Many2one("amazon.instance.ept", string='Marketplace')
    amz_is_outbound_order = fields.Boolean(string='Out Bound Order')
    amz_order_reference = fields.Char(string='Amazon Order Reference')
    amz_sales_order_report_id = fields.Many2one("fbm.sale.order.report.ept", string='Sales Order Report Id')
    amz_seller_id = fields.Many2one("amazon.seller.ept", string='Amazon Seller')
    # amz_shipment_report_id = fields.Many2one(string='Amazon Shipping Report')
    amz_shipment_service_level_category = fields.Selection([("Expedited", "Expedited"), ("NextDay", "NextDay"), ("SecondDay", "SecondDay"), ("Standard", "Standard"), ("FreeEconomy", "FreeEconomy"), ("Priority", "Priority"), ("ScheduledDelivery", "ScheduledDelivery"), ("SameDay", "SameDay"), ("Scheduled", "Scheduled")], string='FBA Shipping Speed')
    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse")
    order_has_fba_warehouse = fields.Boolean()
    is_fba_pending_order = fields.Boolean()
    buyer_requested_cancellation = fields.Boolean()
    buyer_cancellation_reason = fields.Boolean()
    is_amazon_canceled = fields.Boolean()
    is_business_order = fields.Boolean()
    is_prime_order = fields.Boolean()
    exported_in_amazon = fields.Boolean()
    notify_by_email = fields.Boolean()
    
    amz_order_id = fields.Char(string='Amazon Order ID')
    amz_OrderStatus = fields.Char(string='Order Status')
    
    
    def create_outbound_shipment(self):
        pass
    
    
    def cancel_order_in_amazon(self):
        pass
    
    
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
        
    warehouse_id_ept = fields.Many2one("stock.warehouse")
    
class InvoiceCreate(models.Model):
    _inherit = "account.move"    
    amz_order_id = fields.Char(string='Amazon Order ID')
    
    
    
    