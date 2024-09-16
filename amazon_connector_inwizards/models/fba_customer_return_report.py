from odoo import _, api, exceptions, fields, models


class SaleOrderReturnReport(models.Model):
    _name = 'sale.order.return.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    attachment_id = fields.Many2one('ir.attachment', string='Attachment')
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    # display_name = fields.Char(string='Display Name', readonly=True)
    end_date = fields.Datetime(string='End Date')
    has_message = fields.Boolean(string='Has Message')
    log_count = fields.Integer(string='Log Count')
    message_attachment_count = fields.Integer(string='Message Attachment Count')
    # message_follower_ids = fields.Many2many('res.partner', string='Message Followers')
    message_has_error = fields.Boolean(string='Message Has Error')
    message_has_error_counter = fields.Integer(string='Message Has Error Counter')
    message_has_sms_error = fields.Boolean(string='SMS Delivery error')
    # message_ids = fields.One2many('mail.message', 'res_id', string='Messages', domain=[('model', '=', _name)])
    message_is_follower = fields.Boolean(string='Is Follower')
    message_needaction = fields.Boolean(string='Message Need Action')
    message_needaction_counter = fields.Integer(string='Message Need Action Counter')
    message_partner_ids = fields.Many2many('res.partner', string='Message Partners')
    mismatch_details = fields.Boolean(string='Mismatch Details')
    name = fields.Char(string='Name')
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings')
    report_document_id = fields.Char(string='Report Document ID')
    report_id = fields.Char(string='Report ID')
    report_request_id = fields.Char(string='Report Request ID')
    report_type = fields.Char(string='Report Type')
    requested_date = fields.Datetime(string='Requested Date')
    return_count = fields.Integer(string='Return Count', readonly=True)
    seller_id = fields.Many2one('amazon.seller.ept', string='Seller')
    start_date = fields.Datetime(string='Start Date')
    state = fields.Selection([('draft', 'Draft'),('SUBMITTED', 'SUBMITTED'),('_SUBMITTED_', 'SUBMITTED'),('_IN_PROGRESS_', 'IN_PROGRESS'),('_CANCELLED_  ', 'CANCELLED'),('IN_FATAL', 'IN_FATAL'),('_DONE_', 'DONE'),('CANCELLED', 'CANCELLED'),('DONE', 'DONE'), ('FATAL','FATAL'), ('IN_PROGRESS','IN_PROGRESS'), ('IN_QUEUE','IN_QUEUE'), ('_DONE_NO_DATA_','DONE_NO_DATA'), ('processed', 'PROCESSED'), ('imported', 'Imported'), ('partially_processed', 'Partially Processed'), ('closed','Closed')])
    user_id = fields.Many2one('res.users', string='Requested User')
    website_message_ids = fields.One2many('mail.message', 'res_id', string='Website Messages')
    
    
    def request_report(self):
        pass
    
    def get_report_request_list(self):
        pass
    
    def get_report(self):
        pass
    
    def download_report(self):
        pass
    
    def process_return_report_file(self):
        pass
    
    def process_return_report_file(self):
        pass
    
    def list_of_process_logs(self):
        pass
    
    def list_of_return_orders(self):
        pass
    
    
    