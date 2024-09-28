from odoo import models, fields

class InboundShipment(models.Model):
    _name = 'amazon.inbound.shipment.ept'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Inbound Shipment'

    name = fields.Char()
    active = fields.Boolean(string='Active', default=True)
    activity_date_deadline = fields.Date(string='Next Activity Deadline', readonly=True)
    # activity_exception_decoration = fields.Selection([
    #     ('0', 'None'),
    #     ('1', 'Warning'),
    #     ('2', 'Danger'),
    # ], string='Activity Exception Decoration', readonly=True)
    # activity_exception_icon = fields.Char(string='Icon', readonly=True)
    # activity_ids = fields.One2many('mail.activity', 'res_id', string='Activities')
    # Include more fields based on the provided Excel data
    activity_state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned'),
    ], string='Activity State', readonly=True)
    # activity_summary = fields.Char(string='Summary')
    # activity_type_icon = fields.Char(string='Activity Type Icon', readonly=True)
    # after finish
    # activity_type_id = fields.Many2one('mail.activity.type', string='Activity Type')
    activity_user_id = fields.Many2one('res.users', string='Activity User')
    address_id = fields.Many2one("res.partner", string="Ship To Address")
    amazon_reference_id = fields.Char(string="Amazon Reference", help="A unique identifier created by Amazon that identifies this Amazon-partnered, Less Than Truckload/Full Truckload (LTL/FTL) shipment.")
    amazon_shipment_weight = fields.Float("Shipment Weight")
    amazon_shipment_weight_unit = fields.Selection([('pounds', 'Pounds'), ('kilograms', 'Kilograms')])
    amz_inbound_create_date = fields.Date()
    are_cases_required = fields.Boolean()
    box_count = fields.Integer("Number of Box")
    # after finish
    # carrier_id = fields.Many2one("delivery.carrier")
    closed_date = fields.Date()
    confirm_deadline_date =  fields.Datetime(help="The date by which this estimate must be confirmed. After this date the estimate is no longer valid and cannot be confirmed. In ISO 8601 format.")
    
    count_pickings = fields.Integer()
    # activity_warning_icon = fields.Char(string='Activity Warning Icon', readonly=True)
    automated = fields.Boolean(string='Automated')
    barcode = fields.Char(string='Barcode')
    color = fields.Integer(string='Color')
    # create_date = fields.Datetime(string='Create Date', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    declared_value_currency_id = fields.Many2one("res.currency", string="Declare Value Currency")
    estimate_amount = fields.Float(help="The amount that the Amazon-partnered carrier will charge to ship the inbound shipment.")
    # after finish
    # feed_id = fields.Many2one("feed.submission.history", string="Submit Feed Id")
    freight_ready_date = fields.Date()
    from_warehouse_id = fields.Many2one("stock.warehouse")
    fulfill_center_id = fields.Char(help="DestinationFulfillmentCenterId provided by Amazon, when we send shipment Plan to Amazon")
    instance_id_ept = fields.Many2one("amazon.instance.ept")
    intended_box_contents_source = fields.Selection([("FEED", "FEED")])
    is_billof_lading_available = fields.Boolean(help="Indicates whether the bill of lading for the shipment is available.")
    is_carton_content_updated = fields.Boolean()
    is_manually_created = fields.Boolean()
    is_partnered = fields.Boolean()
    is_picking = fields.Boolean()
    is_update_inbound_carton_contents = fields.Boolean()
    label_prep_type = fields.Char(help="LabelPrepType provided by Amazon when we send shipment Plan to Amazon")
    # after finish
    # log_ids = fields.One2many("common.log.lines.ept")
    odoo_shipment_line_ids = fields.One2many("inbound.shipment.plan.line", "odoo_shipment_id")
    partnered_ltl_id = fields.Many2one("res.partner", string="Contact")
    partnered_ltl_ids = fields.One2many("stock.quant.package", "partnered_ltl_shipment_id", string="Partnered LTL")
    partnered_small_parcel_ids = fields.One2many("stock.quant.package", "partnered_small_parcel_shipment_id", string="Partnered Small Parcel")
    picking_ids = fields.One2many("stock.picking", "odoo_shipment_id", string="Pickings")
    preview_delivery_date = fields.Datetime(string="PreviewDeliveryDate", help="The estimated date that the shipment will be delivered to an Amazon fulfillment center.")
    preview_freight_class = fields.Selection([
        ('50', '50'),('55', '55'),('60', '60'),('65', '65'),('77.5', '77.5'),('85', '85'),('92.5', '92.5'),('100', '100'),('110', '110'),('125', '125'),('150', '150'),('175', '175'), ('200', '200'), ('250', '250'),('300', '300'), ('400', '400'),('500', '500')
    ], string='Preview Freight Class')

    preview_pickup_date = fields.Datetime(string='Preview Pickup Date')
    
    pro_number = fields.Char(string='Pro Number')
    
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings')
    
    seller_declared_value = fields.Float(string='Seller Declared Value')

    seller_freight_class = fields.Selection([
        ('50', '50'),('55', '55'),('60', '60'),('65', '65'),('77.5', '77.5'),('85', '85'),('92.5', '92.5'),('100', '100'),('110', '110'),('125', '125'),('150', '150'),('175', '175'), ('200', '200'), ('250', '250'),('300', '300'), ('400', '400'),('500', '500')
    ], string='Seller Freight Class')
    
    shipment_id = fields.Char(string='Shipment ID', index=True)
    
    shipment_plan_id = fields.Many2one('inbound.shipment.plan.ept', string='Shipment Plan')
    
    shipping_type = fields.Selection([
       ('sp', '	SP (Small Parcel)'), ('ltl', 'LTL (Less Than Truckload/FullTruckload (LTL/FTL))')
    ], string='Shipping Type')
    
    state = fields.Selection([
       ("draft", "Draft"), ("WORKING", "WORKING"), ("READY_TO_SHIP", "READY_TO_SHIP"), ("SHIPPED", "SHIPPED"),("IN_TRANSIT", "IN_TRANSIT"),("IN_TRANSIT", "IN_TRANSIT"), ("DELIVERED", "DELIVERED"), ("CHECKED_IN", "CHECKED_IN"), ("RECEIVING", "RECEIVING"), ("CLOSED", "CLOSED"), ("CANCELLED", "CANCELLED"), ("DELETED", "DELETED"), ("ERROR", "ERROR")
    ], string='Shipment Status')
    
    suggest_seller_declared_value = fields.Float(string='Suggest Seller Declared Value')
    
    transport_content_exported = fields.Boolean(string='Transport Content Exported?')
    
    transport_state = fields.Selection([
        ("draft", "Draft"),("WORKING", "WORKING"),("ERROR_ON_ESTIMATING", "ERROR_ON_ESTIMATING"),("ESTIMATING","ESTIMATING"),("ESTIMATED", "ESTIMATED"), ("ERROR_ON_CONFIRMING", "ERROR_ON_CONFIRMING"), ("CONFIRMING", "CONFIRMING"), ("CONFIRMED", "CONFIRMED"), ("VOIDING", "VOIDING"), ("VOIDED", "VOIDED"), ("ERROR_IN_VOIDING", "ERROR_IN_VOIDING"), ("ERROR", "ERROR")
    ], string='Transport States')
    
    transport_type = fields.Selection([
        ("partnered_small_parcel_data", "PartneredSmallParcelData"), ("non_partnered_small_parcel_data", "NonPartneredSmallParcelData"), ("partnered_ltl_data", "PartneredLtlData"), ("non_partnered_ltl_data", "NonPartneredLtlData")
    ], string='Transport Type', readonly=True)
    
    updated_in_amazon = fields.Boolean(string='Updated In Amazon', readonly=True)
    
    void_deadline_date = fields.Datetime(string='Void Deadline Date')
    are_all_pickings_cancelled = fields.Boolean()
    
    
    def action_view_pickings(self):
        pass
    
    def check_status(self):
        pass
    
    def get_package_labels(self):
        pass
    
    def get_unique_package_labels(self):
        pass
    
    def create_shipment_picking(self):
        pass
    
    def get_package_labels(self):
        pass
    
    def export_non_partnered_small_parcel_tracking(self):
        pass
    
    def export_non_partnered_ltl_parcel_tracking(self):
        pass
    
    def export_partnered_small_parcel(self):
        pass
    
    def create_carton_contents_requests(self):
        pass
    
    def get_carton_content_result(self):
        pass
    
    def export_partnered_ltl_parcel(self):
        pass
    
    def estimate_transport_request(self):
        pass
    
    def get_transport_content(self):
        pass
    
    def confirm_transport_request(self):
        pass
    
    def void_transport_request(self):
        pass
    
    def get_bill_of_lading(self):
        pass
    
    def cancel_shipment_in_amazon_via_shipment_lines(self):
        pass
    
    def open_import_inbound_shipment_report_wizard(self):
        pass
    
    def update_inbound_shipment_qty(self):
        pass
    


