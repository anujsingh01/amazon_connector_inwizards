from odoo import models, fields

class AmazonTransactionType(models.Model):
    _name = 'amazon.transaction.type'
    _description = 'Amazon Transaction Type'

    amazon_code = fields.Char(string='Transaction Code')
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    # display_name = fields.Char(string='Display Name')
    is_reimbursement = fields.Boolean(string='REIMBURSEMENT?')
    name = fields.Char(string='Name', required=True)
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    
    
class AmazonTransactionLine(models.Model):
    _name = 'amazon.transaction.line.ept'
    _description = 'Amazon Transaction Line'

    account_id = fields.Many2one('account.account', string='Account')
    amazon_code = fields.Char(string='Amazon Code', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    display_name = fields.Char(string='Display Name')
    seller_id = fields.Many2one('amazon.seller.ept', string='Seller')
    tax_id = fields.Many2one('account.tax', string='Tax')
    transaction_type_id = fields.Many2one('amazon.transaction.type', string='Transaction Type')
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)       
