from odoo import models, fields, api, _
from ...amazon_connector_inwizards import const
from ...amazon_connector_inwizards import utils
from werkzeug import urls
from ..controllers.controllers import compute_oauth_signature
import json
from odoo.exceptions import UserError
from datetime import datetime, timedelta



class AmazonInfoAccount(models.Model):
    _name = "amazon.info.account"
    _check_company_auto = True
    _rec_name =  'seller_id'
    
    name = fields.Char(string="Name", help="The user-defined name of the account.")
    seller_id = fields.Many2one("amazon.seller.ept", string="Seller")
    # is_amz_program = fields.Boolean()
    # offer_ids = fields.One2many(
    #     string="Offers", comodel_name='amazon.offer', inverse_name='account_id', auto_join=True
    # )

    # Credentials fields.
    seller_key = fields.Char()
    refresh_token = fields.Char(
        string="LWA Refresh Token",
        help="The long-lived token that can be exchanged for a new access token.",
    )
    # The API credentials fields below are not stored because they are all short-lived. Their values
    # are kept in memory for the duration of the request and they are re-used as long as they are
    # not expired. If that happens, they are refreshed through an API call.
    access_token = fields.Char(
        string="LWA Access Token",
        help="The short-lived token used to query Amazon API on behalf of a seller.",
        store=True,
    )
    access_token_expiry = fields.Datetime(
        string="The moment at which the token becomes invalid.", default='1970-01-01', store=False
    )
    
    restricted_data_token = fields.Char(
        string="Restricted Data Token",
        help="The short-lived token used instead of the LWA Access Token to access restricted data",
        store=False,
    )
    restricted_data_token_expiry = fields.Datetime(
        string="The moment at which the Restricted Data Token becomes invalid.",
        default='1970-01-01',
        store=False,
    )

    # Marketplace fields.
    base_marketplace_id = fields.Many2one(
        string="Home Marketplace",
        help="The home marketplace of this account; used for authentication only.",
        comodel_name='amazon.retail.marketplace',
        required=True,
    )
    # available_marketplace_ids = fields.Many2many(
    #     string="Available Marketplaces",
    #     help="The marketplaces this account has access to.",
    #     comodel_name='amazon.marketplace',
    #     relation='amazon_account_marketplace_rel',
    #     copy=False,
    # )
    # active_marketplace_ids = fields.Many2many(
    #     string="Sync Marketplaces",
    #     help="The marketplaces this account sells on.",
    #     comodel_name='amazon.marketplace',
    #     relation='amazon_account_active_marketplace_rel',
    #     domain="[('id', 'in', available_marketplace_ids)]",
    #     copy=False,
    # )

    # Follow-up fields.
    # user_id = fields.Many2one(
    #     string="Salesperson",
    #     comodel_name='res.users',
    #     default=lambda self: self.env.user,
    #     check_company=True,
    # )
    # team_id = fields.Many2one(
    #     string="Sales Team",
    #     help="The Sales Team assigned to Amazon orders for reporting",
    #     comodel_name='crm.team',
    #     check_company=True,
    # )
    # company_id = fields.Many2one(
    #     string="Company",
    #     comodel_name='res.company',
    #     default=lambda self: self.env.company,
    #     required=True,
    #     readonly=True,
    # )
    # location_id = fields.Many2one(
    #     string="Stock Location",
    #     help="The location of the stock managed by Amazon under the Amazon Fulfillment program.",
    #     comodel_name='stock.location',
    #     domain="[('usage', '=', 'internal'), ('company_id', '=', company_id)]",
    #     check_company=True,
    # )
    active = fields.Boolean(
        string="Active",
        help="If made inactive, this account will no longer be synchronized with Amazon.",
        default=True,
        required=True,
    )
    # synchronize_inventory = fields.Boolean(
    #     string="Synchronize FBM Inventory",
    #     help="Whether the available quantities of FBM products linked to this account are"
    #          " synchronized with Amazon.",
    #     default=True,
    # )
    # last_orders_sync = fields.Datetime(
    #     help="The last synchronization date for orders placed on this account. Orders whose status "
    #          "has not changed since this date will not be created nor updated in Odoo.",
    #     default=fields.Datetime.now,
    #     required=True,
    # )

    # # Display fields.
    # order_count = fields.Integer(compute='_compute_order_count')
    # offer_count = fields.Integer(compute='_compute_offer_count')
    # is_follow_up_displayed = fields.Boolean(compute='_compute_is_follow_up_displayed')
    

    def action_redirect_to_oauth_url(self):
        
        """ Build the OAuth redirect URL and redirect the user to it.

        See step 1 of https://developer-docs.amazon.com/sp-api/docs/website-authorization-workflow.

        Note: self.ensure_one()

        :return: An `ir.actions.act_url` action to redirect the user to the OAuth URL.
        :rtype: dict
        """
        self.ensure_one()
        country_name = const.MARKETPLACE_COUNTRY[self.base_marketplace_id.name.split(".")[-1]]
        country_id = self.env["res.country"].search([("name", "=", country_name)])
        self.env["amazon.instance.ept"].create({
            "name": self.base_marketplace_id.name,
            "api_ref" : self.base_marketplace_id.api_ref,
            "seller_central_url" : self.base_marketplace_id.seller_central_url,
            "region" : self.base_marketplace_id.region,
            "country_id":country_id.id if country_id else False,
            "company_id":self.env.company.id,
            "warehouse_id": self.env["stock.warehouse"].search([], limit=1).id,
            "seller_id": self.env["amazon.seller.ept"].search([], limit=1).id,
            "amazon_retail_marketplace_id": self.base_marketplace_id.id
        })
        
        base_seller_central_url = self.base_marketplace_id.seller_central_url
        oauth_url = urls.url_join(base_seller_central_url, '/apps/authorize/consent')
        base_database_url = self.get_base_url()
        metadata = {
            'account_id': self.id,
            'return_url': urls.url_join(base_database_url, 'amazon/return'),
            'signature': compute_oauth_signature(self.id),
        }  
        
        oauth_url_params = {
            'application_id': const.APP_ID,
            'state': json.dumps(metadata),
        }
        return {
            'type': 'ir.actions.act_url',
            'url': f'{oauth_url}?{urls.url_encode(oauth_url_params)}',
            'target': 'self',
        }
        
    def generate_access_token(self):
        return utils.refresh_access_token(self)
        