class StockPicking(models.Model):
    _inherit = "stock.picking"
      
    is_fba_wh_picking = fields.Boolean()
    amazon_shipment_id = fields.Char()
    fulfill_center = fields.Char(string="Amazon Fulfillment Center ID")
    ship_label_preference = fields.Selection([("NO_LABEL", "NO_LABEL"), ("AMAZON_LABEL", "AMAZON_LABEL"),  ('SELLER_LABEL', 'SELLER_LABEL'), ('AMAZON_LABEL_ONLY', 'AMAZON_LABEL_ONLY'), ('AMAZON_LABEL_PREFERRED', 'AMAZON_LABEL_PREFERRED')], help="SELLER_LABEL - Seller labels the items in the inbound shipment when labels are required. AMAZON_LABEL_ONLY -Amazon attempts to label the items in the  inbound shipment when labels are required. If Amazon determines that it does not have the information required to successfully label an item, that item is not included in the inbound  shipment plan AMAZON_LABEL_PREFERRED - Amazon attempts to label the items in the inbound  shipment when labels are required. If Amazon determines that it does not have the information required to successfully label an item, that item is included in the inbound shipment plan and the seller must label it.",  string='LabelPrepPreference', readonly=True)
    total_shipped_qty = fields.Float()
    total_received_qty = fields.Float()
    odoo_shipment_id = fields.Many2one("amazon.inbound.shipment.ept")
    
    
