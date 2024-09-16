from odoo import _, api, exceptions, fields, models

class AmazonFbaLiveStockReportEpt(models.Model):
    _name = "amazon.fba.live.stock.report.ept"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    amazon_program = fields.Selection([], string='Amazon Program', readonly=True)
    amz_instance_id = fields.Many2one('amazon.instance.ept', string='Marketplace')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    # display_name = fields.Char(string='Display Name', readonly=True)
    end_date = fields.Datetime(string='End Date')
    inventory_count = fields.Integer(string='Inventory Count', readonly=True)
    log_count = fields.Integer(string='Log Count', readonly=True)
    name = fields.Char(string='Name')
    # after finish
    # quant_ids = fields.One2many('stock.quant', 'fba_live_stock_report_id', string='Inventory')
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings')
    report_date = fields.Date(string='Report Date')
    report_document_id = fields.Char(string='Report Document ID')
    report_id = fields.Char(string='Report ID', required=True)
    report_request_id = fields.Char(string='Report Request ID', required=True)
    report_type = fields.Char(string='Report Type')
    requested_date = fields.Datetime(string='Requested Date')
    seller_id = fields.Many2one('amazon.seller.ept', string='Seller')
    start_date = fields.Datetime(string='Start Date')
    state = fields.Selection([('draft', 'Draft'),('SUBMITTED', 'SUBMITTED'),('_SUBMITTED_', 'SUBMITTED'),('_IN_PROGRESS_', 'IN_PROGRESS'),('_CANCELLED_  ', 'CANCELLED'),('IN_FATAL', 'IN_FATAL'),('_DONE_', 'DONE'),('CANCELLED', 'CANCELLED'),('DONE', 'DONE'), ('FATAL','FATAL'), ('IN_PROGRESS','IN_PROGRESS'), ('IN_QUEUE','IN_QUEUE'), ('_DONE_NO_DATA_','DONE_NO_DATA'), ('processed', 'PROCESSED'), ('imported', 'Imported'), ('partially_processed', 'Partially Processed'), ('closed','Closed')], default="draft", string='Report Status')
    user_id = fields.Many2one('res.users', string='Requested User')
    website_message_ids = fields.One2many('mail.message', 'res_id', string='Website Messages')
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True) 
    
    def download_report(self):
        pass
        
    def request_report(self):
        pass

    def get_report_request_list(self):
        pass

    def get_report(self):
        pass

    def process_fba_live_stock_report(self):
        pass

    def set_fulfillment_channel_sku(self):
        pass

    def list_of_logs(self):
        pass

    def list_of_inventory(self):
        pass
    