from odoo import _, api, exceptions, fields, models

class AddAmazonProduct(models.Model):
    _inherit = "product.template"
    _description = "Product create on amazon"
    
    amazon_sku = fields.Char(string="Amazon SKU")
    
    
    def add_amazon_product(self):
        pass
    