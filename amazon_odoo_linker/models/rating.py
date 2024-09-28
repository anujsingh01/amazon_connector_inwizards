from odoo import models, fields, api

class Rating(models.Model):
    _name = "rating.rating"
    
    access_token = fields.Char()
    amz_fulfillment_by = fields.Selection([('FBA','	Amazon Fulfillment Network'), ('FBM', '	Merchant Fulfillment Network')])
    amz_instance_id = fields.Many2one("amazon.instance.ept", string="Marketplace")
    amz_rating_report_id = fields.Many2one("rating.report.history", string="Amazon Rating Report History")
    amz_rating_submitted_date = fields.Date(string="Amazon Rating Submitted Date")
    consumed = fields.Boolean(string="Filled Rating")
    # display_name = fields.Char()
    feedback = fields.Text(string="Comment")
    is_internal = fields.Boolean(string="Visible Internally Only")
    message_id = fields.Many2one("mail.message", string="Message")
    partner_id = fields.Many2one("res.partner", string="Customer")
    publisher_comment = fields.Text()
    publisher_datetime = fields.Datetime()
    publisher_id = fields.Many2one("res.partner", string="Commented by")
    rated_partner_id = fields.Many2one("res.partner", string="Rated Operator")
    rated_partner_name = fields.Char()
    rating = fields.Float("Rating Value")
    rating_image = fields.Binary(string="Image")
    rating_image_url = fields.Char(string="Image Url")
    rating_text = fields.Selection([('top', 'Satisfied'), ('ok', 'Okay'), ('ko', 'Dissatisfied'), ('none', 'No Rating yet')])
    parent_res_name =  fields.Char(string="Parent Document Name")
    res_name =  fields.Char(string="Resource name")
    res_id = fields.Many2one("rating.report.history")
    
class RatingReportHistory(models.Model):
    _name = "rating.report.history"
    
    amz_rating_report_ids = fields.One2many("rating.rating", "amz_rating_report_id", string="Ratings (Amz)")
    attachment_id = fields.Many2one("ir.attachment", string="Attachment")
    company_id = fields.Many2one("res.company", string="Company")
    end_date = fields.Date()
    has_message = fields.Boolean()
    # instance_id = fields.Many2one("amazon.instance.ept", string="Marketplace")
    log_count = fields.Integer()
    message_attachment_count = fields.Integer()
    message_follower_ids = fields.One2many("mail.followers", "res_id", string="Followers")
    message_has_error = fields.Boolean()
    message_has_error_counter = fields.Integer()
    message_has_sms_error = fields.Boolean("SMS Delivery error")
    message_ids = fields.One2many("mail.message", "res_id", string="Messages")
    message_is_follower = fields.Boolean()
    message_needaction = fields.Boolean()
    message_needaction_counter = fields.Integer()
    message_partner_ids =  fields.Many2many("res.partner")  
    name = fields.Char()
    rating_count = fields.Integer()
    rating_ids = fields.One2many("rating.rating", "res_id", string="Ratings")
    report_document_id= fields.Char()
    report_id = fields.Char()
    report_request_id = fields.Char()
    report_type = fields.Char()
    requested_date = fields.Date()
    seller_id = fields.Many2one("amazon.seller.ept", string="Seller")
    start_date = fields.Datetime()
    state = fields.Selection([('draft', 'Draft'),('_SUBMITTED_', 'SUBMITTED'),('_IN_PROGRESS_', 'IN_PROGRESS'),('_CANCELLED_  ', 'CANCELLED'),
                              ('_DONE_', 'DONE'),('CANCELLED', 'CANCELLED'),('SUBMITTED', 'SUBMITTED'),
                              ('DONE', 'DONE'), ('FATAL','FATAL'), ('IN_PROGRESS','IN_PROGRESS'), ('IN_QUEUE','IN_QUEUE'), ('_DONE_NO_DATA_','DONE_NO_DATA'), ('processed', 'PROCESSED'), ('imported', 'Imported'), ('partially_processed', 'Partially Processed'), ('closed','Closed')
                              ])
    user_id = fields.Many2one("res.users", string="Requested User")
    website_message_ids = fields.One2many("mail.message", "res_id", string="Website Messages")
    

    def download_report(self):
        pass
   

class Reissue(models.Model):
    _name = "reissue.reissue" 
    
    name = fields.Char()
    