class IrModuleModule(models.Model):
    _inherit = "ir.module.module"
    
    def write(self, vals):
        res = super(IrModuleModule, self).write(vals)
        actual_date = datetime.now().date()
        validate_date = actual_date + timedelta(days=365)
        
        if self.name == "amazon_connector_inwizards":
            self.env["customer.enrollment"].create({
                "actual_date" : actual_date,
                "validate_date" : validate_date
            })
            
        ir_cron = self.env["ir.cron"].search([("name", "=", "Renew Subscription")])
        if not ir_cron.is_hidden:
            ir_cron.is_hidden = True
        return res
    
class CustomerEnrollment(models.Model):
    _name = "customer.enrollment"
    
    actual_date = fields.Date()
    validate_date = fields.Date()
    
    def _validate_till_date(self):
        # actual_date = datetime.now().date()
        # latest_record = self.env["customer.enrollment"].search([])[:-1]
        # if actual_date > latest_record.validate_date:
        # import pdb;pdb.set_trace()
        
        menuitem = self.env["ir.ui.menu"].search([('parent_id.name', '=', 'Amazon'), ('name', '=', 'Dashboard')])
        action_id = self.env['ir.actions.act_window'].search([('name', '=', 'Renew Subscription')], limit=1).id
        if action_id:
            menuitem.action = f"ir.actions.act_window, {action_id}"
        else:
            action_id = self.env['ir.actions.act_window'].search([()], limit=1).id
            menuitem.action = f"ir.actions.act_window, {action_id}"
        
        
class amazon_connector_inwizards(models.Model):
    _name = 'amazon.connector'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"
    
    is_fba_warehouse = fields.Boolean()
    seller_id = fields.Many2one("amazon.seller.ept", string="Seller")
    fulfillment_center_ids = fields.One2many("amazon.fulfillment.center", "warehouse_id")
    unsellable_location_id = fields.Many2one("stock.location")
    
class AmazonFulfillmentCenter(models.Model):
    _name = "amazon.fulfillment.center"
    
    warehouse_id = fields.Many2one("stock.warehouse")
    seller_id = fields.Many2one("amazon.seller.ept", string="Seller")
    center_code = fields.Char()
    
class ResCountry(models.Model):
    _inherit = "res.country"
    
    amazon_marketplace_code = fields.Char()
    

class IrCron(models.Model):
    _inherit = 'ir.cron'

    is_hidden = fields.Boolean(default=lambda self: self._default_is_hidden())
    
    def _default_is_hidden(self):
        # import pdb;pdb.set_trace
        # Example condition: if the first record's `condition_field` is 'specific_value'
        return self.env['ir.cron'].browse(self.id).name == 'Renew Subscription'
    
