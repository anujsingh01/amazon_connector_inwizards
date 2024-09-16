from odoo import models, fields, api
import json
import requests
from ...odoo_amazon_connector import amazon_api, utils

class AmazonProductEPT(models.Model):
    _name = "amazon.product.ept"
    
    name = fields.Char(string="Product Name")
    
    # Product info
    
    seller_sku = fields.Char(string="Seller SKU")
    product_id = fields.Many2one("product.product", string="Odoo Product")
    fix_stock_type =  fields.Selection([('fix', 'Fix'), ('percentage', 'Percentage')],string='Fix Stock Type')
    fix_stock_value = fields.Float()
    fulfillment_latency = fields.Integer()
    related_product_type = fields.Selection([('ean', 'EAN'), ('ASIN', 'ASIN'), ('GTIN', 'GTIN'), ('UPC', 'UPC')])
    related_product_value =  fields.Char()
    product_upc = fields.Char()
    barcode = fields.Char()
    product_asin=fields.Char()
    asin_qty = fields.Integer()
    
    # Amazon Info
    
    exported_to_amazon = fields.Boolean()
    instance_id = fields.Many2one("amazon.instance.ept",  required=True, readonly=True, string="Marketplace")
    fulfillment_by = fields.Selection([('FBM', 'Manufacturer Fullfillment Network'), ('FBA', 'Amazon Fullfillment Network')], required=True)
    launch_date = fields.Datetime()
    discontinue_date = fields.Datetime()
    release_date = fields.Datetime()
    
    # Product Listing Element
    designer = fields.Char(string="Designer")
    package_weight_uom = fields.Selection([('gr', 'GR'), ('kg', 'KG'), ('oz', 'OZ'), ('lb', 'LB'), ('mg', 'MG')])
    package_weight = fields.Float()
    shipping_weight_uom = fields.Selection([('gr', 'GR'), ('kg', 'KG'), ('oz', 'OZ'), ('lb', 'LB'), ('mg', 'MG')])
    shipping_weight = fields.Float()
    package_dimensions_uom = fields.Selection([('cm', 'CM'), ('m', 'M'), ('ft', 'FT'), ('in', 'IN'), ('mm', 'MM')])
    package_height= fields.Float()
    package_length= fields.Float()
    package_width= fields.Float()
    max_order_quantity = fields.Integer()
    item_package_qty = fields.Integer(sting="Package Quantity")
    condition =  fields.Selection([('new','New (DEPRECATED)'), ('new_item','NewItem'),('new_with_warranty','New With Warranty'),
                                   ('new_oem','New OEM'),('new_open_box','New Open Box'),('used_like_new','Used Like New'),
                                   ('used_very_good','Used Very Good'),('used_good','Used Good'),('used_acceptable','Used Acceptable'),
                                   ('used_poor','Used Poor'),('used_refurbished','Used Refurbished'),('CollectibleLikeNew','CollectibleLikeNew'),
                                   ('CollectibleVeryGood','CollectibleVeryGood'),('CollectibleGood','CollectibleGood'),('CollectibleAcceptable','CollectibleAcceptable'),
                                   ('CollectiblePoor','CollectiblePoor'),('RefurbishedWithWarranty','RefurbishedWithWarranty'),('Refurbished','Refurbished')])
    standard_product_id_type = fields.Selection([('ean', 'EAN'), ('ASIN', 'ASIN'), ('GTIN', 'GTIN'), ('UPC', 'UPC')])
    gtin_exemption_reason = fields.Selection([('part', 'Part'), ('bundle', 'Bundle')])
    item_dimensions_uom =  fields.Selection([('cm', 'CM'), ('m', 'M'), ('ft', 'FT'), ('in', 'IN'), ('mm', 'MM')])
    item_height= fields.Float()
    item_length= fields.Float()
    item_width= fields.Float()
    allow_package_qty = fields.Boolean()
    is_gift_wrap_available = fields.Boolean()
    is_gift_message_available = fields.Boolean()
    
    stock_quant_id = fields.Many2one("stock.quant.package")
    
    # Description & Disclaimer
    long_description = fields.Text()
    
    def send_product(self):
        active_ids = self._context.get('active_ids', [])
        account = self.env["amazon.info.account"].search([("seller_id", "=", self.seller_id.id)])
        operation = "productCrud"
        seller = self.seller_id
        
        if active_ids:
            products = self.browse(active_ids)
            for product in products:
                ProductpriceListId= self.env["product.pricelist"].search_read([("instance_id", "=", product.instance_id.id)],["id","seller_id","instance_id"])[0]

                Pricelistitem= self.env["product.pricelist.item"].search_read([("pricelist_id", "=", ProductpriceListId["id"]),("amazon_sku", "=", product.seller_sku)],["id","amazon_sku","fixed_price","maximum_retail_price"])[0]
                
                seller_id = self.env["amazon.seller.ept"].search_read([("id", "=", ProductpriceListId["seller_id"][0])],["merchant_id"])[0]["merchant_id"]
                
                instance_id= self.env["amazon.instance.ept"].search_read([("id", "=", product.instance_id.id)],["api_ref"])[0]["api_ref"]
                amazon_sku = Pricelistitem["amazon_sku"]
                
                payload = json.dumps({
                "productType": "PRODUCT",
                "patches": [
                    {
                    "op": "replace",
                    "path": "/attributes/purchasable_offer",
                    "value": [
                        {
                        "marketplace_id": instance_id,
                        "our_price": [
                            {
                            "schedule": [
                                {
                                "value_with_tax": Pricelistitem["fixed_price"]
                                }
                            ]
                            }
                        ],
                        "maximum_retail_price": [
                            {
                            "schedule": [
                                {
                                "value_with_tax":  Pricelistitem["maximum_retail_price"]
                                }
                            ]
                            }
                        ]
                        }
                    ]
                    }
                ]
                })
                
                path_parameter = f"{seller_id}/{amazon_sku}?marketplaceIds={instance_id}&issueLocale=en_IN"
                utils.make_sp_api_request(account, operation, seller, path_parameter, payload, "PATCH")
    
    
