from odoo import _, api, exceptions, fields, models

class AmazonMarketplaceEpt(models.Model):
    _name = "amazon.marketplace.ept"

    name = fields.Char()
    country_id = fields.Many2one("res.country", string="Country")
    currency_id = fields.Many2one("res.currency", string="Currency")
    seller_id = fields.Many2one('amazon.seller.ept', string='Seller')
    instance_id = fields.Many2one('amazon.instance.ept', string='Seller')
    lang_id = fields.Many2one("res.lang", string="Language")
    market_place_id = fields.Char(string="Marketplace")