class ResconfigAmazonseller(models.Model):
    _name = "res.config.amazon.seller"
    
    name = fields.Char()
    merchant_id = fields.Char(string="Merchant")
    amazon_selling = fields.Selection([('FBA', 'FBA'), ('FBM', 'FBM'), ('Both', 'FBA & FBM')], string="Fulfillment By ?")
    country_id = fields.Many2one("res.country", string="Country")
    company_id = fields.Many2one("res.company", string="Company")
    is_amz_program = fields.Boolean()
    
    def test_amazon_connection(self):
        warehouse_obj = self.env["stock.warehouse"]
        seller = self.env["amazon.seller.ept"].search([("merchant_id", "=", self.merchant_id)])
        api_ref = const.MAPPING_COUNTRY_WITH_MARKETPLACE.get(self.country_id.amazon_marketplace_code.strip())
        marketplace = self.env["amazon.retail.marketplace"].search([("api_ref", '=', api_ref)])
            
        if not seller:
            seller_id = self.env["amazon.seller.ept"].create({
                "name" : self.name,
                "country_id" : self.country_id.id,
                "company_id" : self.company_id.id,
                "merchant_id" : self.merchant_id,
                "amazon_selling" : self.amazon_selling,
                "is_european_region" :  True if marketplace.region == "eu-west-1" else False,
                "is_north_america_region" : True if marketplace.region == "us-east-1" else False
            })
            
            if self.amazon_selling == "FBA" or self.amazon_selling == "Both":
                seller_id.amz_warehouse_ids = [(0, 0, {
                    "name": f'FBA {marketplace.name} ({seller_id.name})' if marketplace  else f'FBA {self.country_id.name} ({seller_id.name})',
                    "code": f'{self.country_id.name[:2].lower()}{seller_id.id}',
                    "company_id": self.env.company.id,
                    "seller_id": seller_id.id,
                    "fulfillment_center_ids": [(0, 0, {'center_code': f'{self.country_id.name[:2].lower()}{seller_id.id}', "seller_id": seller_id.id})],
                    "is_fba_warehouse": True,
                    "partner_id": self.env["res.partner"].create({"name": f'{self.country_id.name[:2].lower()}{seller_id.id}'}).id
                })]
                
                warehouse_id = warehouse_obj.search([("code", "=", "WH")])
                fba_warehouse_id = seller_id.amz_warehouse_ids
                
                marketplace_id = self.env["amazon.instance.ept"].create({
                    "name" : f'{marketplace.name} ({seller_id.name})' if marketplace  else f'FBA {self.country_id.name}',
                    "country_id" : self.country_id.id,
                    "seller_id" : seller_id.id,
                    "company_id" : self.company_id.id,
                    "fba_warehouse_id": fba_warehouse_id.id if self.amazon_selling == "FBA" or self.amazon_selling == "Both" else None,
                    "warehouse_id": warehouse_id.id if warehouse_id and (self.amazon_selling == "FBM" or self.amazon_selling == "Both") else None,
                    "removal_warehouse_id" : warehouse_id.id if warehouse_id and (self.amazon_selling == "FBM" or self.amazon_selling == "Both") else None,
                    "amazon_retail_marketplace_id": marketplace.id if marketplace else None,
                    "api_ref" : marketplace.api_ref,
                    "seller_central_url" : marketplace.seller_central_url,
                })
                
                seller_id.marketplace_ids = [(0, 0, {'name': marketplace_id.name, "country_id": self.country_id.id, "currency_id": self.country_id.currency_id.id, "market_place_id": marketplace.api_ref if marketplace else None})]
                
                profit_account_id = self.env["account.account"].search([("name", "=", "Cash Difference Gain")])
                loss_account_id = self.env["account.account"].search([("name", "=", "Cash Difference Loss")])
                
                if self.amazon_selling == "FBA" or self.amazon_selling == "Both":
                    self.env["account.journal"].create({
                        "name": marketplace.name if marketplace  else self.country_id.name,
                        "type" : "bank",
                        "company_id": self.company_id.id,
                        "payment_sequence": True,
                        "code": f'{seller_id.name[:2]}{self.country_id.name[:2]}',
                        "currency_id": self.country_id.currency_id.id,
                        "profit_account_id": profit_account_id.id if profit_account_id else None,
                        "loss_account_id" :  loss_account_id.id if loss_account_id else None
                    })
                    
            self.env["amazon.info.account"].create({
                "name" : self.name,
                "base_marketplace_id" : marketplace.id,
                "seller_id" : seller_id.id
            })
            
            if not self.is_amz_program:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Account',
                    'view_mode': 'form',
                    'context': {'default_seller_id': seller_id.id},
                    'res_model': 'amazon.info.account',
                    'target' : 'new'
                }
            else :
                return{
                    'type': 'ir.actions.act_window',
                    'name': 'Marketplace',
                    'view_mode': 'form',
                    'context': {'default_seller_id': seller_id.id},
                    'res_model': 'add.amazon.fulfillment.center',
                    'target' : 'new'
                }
        else:
            raise UserError(_("Seller already exist."))

class AmznSubscription(models.TransientModel):
    _name = 'amzn.subscription'
    
    name = fields.Char()
    email = fields.Char(string="Email")
    country_id = fields.Many2one("res.country", string="Country")
    mobile = fields.Char()
    
    
    def activate_connector(self):
        # self.env["res.config.settings"].res_config_amazon_seller_action()
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seller Account',
            'view_mode': 'form',
            'res_model': 'res.config.amazon.seller',
            'target' : 'new'
        }
        

    
    
    
    
    
    

    