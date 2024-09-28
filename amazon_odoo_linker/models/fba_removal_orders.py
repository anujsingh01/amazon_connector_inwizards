from odoo import models, fields

class RemovalOrder(models.Model):
    _name = 'amazon.removal.order.ept'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Removal Order'

    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    # display_name = fields.Char(string='Display Name', readonly=True, store=False)
    disposition_location_id = fields.Many2one('stock.location', string='Unsellable Location', readonly=True, store=False)
    has_message = fields.Char(string='Has Message', readonly=True, store=False)
    instance_id = fields.Many2one('amazon.instance.ept', string='Marketplace', readonly=True)
    last_feed_submission_id = fields.Char(string='Feed Submission Id', help="This Fields relocates last feed submission id.")
    # message_attachment_count = fields.Char(string='Attachment Count', readonly=True, store=False)
    # message_follower_ids = fields.Many2one('mail.followers', string='Followers')
    # message_has_error = fields.Char(string='Message Delivery error', readonly=True, store=False)
    # message_has_error_counter = fields.Char(string='Number of errors', readonly=True, store=False)
    # message_has_sms_error = fields.Char(string='SMS Delivery error', readonly=True, store=False)
    # message_ids = fields.Many2one('mail.message', string='Messages')
    # message_is_follower = fields.Char(string='Is Follower', readonly=True, store=False)
    # message_needaction = fields.Char(string='Action Needed', readonly=True, store=False)
    # message_needaction_counter = fields.Char(string='Number of Actions', readonly=True, store=False)
    # message_partner_ids = fields.Many2one('res.partner', string='Followers (Partners)', store=False)
    name = fields.Char(string='Name')
    rating_ids = fields.One2many('rating.rating', "res_id", string='Ratings')
    removal_count = fields.Integer(string='Removal Order Pickings', readonly=True, store=False)
    removal_disposition = fields.Selection([("Return", "Return"), ("Disposal", "Disposal"), ("Liquidations", "Liquidations")], help="This Fields relocates type of disposition.")
    # after finish
    # removal_order_lines_ids = fields.One2many('removal.orders.lines.ept', "removal_order_id", string='Removal Orders Lines')
    # removal_order_picking_ids = fields.Many2one('stock.picking', 'removal_order_id', string='Removal Pickings')
    ship_address_id = fields.Many2one('res.partner', string='Ship Address', readonly=True)
    shipping_notes = fields.Text(string='Notes')
    state = fields.Selection([("draft", "Draft"), ("plan_approved", "Removal Plan Approved"), ("Cancelled", "Cancelled"), ("In Process", "In Process"), ("Completed", "Completed")], default="draft")
    warehouse_id = fields.Many2one('stock.warehouse', string='Destination Warehouse')
    website_message_ids = fields.Many2one('mail.message', string='Website Messages')
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    
    
    def create_removal_order(self):
        pass
    
    def get_unsellable_products(self):
        pass
    
    def import_product_for_removal_order(self):
        pass
    
    def list_of_transfer_removal_pickings(self):
        pass