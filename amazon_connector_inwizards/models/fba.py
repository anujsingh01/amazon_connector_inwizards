from odoo import models, fields

class ShippingReportRequestHistory(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'shipping.report.request.history'
    _description = 'Shipping Report'

    name = fields.Char(string='Name')
    activity_date_deadline = fields.Date(string='Next Activity Deadline', readonly=True)
    activity_exception_decoration = fields.Selection([('warning', 'Alert'), ('danger', 'Error')],string='Activity Exception Decoration', readonly=True)
    activity_exception_icon = fields.Char(string='Icon', readonly=True)
    # activity_ids = fields.One2many('mail.activity', 'res_id', string='Activities')
    activity_state = fields.Selection([('overdue','Overdue'), ('today','Today'), ('planned','Planned')],string='Activity State', readonly=True)
    activity_summary = fields.Char(string='Next Activity Summary')
    activity_type_icon = fields.Char(string='Activity Type Icon', readonly=True)
    # activity_type_id = fields.Many2one("mail.activity.type", string='Next Activity Type')
    activity_user_id = fields.Char(string='Responsible User', readonly=True)
    amazon_sale_order_ids = fields.One2many('sale.order', 'amz_shipment_report_id', string='Sales Order Ids')
    attachment_id = fields.Many2one("ir.attachment", string='Attachment')
    company_id = fields.Many2one("res.company", string='Company', readonly=True)
    end_date = fields.Datetime(string='End Date')
    has_message = fields.Boolean(string='Has Message', readonly=True)
    is_fulfillment_center = fields.Boolean(string='Is Fulfillment Center')
    log_count = fields.Integer(string='Log Count', readonly=True)
    message_attachment_count = fields.Integer(string='Attachment Count', readonly=True)
    # message_follower_ids = fields.One2many('mail.followers', 'res_id', string='Followers')
    message_has_error = fields.Boolean(string='Message Delivery error', readonly=True)
    message_has_error_counter = fields.Integer(string='Number of errors', readonly=True)
    message_has_sms_error = fields.Boolean(string='SMS Delivery error', readonly=True)
    message_ids = fields.One2many('mail.message', 'res_id', string='Messages')
    message_is_follower = fields.Boolean(string='Is Follower', readonly=True)
    message_needaction = fields.Boolean(string='Action Needed', readonly=True)
    message_needaction_counter = fields.Integer(string='Number of Actions', readonly=True)
    message_partner_ids = fields.Many2many("res.partner", string='Followers (Partners)')
    mismatch_details = fields.Boolean(string='Mismatch Details', readonly=True)
    moves_count = fields.Integer(string='Move Count', readonly=True)
    my_activity_date_deadline = fields.Date(string='My Activity Deadline', readonly=True)
    order_count = fields.Integer(string='Order Count', readonly=True)
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings')
    report_document_id = fields.Char(string='Report Document ID')
    report_id = fields.Char(string='Report ID')
    report_request_id = fields.Char(string='Report Request ID')
    report_type = fields.Char(string='Report Type')
    requested_date = fields.Datetime(string='Requested Date')
    seller_id = fields.Many2one("amazon.seller.ept", string='Seller')
    start_date = fields.Datetime(string='Start Date')
    # state = fields.Selection(string='Report Status')
    state = fields.Selection([('draft', 'Draft'),('SUBMITTED', 'SUBMITTED'),('_SUBMITTED_', 'SUBMITTED'),('_IN_PROGRESS_', 'IN_PROGRESS'),('_CANCELLED_  ', 'CANCELLED'),('IN_FATAL', 'IN_FATAL'),('_DONE_', 'DONE'),('CANCELLED', 'CANCELLED'),('DONE', 'DONE'), ('FATAL','FATAL'), ('IN_PROGRESS','IN_PROGRESS'), ('IN_QUEUE','IN_QUEUE'), ('_DONE_NO_DATA_','DONE_NO_DATA'), ('processed', 'PROCESSED'), ('imported', 'Imported'), ('partially_processed', 'Partially Processed'), ('closed','Closed')])
    user_id = fields.Many2one("res.users", string='Requested User')
    # website_message_ids = fields.One2many('mail.message', 'res_id', string='Website Messages')
   
   
#    amz_shipment_report_id


    def download_report(self):
        pass
    
    def configure_missing_fulfillment_center(self):
        pass
    
    def list_of_process_logs(self):
        pass
    
    def process_shipment_file(self):
        pass
    
    def process_shipment_file(self):
        pass
    
    def get_report(self):
        pass
    
    def get_report_request_list(self):
        pass
    
    def request_report(self):
        pass
    
    def list_of_sales_orders(self):
        pass
    
    def list_of_stock_moves(self):
        pass