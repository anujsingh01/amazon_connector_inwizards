from odoo import _, api, exceptions, fields, models



class AmazonStockAdjustmentConfig(models.Model):
    _name = "amazon.stock.adjustment.config"
    
    create_date = fields.Datetime(string="Created on", readonly=True)
    create_uid = fields.Many2one('res.users', string="Created by", readonly=True)
    email_template_id = fields.Many2one('mail.template', string="Email Template")
    group_id = fields.Many2one('amazon.adjustment.reason.group', string="Group")
    is_send_email = fields.Boolean(string="Is Send Email ?")
    location_id = fields.Many2one('stock.location', string="Location")
    seller_id = fields.Many2one('amazon.seller.ept', string="Seller")
    write_date = fields.Datetime(string="Last Updated on", readonly=True)
    write_uid = fields.Many2one('res.users', string="Last Updated by", readonly=True)
    
    
    
class AmazonStockAdjustmentConfigReason(models.Model):
    _name = "amazon.adjustment.reason.group"
    
    create_date = fields.Datetime(string="Created on", readonly=True)
    create_uid = fields.Many2one('res.users', string="Created by", readonly=True)
    write_date = fields.Datetime(string="Last Updated on", readonly=True)
    write_uid = fields.Many2one('res.users', string="Last Updated by", readonly=True)
    is_counter_part_group = fields.Boolean()
    name = fields.Char()
    reason_code_ids = fields.One2many("amazon.adjustment.reason.code", 'group_id')
    
    
class AmazonAdjustmentReasonGroup(models.Model):
    _name = 'amazon.adjustment.reason.code'
    
    counter_part_id = fields.Many2one("amazon.adjustment.reason.code", string="Counter Part")
    group_id = fields.Many2one("amazon.adjustment.reason.group", string="Group")
    is_reimbursed = fields.Boolean()
    long_description = fields.Text()
    type= fields.Selection([('-', '-'), ('+', '+')])
    description = fields.Char()
    name = fields.Char()
    