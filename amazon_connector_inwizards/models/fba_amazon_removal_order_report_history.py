
from odoo import _, api, exceptions, fields, models

class AmazonRemovalOrderReportHistory(models.Model):
    _name = "amazon.removal.order.report.history"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    # display_name = fields.Char(string='Display Name', readonly=True, store=False)
    end_date = fields.Datetime(string='End Date')
    has_message = fields.Boolean(string='Has Message', readonly=True, store=False)
    instance_id = fields.Many2one('amazon.instance.ept', string='Marketplace')
    log_count = fields.Integer(string='Log Count', readonly=True, store=False)
    mismatch_details = fields.Boolean(string='Mismatch Details', readonly=True, store=False)
    name = fields.Char(string='Name')
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings')
    removal_count = fields.Integer(string='Removal Count', readonly=True, store=False)
    # after finish
    # removal_picking_ids = fields.One2many('stock.picking', 'removal_order_report_id', string='Pickings')
    report_document_id = fields.Char(string='Report Document ID')
    report_id = fields.Char(string='Report ID')
    report_request_id = fields.Char(string='Report Request ID', readonly=True)
    report_type = fields.Char(string='Report Type')
    requested_date = fields.Datetime(string='Requested Date')
    seller_id = fields.Many2one('amazon.seller.ept', string='Seller')
    start_date = fields.Datetime(string='Start Date')
    state = fields.Selection([('draft', 'Draft'),('SUBMITTED', 'SUBMITTED'),('_SUBMITTED_', 'SUBMITTED'),('_IN_PROGRESS_', 'IN_PROGRESS'),('_CANCELLED_  ', 'CANCELLED'),('IN_FATAL', 'IN_FATAL'),('_DONE_', 'DONE'),('CANCELLED', 'CANCELLED'),('DONE', 'DONE'), ('FATAL','FATAL'), ('IN_PROGRESS','IN_PROGRESS'), ('IN_QUEUE','IN_QUEUE'), ('_DONE_NO_DATA_','DONE_NO_DATA'), ('processed', 'PROCESSED'), ('imported', 'Imported'), ('partially_processed', 'Partially Processed'), ('closed','Closed')], default="draft", string='Report Status')
    
    user_id = fields.Many2one('res.users', string='Requested User')
    
    
    def request_report(self):
        pass

    def get_report_request_list(self):
        pass

    def get_report(self):
        pass

    def download_report(self):
        pass

    def process_removal_order_report(self):
        pass

    def process_removal_order_report(self):
        pass

    def list_of_logs(self):
        pass

    def list_of_removal_pickings(self):
        pass