class ActiveProductListing(models.Model):
    _name = 'active.product.listing.report.ept'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    name = fields.Char()
    seller_id = fields.Many2one("amazon.seller.ept", string='Seller')
    instance_id = fields.Many2one("amazon.instance.ept", string='MarketPlace')
    fulfillment_by = fields.Selection([('FBM', 'Manufacturer Fullfillment Network'), ('FBA', 'Amazon Fullfillment Network')], required=True)
    attachment_id = fields.Many2one("ir.attachment")
    log_count = fields.Integer()
    mismatch_details = fields.Boolean()
    # message_follower_ids = fields.One2many("mail.followers")
    
    # amzn1.spdoc.1.4.eu.903fb445-ee65-4a38-a253-7b9743c065c3.T362Z78KP4DVNX.300
    report_document_id = fields.Char(string="Report Document Reference")
    report_id = fields.Char()
    update_price_in_pricelist = fields.Boolean()
    auto_create_product = fields.Boolean()
    state = fields.Selection([('draft', 'Draft'),('_SUBMITTED_', 'SUBMITTED'),('_IN_PROGRESS_', 'IN_PROGRESS'),('_CANCELLED_  ', 'CANCELLED'),
                              ('_DONE_', 'DONE'),('CANCELLED', 'CANCELLED'),('SUBMITTED', 'SUBMITTED'),
                              ('DONE', 'DONE'), ('FATAL','FATAL'), ('IN_PROGRESS','IN_PROGRESS'), ('IN_QUEUE','IN_QUEUE'), ('_DONE_NO_DATA_','DONE_NO_DATA'), ('processed', 'PROCESSED'), ('imported', 'Imported'), ('partially_processed', 'Partially Processed'), ('closed','Closed')
                              ])
    user_id = fields.Many2one("res.users")
    report_type = fields.Char()
    live_product_json=fields.Text(string='Note',readonly=False,store=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('active.product.listing.report.ept') or ('New')
        return super(ActiveProductListing, self).create(vals)
    
    
    def request_report(self):
        pass


    def get_report_request_list(self):
        pass


    def get_report(self):
        pass


    def download_report(self):
        
        file_data = self.attachment_id.datas
        file_name = self.attachment_id.name

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model=ir.attachment&id={self.attachment_id.id}&field=datas&filename_field=name&download=true',
            'target': 'self',
        }


    def sync_products(self):
        data_string=f"""{self.live_product_json}"""
        data_string = data_string.replace("'", '"')
        final_dictionary = json.loads(data_string)

        for item in final_dictionary:
            if not self.env["amazon.product.ept"].search([("seller_sku", "=", item["seller-sku"])]) :
                if not self.env["product.product"].search([("default_code", "=", item["seller-sku"])]) :

                    product_id = self.env["product.product"].create({
                        "name" : item["item-name"],
                        # "default_code" : item["seller-sku"]
                        "default_code" :item["seller-sku"]
                    })
                    
                    map_product_id = self.env["map.amazon.product"].create({
                        "name" : item["item-name"],
                        "product_id" : product_id.id,
                        "Prod_int_ref" : product_id.default_code,
                        "amazon_sku": item["seller-sku"],
                        "marketplace" : self.instance_id.id,
                        "fulfillment" : "FBM",
                        "description" : "Importing product."
                    })

                    record = self.env["product.product"].search([("id", "=", product_id.id)]).write({'map_sku_id': [(4, map_product_id.id)]})
                    
                    self.env["amazon.product.ept"].create({
                        "name" : item["item-name"],
                        "seller_sku" : item["seller-sku"],
                        "product_id": product_id.id,
                        "instance_id": self.instance_id.id,
                        "fulfillment_by" : "FBM",
                        "standard_product_id_type" : "ASIN",
                        "product_asin": item["asin1"]
                    })
                
                    if not self.env["product.pricelist"].search([("instance_id", "=", self.instance_id.id)]):
                        # print("product list id",self.env["product.pricelist"].search([], limit=1).id)    
                        #create product
                        product_pricelist_item = self.env["product.pricelist"].create({
                                "name": f"Marketplace {self.instance_id.name}",
                                "instance_id": self.instance_id.id,
                                "seller_id":self.seller_id.id
                            }) 
                        
                        if not self.env["product.pricelist.item"].search([("amazon_sku", "=", item["seller-sku"])]):
                            product_pricelist_item_data = self.env["product.pricelist.item"].create({
                                "pricelist_id": product_pricelist_item.id,
                                "product_tmpl_id" : product_id.product_tmpl_id.id,
                                "min_quantity" : 1,
                                "fixed_price":0,
                                "maximum_retail_price":0,
                                "amazon_sku":item["seller-sku"]
                            }) 
                        
                    else:
                        product_pricelist_item_data = self.env["product.pricelist.item"].create({
                                "pricelist_id": self.env["product.pricelist"].search([("instance_id", "=", self.instance_id.id)]).id,
                                "product_tmpl_id" : product_id.product_tmpl_id.id,
                                "min_quantity" : 1,
                                "fixed_price":0,
                                "maximum_retail_price":0,
                                "amazon_sku":item["seller-sku"]
                            })     
                        
                else:
                    product_id = self.env["product.product"].search([("default_code", "=", item["seller-sku"])])
                    self.env["amazon.product.ept"].create({
                        "name" : item["item-name"],
                        "seller_sku" : item["seller-sku"],
                        "product_id": product_id.id,
                        "instance_id": self.instance_id.id,
                        "fulfillment_by" : "FBM",
                    })        
                    
        record = self.env["active.product.listing.report.ept"].search([("id", "=", self.id)]).write({'state': "processed","log_count":0})            

    def list_of_process_logs(self):
        pass


    def reprocess_sync_products(self):
        pass
    
    
    def action_open_mismatch_details(self):
     
        return {
            'type': 'ir.actions.act_window',
            'name': 'Mismatch Details',
            'res_model': 'common.log.lines.ept',
            'view_mode': 'tree,form',
            'target': 'current',
            'context': {'default_active_product_listing_report_id': self.id},
            'domain': [('active_product_listing_report_ept_id', '=', self.id)],
        }
    

