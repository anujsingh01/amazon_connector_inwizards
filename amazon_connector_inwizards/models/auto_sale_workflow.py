from odoo import _, api, exceptions, fields, models


class SaleWorkflowProcessEPT(models.Model):
    _name = "sale.workflow.process.ept"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    # activity_date_deadline = fields.Date(string="Next Activity Deadline", readonly=True)
    # activity_exception_decoration = fields.Selection([('info', 'Info'), ('warning', 'Warning'), ('danger', 'Danger')], string="Activity Exception Decoration")
    # activity_exception_icon = fields.Char(string="Icon")
    # activity_ids = fields.One2many('mail.activity', 'res_id', string="Activities")
    # activity_state = fields.Selection([('today', 'Today'), ('planned', 'Planned')], string="Activity State")
    # activity_summary = fields.Char(string="Next Activity Summary")
    # activity_type_icon = fields.Char(string="Activity Type Icon")
    # activity_type_id = fields.Many2one('mail.activity.type', string="Next Activity Type")
    # activity_user_id = fields.Many2one('res.users', string="Responsible User")
    create_date = fields.Datetime(string="Created on", readonly=True)
    create_invoice = fields.Boolean(string="Create & Validate Invoice")
    create_uid = fields.Many2one('res.users', string="Created by", readonly=True)
    # display_name = fields.Char(string="Display Name", readonly=True)
    # has_message = fields.Boolean(string="Has Message", readonly=True)
    # id = fields.Integer(string="ID", readonly=True)
    inbound_payment_method_id = fields.Many2one('account.payment.method', string="Debit Method")
    invoice_date_is_order_date = fields.Boolean(string="Force Accounting Date")
    journal_id = fields.Many2one('account.journal', string="Payment Journal")
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
    name = fields.Char(string="Name")
    picking_policy = fields.Selection([('direct', 'Deliver each product when available'), ('one', 'Deliver all products at once')], string="Shipping Policy")
    rating_ids = fields.One2many('rating.rating', 'res_id', string="Ratings")
    register_payment = fields.Boolean(string="Register Payment")
    sale_journal_id = fields.Many2one('account.journal', string="Sales Journal")
    validate_order = fields.Boolean(string="Confirm Quotation")
    website_message_ids = fields.One2many('mail.message', 'res_id', string="Website Messages")
    write_date = fields.Datetime(string="Last Updated on", readonly=True)
    write_uid = fields.Many2one('res.users', string="Last Updated by", readonly=True)
    
    
    


    