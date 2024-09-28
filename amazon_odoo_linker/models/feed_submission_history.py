from odoo import models, fields


class FeedSubmissionHistory(models.Model):
    _name = 'feed.submission.history'
    _description = 'Feed Submission History'

    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    # display_name = fields.Char(string='Display Name', readonly=True)
    feed_document_id = fields.Char(string='Feed Document ID')
    feed_result = fields.Text(string='Feed Result')
    feed_result_date = fields.Datetime(string='Feed Result Date')
    feed_result_id = fields.Char(string='Feed Result ID')
    feed_submit_date = fields.Datetime(string='Feed Submit Date')
    feed_type = fields.Selection([], string='Feed Submission Type')
    has_message = fields.Boolean(string='Has Message', readonly=True)
    instance_id = fields.Many2one('amazon.instance.ept', string='Marketplace')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    message = fields.Text(string='Message')
    message_attachment_count = fields.Integer(string='Attachment Count', readonly=True)
    message_follower_ids = fields.One2many('mail.followers', 'res_id', string='Followers', readonly=True)
    message_has_error = fields.Boolean(string='Message Delivery Error', readonly=True)
    message_has_error_counter = fields.Integer(string='Number of Errors', readonly=True)
    message_has_sms_error = fields.Boolean(string='SMS Delivery Error', readonly=True)
    message_ids = fields.One2many('mail.message', 'res_id', string='Messages', readonly=True)
    message_is_follower = fields.Boolean(string='Is Follower', readonly=True)
    message_needaction = fields.Boolean(string='Action Needed', readonly=True)
    message_needaction_counter = fields.Integer(string='Number of Actions', readonly=True)
    message_partner_ids = fields.Many2many('res.partner', string='Followers (Partners)')
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings', readonly=True)
    seller_id = fields.Many2one('amazon.seller.ept', string='Seller')
    user_id = fields.Many2one('res.users', string='Requested User')
    website_message_ids = fields.One2many('mail.message', 'res_id', string='Website Messages', readonly=True)
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)




