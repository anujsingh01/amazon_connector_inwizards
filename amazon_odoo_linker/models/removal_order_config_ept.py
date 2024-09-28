from odoo import models, fields, api


class RemovalOrderConfigEpt(models.Model):
    _name = 'removal.order.config.ept'
    
    instance_id = fields.Many2one('amazon.instance.ept', string="Marketplace")
    location_id = fields.Many2one('stock.location', string="Location")
    picking_type_id = fields.Many2one('stock.picking.type', string="Picking Type")
    removal_disposition = fields.Selection([('sellable', 'Sellable'), ('unsellable', 'Unsellable')], string="Disposition")
    sellable_route_id = fields.Many2one('stock.route', string="Sellable Route")
    unsellable_route_id = fields.Many2one('stock.route', string="UnSellable Route")
   
    
    
class AmazonFulfillmentCenter(models.Model):
    _name = "amazon.fulfillment.center"
    
    seller_id = fields.Many2one("amazon.seller.ept", string="Seller")
    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse")
    center_code = fields.Char(string="Fulfillment Center Code")
    
    
class StockRoute(models.Model):
    _inherit="stock.route"
    
    is_removal_order = fields.Boolean()
    