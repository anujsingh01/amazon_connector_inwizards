from odoo import _, api, exceptions, fields, models

class Inboundshipmentplan(models.Model):
    _name = 'inbound.shipment.plan.ept'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Inboundshipmentplan'
    
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    count_odoo_shipment = fields.Integer(string='Count Odoo Shipment', readonly=True)
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    # display_name = fields.Char(string='Display Name', readonly=True)
    # has_message = fields.Boolean(string='Has Message', readonly=True)
    instance_id = fields.Many2one('amazon.instance.ept', string='Marketplace', readonly=True)
    intended_box_contents_source = fields.Selection([('Feed', 'Feed')], string='Intended BoxContents Source', readonly=True)
    is_are_cases_required = fields.Boolean(string='Are Cases Required?')
    is_partnered = fields.Boolean(string='Is Partnered')
    label_preference = fields.Selection([('SELLER_LABEL', 'SELLER_LABEL'), ('AMAZON_LABEL_ONLY', 'AMAZON_LABEL_ONLY'), ('AMAZON_LABEL_PREFERRED', 'AMAZON_LABEL_PREFERRED')], help="SELLER_LABEL - Seller labels the items in the inbound shipment when labels are required. AMAZON_LABEL_ONLY -Amazon attempts to label the items in the  inbound shipment when labels are required. If Amazon determines that it does not have the information required to successfully label an item, that item is not included in the inbound  shipment plan AMAZON_LABEL_PREFERRED - Amazon attempts to label the items in the inbound  shipment when labels are required. If Amazon determines that it does not have the information required to successfully label an item, that item is included in the inbound shipment plan and the seller must label it.",  string='LabelPrepPreference', readonly=True)
    # after finish
    # log_ids = fields.One2many('common.log.lines.ept',  string='Log', readonly=True)
    # message_attachment_count = fields.Integer(string='Attachment Count', readonly=True)
    # message_follower_ids = fields.One2many('mail.followers', 'res_id', string='Followers')
    # message_has_error = fields.Boolean(string='Message Delivery error', readonly=True)
    # message_has_error_counter = fields.Integer(string='Number of errors', readonly=True)
    # message_has_sms_error = fields.Boolean(string='SMS Delivery error', readonly=True)
    # message_ids = fields.One2many('mail.message', 'res_id', string='Messages')
    # message_is_follower = fields.Boolean(string='Is Follower', readonly=True)
    # message_needaction = fields.Boolean(string='Action Needed', readonly=True)
    # message_needaction_counter = fields.Integer(string='Number of Actions', readonly=True)
    # message_partner_ids = fields.Many2many('res.partner', string='Followers (Partners)')
    name = fields.Char(string='Name', readonly=True)
    # odoo_shipment_ids = fields.One2many('amazon.inbound.shipment.ept', 'shipment_plan_id', string='Amazon Shipments')
    picking_ids = fields.Many2many('stock.picking', 'ship_plan_id', string='Picking')
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings')
    ship_from_address_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    ship_to_address_ids = fields.Many2many('res.partner', string='Partner', readonly=True)
    ship_to_country = fields.Many2one('res.country', string='Partner', readonly=True)
    # sale_id = fields.Many2one('sale.order', string='Sale Order')
    # seller_id = fields.Many2one('res.partner', string='Seller')
    shipment_line_ids = fields.One2many('inbound.shipment.plan.line', 'shipment_plan_id', string='Shipment Lines')
    shipping_type = fields.Selection([("sp", "SP (Small Parcel)"), ("ltl", "LTL (Less Than Truckload/FullTruckload (LTL/FTL))")] )
    state = fields.Selection([('draft', 'Draft'), ('plan_approved', 'Shipment Plan Approved'), ('cancel', 'Cancelled')], string='State')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', readonly=True)
    # website_message_ids = fields.One2many('mail.message', 'res_id', string='Website Messages')
    # write_date = fields.Datetime(string='Last Updated on', readonly=True)
    # write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    
    
    def create_inbound_shipment_plan(self):
        pass
    
    def set_to_draft_ept(self):
        pass
    
    def import_product_for_inbound_shipment(self):
        pass
    
    def action_view_inbound_shipment(self):
        pass
    
    
class InboundShipmentPlanLine(models.Model):
    _name = "inbound.shipment.plan.line"
    
    amazon_product_id = fields.Many2one("amazon.product.ept", string="Amazon Product")
    odoo_product_id = fields.Many2one("product.product")
    quantity = fields.Float()
    seller_sku = fields.Char()
    fn_sku = fields.Char(string="Fulfillment Network SKU")
    quantity_in_case = fields.Float()
    difference_qty = fields.Float("Difference Quantity")
    shipment_plan_id = fields.Many2one("inbound.shipment.plan.ept")
    odoo_shipment_id = fields.Many2one("amazon.inbound.shipment.ept")
    received_qty = fields.Float("Received Quantity")
    is_extra_line = fields.Boolean()
    
    
    