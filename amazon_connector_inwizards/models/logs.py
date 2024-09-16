import logging

from odoo import models, fields, api


class CommonLogLinesEPT(models.Model):
    _name = 'common.log.lines.ept'
    _description = 'Common Log Line'

    activity_date_deadline = fields.Date(string='Next Activity Deadline', readonly=True)
    activity_exception_decoration = fields.Selection([], string='Activity Exception Decoration', readonly=True)
    activity_exception_icon = fields.Char(string='Icon', readonly=True)
    activity_ids = fields.One2many('mail.activity', 'res_id', string='Activities', readonly=False)
    activity_state = fields.Selection([], string='Activity State', readonly=True)
    activity_summary = fields.Char(string='Next Activity Summary')
    activity_type_icon = fields.Char(string='Activity Type Icon', readonly=True)
    activity_type_id = fields.Many2one('mail.activity.type', string='Next Activity Type')
    activity_user_id = fields.Many2one('res.users', string='Responsible User', readonly=True)
    amz_instance_ept = fields.Many2one('amazon.instance.ept', string='Amazon Instance', readonly=True)
    amz_seller_ept = fields.Many2one('amazon.seller.ept', string='Amazon Seller', readonly=True)
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    default_code = fields.Char(string='SKU')
    # display_name = fields.Char(string='Display Name', readonly=True)
    file_name = fields.Char(string='File Name')
    fulfillment_by = fields.Selection([], string='Fulfillment By')
    has_message = fields.Boolean(string='Has Message', readonly=True)
    log_book_id = fields.Many2one('common.log.book.ept', string='Log Book', readonly=True)
    log_line_type = fields.Selection([], string='Log Line Type')
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
    mismatch_details = fields.Boolean(string='Mismatch Detail')
    model_id = fields.Many2one('ir.model', string='Model', readonly=True)
    module = fields.Selection([], string='Module')
    my_activity_date_deadline = fields.Date(string='My Activity Deadline', readonly=True)
    operation_type = fields.Selection([], string='Operation')
    order_queue_data_id = fields.Many2one('shipped.order.data.queue.ept', string='Shipped Order Data Queue', readonly=True)
    order_ref = fields.Char(string='Order Reference')
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_title = fields.Char(string='Product Title')
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings', readonly=True)
    res_id = fields.Integer(string='Record ID')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    stock_move_id = fields.Many2one('stock.move', string='Stock Move', readonly=True)
    website_message_ids = fields.One2many('mail.message', 'res_id', string='Website Messages', readonly=True)
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    active_product_listing_report_ept_id = fields.Many2one('active.product.listing.report.ept', string='active listing report id', readonly=True)
    error_log= fields.Text(string='Error Occur from')




#     @api.model
#     def capture_log(self, order_ref, default_code, message, mismatch_details, model_name):
#         import pdb;pdb.set_trace()
#         model = self.env['ir.model'].search([('model', '=', model_name)], limit=1)
#         self.create({
#             'order_ref': order_ref,
#             'default_code': default_code,
#             'message': message,
#             'mismatch_details': mismatch_details,
#             'model_id': model.id,
#         })

# # Example usage of logging mechanism
# _logger = logging.getLogger(__name__)

# class SomeModel(models.Model):
#     _name = 'some.model'
#     _inherit = 'common.log.lines.ept'

#     @api.model
#     def some_method(self):
#         import pdb;pdb.set_trace()
#         try:
#             # Some code that might fail
#             pass
#         except Exception as e:
#             logger.error('An error occurred: %s', e)
#             self.capture_log(order_ref='1234', default_code='ABC', message=str(e), mismatch_details=True, model_name='some.model')
