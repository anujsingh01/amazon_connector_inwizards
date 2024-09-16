from odoo import models, fields, api

class ShippedOrderDataQueueEPT(models.Model):
    _name = 'shipped.order.data.queue.ept'
    
    
    name = fields.Char(string='Name')
    activity_ids = fields.One2many('mail.activity', "res_id", string='Activities')
    amz_seller_id = fields.Many2one("amazon.seller.ept", string='Amazon Seller')
    create_date = fields.Datetime(string='Created on')
    log_count = fields.Integer(string='Move Count')
    log_lines = fields.One2many('common.log.lines.ept', "order_queue_data_id", string='Log Lines')
    message_follower_ids = fields.One2many('mail.followers', "res_id", string='Followers')
    message_ids = fields.One2many('mail.message', "res_id", string='Messages')
    queue_line_done_record = fields.Integer(string='Done Records')
    queue_line_draft_record = fields.Integer(string='Draft Records')
    queue_line_fail_record = fields.Integer(string='Fail Records')
    queue_line_total_record = fields.Integer(string='Total Records')
    shipped_order_data_queue_lines = fields.One2many('shipped.order.data.queue.line.ept', "shipped_order_data_queue_id", string='Shipped Order Queue Lines')
    state = fields.Selection([('draft', 'Draft'), ('partially_completed', 'Partially Completed'), ('completed', 'Completed')],string='State')

    
    # activity_date_deadline = fields.Date(string='Next Activity Deadline')
    # activity_exception_decoration = fields.Selection([('')],string='Activity Exception Decoration')
    # activity_exception_icon = fields.Char(string='Icon')
    # activity_state = fields.Selection(string='Activity State')
    # activity_summary = fields.Char(string='Next Activity Summary')
    # activity_type_icon = fields.Char(string='Activity Type Icon')
    # activity_type_id = fields.Char(string='Next Activity Type')
    # activity_user_id = fields.Char(string='Responsible User')
    # company_id = fields.Char(string='Company')
    # create_uid = fields.Char(string='Created by')
    # display_name = fields.Char(string='Display Name')
    # has_message = fields.Char(string='Has Message')
    # message_attachment_count = fields.Char(string='Attachment Counamazon_product_tree_view_eptt')
    # message_has_error = fields.Char(string='Message Delivery error')
    # message_has_error_counter = fields.Char(string='Number of errors')
    # message_has_sms_error = fields.Char(string='SMS Delivery error')
    # message_is_follower = fields.Char(string='Is Follower')
    # message_needaction = fields.Char(string='Action Needed')
    # message_needaction_counter = fields.Char(string='Number of Actions')
    # message_partner_ids = fields.Char(string='Followers (Partners)')
    # my_activity_date_deadline = fields.Date(string='My Activity Deadline')
    # rating_ids = fields.One2many('rating.rating', string='Ratings')
    # website_message_ids = fields.One2many('mail.message', string='Website Messages')
    # write_date = fields.Char(string='Last Updated on')
    # write_uid = fields.Char(string='Last Updated by')
    
    
    def process_order(self):
        pass


class ShippedOrderDataQueueLineEpt(models.Model):
    _name = "shipped.order.data.queue.line.ept"

    order_id= fields.Char(string="Order")
    order_data_id=fields.Char(string="Order Data")
    order_status=fields.Selection([('Pending', 'Pending'), ('Unshipped', 'Unshipped'), ('PartiallyShipped', 'PartiallyShipped'), 
                                   ('Shipped', 'Shipped'), ('Canceled', 'Canceled'), ('Unfulfillable', 'Unfulfillable'), 
                                   ('InvoiceUnconfirmed', 'InvoiceUnconfirmed'), ('PendingAvailability', 'PendingAvailability')], string="Order Status")
    amz_instance_id=fields.Many2one("amazon.instance.ept", string="Marketplace")
    last_process_date=fields.Datetime()
    state=fields.Selection([('draft', 'Draft'), ('fail', 'Fail'), ('done', 'Done')], string="State")
    
    shipped_order_data_queue_id= fields.Many2one("shipped.order.data.queue.ept")
                               
class Commonlogline(models.Model):
    _name = "common.log.lines.ept"
    
    order_ref = fields.Char(string="Order Reference")
    default_code = fields.Char(string="SKU")
    message = fields.Text()
    order_queue_data_id  = fields.Many2one("shipped.order.data.queue.ept")