class StockQuantPackage(models.Model):
    _inherit="stock.quant.package"
    
    partnered_ltl_shipment_id = fields.Many2one("amazon.inbound.shipment.ept", string="LTL Shipment")
    partnered_small_parcel_shipment_id = fields.Many2one("amazon.inbound.shipment.ept", string="Small Parcel Shipment")
    ul_id = fields.Many2one("product.ul.ept", string="Logistic Unit")
    weight_unit = fields.Selection([("pounds", "Pounds"), ("kilograms", "Kilograms")])
    weight_value = fields.Float()
    box_no = fields.Char()
    box_expiration_date = fields.Date()
    is_update_inbound_carton_contents = fields.Boolean()
    amazon_product_ids = fields.One2many("amazon.product.ept", "stock_quant_id")
    carton_info_ids = fields.One2many("amazon.carton.content.info.ept", "package_id")
    is_stacked = fields.Boolean()
    
    
class AmazonCartonContentInfoEpt(models.Model):
    _name = "amazon.carton.content.info.ept"
    
    name = fields.Char()
    package_id = fields.Many2one("stock.quant.package")
    amazon_product_id = fields.Many2one("amazon.product.ept")
    seller_sku = fields.Char()
    quantity = fields.Float("Carton Qty")
    





    
    
    

   