class AmazonPriceList(models.Model):
    _inherit = 'product.pricelist.item'
    
    amazon_sku = fields.Char(string="Amazon SKU")
    maximum_retail_price = fields.Char(string="MAX Retail Price")

class AmazonPriceList(models.Model):
    _inherit = 'product.pricelist'
    
    seller_id = fields.Many2one("amazon.seller.ept", string='Seller')
    instance_id = fields.Many2one("amazon.instance.ept", string='MarketPlace')
    

class Productmodule(models.Model):
    _inherit = 'product.product'

    map_sku_id = fields.Many2many(
        'map.amazon.product',  # Target model
        'product_map_amazon_rel',  # Relation table
        'product_id',  # Column in the relation table for 'product.product'
        'amazon_product_id',  # Column in the relation table for 'map.amazon.product'
        string='Amazon SKU'
    )
    
    
class ProductLink(models.Model):
    _name = 'map.amazon.product'
    _description = 'Map amazon Product'
    _rec_name = 'amazon_sku'

    name = fields.Char('Title')
    product_id = fields.Many2one('product.product', string='Product',required=True)
    Prod_int_ref = fields.Char('Product Internal Ref', required=True)
    amazon_sku = fields.Char('Amazon SKU', required=True)
    marketplace = fields.Many2one('amazon.instance.ept', string='marketplace')
    fulfillment = fields.Char('Amazon SKU')
    description = fields.Char('description')    
    
    
    


